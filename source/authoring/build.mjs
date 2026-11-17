import fs from 'node:fs/promises';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {build} from '../runtime/node_modules/esbuild/lib/main.js';

const work=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const dest=path.join(work,'plugin');
const upstream=path.join(work,'runtime','node_modules','@bridgetek');
const base=process.env.EVE_BASE_PLUGIN || path.join(work,'base-plugin');
await fs.mkdir(dest,{recursive:true});
await fs.cp(base,dest,{recursive:true});
await fs.mkdir(path.join(dest,'scripts'),{recursive:true});
for(const file of ['launch.mjs','configure.mjs']) await fs.copyFile(path.join(work,'authoring',file),path.join(dest,'scripts',file));
await fs.copyFile(path.join(work,'authoring/rust-eab-cli.md'),path.join(dest,'skills/instructions/references/rust-eab-cli.md'));
await fs.copyFile(path.join(work,'authoring/eve-emulator-setup.md'),path.join(dest,'skills/instructions/references/eve-emulator-setup.md'));
await build({absWorkingDir:work,entryPoints:[path.join(work,'authoring/verify.mjs')],outfile:path.join(dest,'scripts/verify.mjs'),bundle:true,platform:'node',format:'esm',target:'node20',legalComments:'linked',banner:{js:"import {createRequire as eveRequire} from 'node:module'; const require = eveRequire(import.meta.url);"}});
for(const family of ['bt82x','pre82x']) {
 const packageName=`eveapps-${family}-mcp-server`;
 const coreName=`eveapps-${family}-core`;
 const out=path.join(dest,'server',family,'dist','lib','index.mjs');
 const patches={name:'eve-assistant-integration',setup(b){b.onLoad({filter:/\.js$/},async args=>{
  if(!args.path.includes('@bridgetek')) return;
  let contents=await fs.readFile(args.path,'utf8');
  if(args.path.endsWith('/server.js') && args.path.includes(packageName)) {
   contents=contents.replace(/server\.registerTool\(("[^"]+"), \{/g,'server.registerTool($1, {\n    annotations: {readOnlyHint: true, destructiveHint: false, openWorldHint: false},');
  }
  if(args.path.endsWith('/searchSourceFiles.js')) contents=contents.replace('for (const entry of entries) {','for (const entry of entries) {\n        if (entry.isSymbolicLink()) continue;');
  if(family==='bt82x' && args.path.endsWith('/tools/readSourceFile.js')) {
   const needle='    return {\n        path: relativePath.split(path.sep).join("/"),';
   if(!contents.includes(needle)) throw new Error('Unexpected BT82X reader source');
   contents=contents.replace(needle,`    const realRoot = fs.realpathSync(repoRoot);
    const realFile = fs.realpathSync(fullPath);
    const realRelative = path.relative(realRoot, realFile);
    if (realRelative === '..' || realRelative.startsWith('..' + path.sep) || path.isAbsolute(realRelative)) {
        throw new Error('relative_path resolves outside the local EveApps repository root.');
    }
    return {
        path: relativePath.split(path.sep).join("/"),`);
  }
  return {contents,loader:'js'};
 });}};
 await build({absWorkingDir:work,entryPoints:[path.join(upstream,packageName,'dist','cli.js')],outfile:out,bundle:true,platform:'node',format:'esm',target:'node20',legalComments:'linked',banner:{js:"import {createRequire as eveCreateRequire} from 'node:module'; const require = eveCreateRequire(import.meta.url);"},plugins:[patches]});
 await fs.cp(path.join(upstream,coreName,'data'),path.join(dest,'server',family,'data'),{recursive:true});
}
let eab=await fs.readFile(path.join(upstream,'eab-mcp-server/dist/index.js'),'utf8');
const needle='    inputSchema: tool.inputSchema\n  }))';
if(!eab.includes(needle)) throw new Error('Unexpected EAB tool-list source');
eab=eab.replace(needle,`    inputSchema: tool.inputSchema,
    annotations: {
      readOnlyHint: !['prepare_eab_tool_call','update_eab_tool_call','execute_eab_tool_call','install_eab_cli'].includes(tool.name) && !tool.name.startsWith('eab_') || ['eab_sample'].includes(tool.name),
      destructiveHint: ['execute_eab_tool_call','install_eab_cli'].includes(tool.name),
      openWorldHint: ['check_eab_installation','install_eab_cli','eab_sample','execute_eab_tool_call'].includes(tool.name)
    }
  }))`);
await fs.mkdir(path.join(dest,'server/eab/dist/lib'),{recursive:true});
await fs.writeFile(path.join(dest,'server/eab/dist/lib/index.mjs'),eab);
for(const file of ['EAB_mcp_data.json','EAB_mcp_data_for_EAB4.6.0.json','LICENSE','README.md']) await fs.copyFile(path.join(upstream,'eab-mcp-server',file),path.join(dest,'server/eab',file));
console.log(dest);
