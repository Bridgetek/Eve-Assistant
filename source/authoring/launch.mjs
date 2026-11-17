import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {spawn} from 'node:child_process';

export function configPath() {
  return process.env.EVE_ASSISTANT_CONFIG || path.join(os.homedir(), '.config', 'bridgetek-eve-assistant', 'config.json');
}
export function loadConfig() {
  const file = configPath();
  if (!fs.existsSync(file)) return {};
  const cfg = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!cfg || typeof cfg !== 'object' || Array.isArray(cfg)) throw new Error('Configuration must be a JSON object.');
  return cfg;
}
export function validateRepo(input) {
  if (typeof input !== 'string' || !input.trim() || !path.isAbsolute(input)) throw new Error('An absolute repository path is required. Run node scripts/configure.mjs.');
  const real = fs.realpathSync(input);
  for (const dir of ['common', 'SampleApp']) if (!fs.statSync(path.join(real,dir)).isDirectory()) throw new Error('Repository must contain common and SampleApp directories.');
  return real;
}
export function eabSpecSelection(cfg, env, pluginRoot) {
  // Preserve older saved configurations through auto-detection. Fresh setups
  // prefer the Rust CLI; users can explicitly retain the legacy executable.
  const flavor = env.EVE_EAB_CLI_FLAVOR || cfg.eabCliFlavor || (cfg.eabToolsPath || env.EAB_TOOLS_PATH ? 'auto' : 'rust');
  if (!['rust','legacy','auto'].includes(flavor)) throw new Error('EAB CLI flavor must be rust, legacy or auto.');
  if (env.EAB_MCP_SPEC || flavor === 'auto') return {flavor};
  const spec = path.join(pluginRoot,'server','eab',flavor === 'rust' ? 'EAB_mcp_data_for_EAB4.6.0.json' : 'EAB_mcp_data.json');
  if (!fs.statSync(spec).isFile()) throw new Error('Bundled EAB command specification is missing.');
  return {flavor,spec};
}
export function validateRustLayout(executable) {
  const directory = path.dirname(fs.realpathSync(executable));
  for (const folder of ['exts','dependencies']) {
    const candidate=path.join(directory,folder);
    if (!fs.existsSync(candidate) || !fs.statSync(candidate).isDirectory()) throw new Error('Rust EAB CLI requires exts/ and dependencies/ beside eab_tools.exe; extract the complete EAB-CLI distribution.');
  }
}
const pluginRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const family = process.argv[2];
    if (!['eab','bt82x','pre82x'].includes(family)) throw new Error('Expected eab, bt82x or pre82x.');
    const cfg = loadConfig();
    const env = {...process.env};
    let cwd = pluginRoot;
    const entry = path.join(pluginRoot,'server',family,'dist','lib','index.mjs');
    const args = [entry];
    if (family === 'eab') {
      if (cfg.eabToolsPath && !env.EAB_TOOLS_PATH) env.EAB_TOOLS_PATH = cfg.eabToolsPath;
      if (env.EAB_TOOLS_PATH && (!path.isAbsolute(env.EAB_TOOLS_PATH) || !fs.statSync(env.EAB_TOOLS_PATH).isFile())) throw new Error('EAB_TOOLS_PATH must point to an installed EAB executable.');
      const selection=eabSpecSelection(cfg,env,pluginRoot);
      if(selection.flavor==='rust' && env.EAB_TOOLS_PATH) validateRustLayout(env.EAB_TOOLS_PATH);
      if(selection.spec) env.EAB_MCP_SPEC=selection.spec;
      // Always use stdio. Do not expose the EAB HTTP listener from this plugin.
      args.push('--transport','stdio');
    } else {
      cwd = validateRepo(family === 'bt82x' ? (env.EVEAPPS_BT82X_ROOT || cfg.bt82xRepo) : (env.EVEAPPS_PRE82X_ROOT || cfg.pre82xRepo));
      args.push('--eveapps',cwd);
    }
    const child = spawn(process.execPath,args,{cwd,env,stdio:'inherit',shell:false,windowsHide:true});
    child.on('error',err=>{console.error('[EVE Assistant]',err.message);process.exitCode=1;});
    child.on('exit',(code,signal)=>{process.exitCode=code ?? (signal ? 1 : 0);});
    for(const signal of ['SIGINT','SIGTERM']) process.on(signal,()=>child.kill(signal));
  } catch(err) { console.error('[EVE Assistant]',err.message); process.exitCode=1; }
}
