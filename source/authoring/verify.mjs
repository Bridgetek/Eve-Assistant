import {Client} from '../runtime/node_modules/@modelcontextprotocol/sdk/dist/esm/client/index.js';
import {StdioClientTransport} from '../runtime/node_modules/@modelcontextprotocol/sdk/dist/esm/client/stdio.js';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import assert from 'node:assert/strict';
import {spawnSync} from 'node:child_process';

const root=process.env.EVE_TEST_PLUGIN_ROOT || path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const arg=(name)=>{const i=process.argv.indexOf(name);return i>=0?process.argv[i+1]:undefined;};
const pre=arg('--pre82x') || process.env.EVEAPPS_PRE82X_ROOT;
const bt=arg('--bt82x') || process.env.EVEAPPS_BT82X_ROOT;
if(!pre||!bt) throw new Error('Provide --pre82x <EveApps path> --bt82x <EveApps-BT82X path>.');
const results={date:new Date().toISOString(),node:process.version,checks:[],tools:{}};
async function check(name,fn){try{await fn();results.checks.push({name,status:'Passed'});}catch(e){results.checks.push({name,status:'Failed',error:e.message});process.exitCode=1;}}
async function withServer(family,fn,overrides={}){
 const c=new Client({name:'eve-assistant-verifier',version:'1.0.0'});
 const t=new StdioClientTransport({command:process.execPath,args:[path.join(root,'scripts/launch.mjs'),family],env:{...process.env,EVEAPPS_PRE82X_ROOT:path.resolve(pre),EVEAPPS_BT82X_ROOT:path.resolve(bt),...overrides},stderr:'pipe'});
 t.stderr?.on('data',()=>{});
 try{await c.connect(t);await fn(c);}finally{await c.close();}
}
async function call(c,name,args){const r=await c.callTool({name,arguments:args});assert(!r.isError,JSON.stringify(r));const p=JSON.parse(r.content.find(x=>x.type==='text').text);assert(!p.error,JSON.stringify(p));return p;}
const testCalls={
 eab:[['catalog','list_eab_catalog',{},p=>assert(p.entries.length>0)],['image command','explain_eab_command',{command:'img_cvt'},p=>assert.equal(p.status,'ok')],['asset routing','find_relevant_eab_tool',{task:'convert PNG image to RGB565'},p=>assert.equal(p.status,'ok')],['workflows','list_eab_workflows',{},p=>assert(p.workflows.length>0)],['engineering query','eab',{query:'Convert a PNG image to RGB565'},p=>assert(p.answer.commands.length>0)]],
 bt82x:[['engineering query','ask_bt82x',{query:'CMD_BUTTON'},p=>assert(p.answer.commands.length>0)],['sample search','find_relevant_sample',{query:'touch widget button',limit:2},p=>assert(p.matches.length>0&&p.matches.length<=2)],['symbol lookup','explain_eve_symbol',{symbol:'CMD_BUTTON'},p=>assert.equal(p.found,true)],['code validation','validate_bt82x_code',{code:'void example(void) { EVE_Hal_wr8(phost, REG_GPIO, 1); }'},p=>assert(p.issues.length>0)],['repository read','bt82x_read_file',{relative_path:'README.md'},p=>assert(p.content.includes('EveApps-BT82X'))]],
 pre82x:[['engineering query','ask_pre820',{query:'CMD_BUTTON BT817'},p=>assert(p.answer.commands.length>0)],['sample search','find_relevant_sample',{query:'touch widget button',limit:2},p=>assert(p.matches.length>0&&p.matches.length<=2)],['symbol lookup','explain_eve_symbol',{symbol:'CMD_BUTTON',graphics:'BT817'},p=>assert.equal(p.found,true)],['module lookup','lookup_module_graphics',{module:'ME817EV'},p=>assert.equal(p.graphic,'BT817')],['repository read','pre820_read_file',{relative_path:'README.md'},p=>assert(p.content.includes('EveApps'))]]
};
for(const family of ['eab','bt82x','pre82x']) await check(family+' startup and tools',()=>withServer(family,async c=>{
 const tools=(await c.listTools()).tools;results.tools[family]=tools;
 assert.equal(tools.length,{eab:30,bt82x:8,pre82x:9}[family]);
 for(const t of tools) for(const field of ['readOnlyHint','destructiveHint','openWorldHint']) assert.equal(typeof t.annotations?.[field],'boolean',t.name+' '+field);
 for(const [label,name,args,validate] of testCalls[family]) await check(family+' '+label,async()=>validate(await call(c,name,args)));
}));
const temp=await fs.mkdtemp(path.join(os.tmpdir(),'eve-assistant-test-'));
try{
 const {eabSpecSelection,validateRustLayout}=await import(pathToFileURL(path.join(root,'scripts/launch.mjs')).href);
 await check('fresh EAB setup selects Rust chip-name specification',async()=>assert(eabSpecSelection({}, {}, root).spec.endsWith('EAB_mcp_data_for_EAB4.6.0.json')));
 await check('explicit legacy EAB remains supported',async()=>assert(eabSpecSelection({eabCliFlavor:'legacy'}, {}, root).spec.endsWith('EAB_mcp_data.json')));
 await check('existing path-only EAB config preserves auto detection',async()=>assert.equal(eabSpecSelection({eabToolsPath:'existing.exe'}, {}, root).flavor,'auto'));
 await check('explicit EAB spec override is preserved',async()=>assert.equal(eabSpecSelection({eabCliFlavor:'rust'}, {EAB_MCP_SPEC:'custom-spec.json'}, root).spec,undefined));
 await check('invalid EAB CLI flavor fails clearly',async()=>assert.throws(()=>eabSpecSelection({eabCliFlavor:'invalid'}, {}, root),/rust, legacy or auto/));
 const eabDir=path.join(temp,'eab');await fs.mkdir(eabDir);const fakeExe=path.join(eabDir,'eab_tools.exe');await fs.writeFile(fakeExe,'synthetic fixture; never executable');
 await check('Rust EAB rejects executable-only distribution',async()=>assert.throws(()=>validateRustLayout(fakeExe),/exts.*dependencies/));
 await fs.mkdir(path.join(eabDir,'exts'));await fs.mkdir(path.join(eabDir,'dependencies'));
 await check('Rust EAB accepts complete distribution layout',async()=>validateRustLayout(fakeExe));
 await check('Rust EAB MCP catalog uses chip-family tokens',()=>withServer('eab',async c=>{
  const p=await call(c,'list_eab_catalog',{});const tokens=new Set(p.entries.map(x=>x.chipGen));assert(tokens.has('bt82x'));assert(tokens.has('bt81x'));assert(!tokens.has('82x'));assert(!tokens.has('pre82x'));
  const command=await call(c,'explain_eab_command',{command:'img_cvt',targetChip:'BT82X'});assert(command.invocation.includes('bt82x img_cvt'));
 },{EVE_EAB_CLI_FLAVOR:'rust',EAB_MCP_SPEC:'',EAB_TOOLS_PATH:'',EVE_ASSISTANT_CONFIG:path.join(temp,'missing-eab-config.json')}));
 const repo=path.join(temp,'repo');await fs.mkdir(path.join(repo,'common'),{recursive:true});await fs.mkdir(path.join(repo,'SampleApp'));await fs.writeFile(path.join(repo,'README.md'),'EveApps test fixture');await fs.writeFile(path.join(temp,'outside.txt'),'OUTSIDE_FIXTURE_SENTINEL');
 let symlink=true;try{await fs.symlink(path.join(temp,'outside.txt'),path.join(repo,'outside.txt'));}catch{symlink=false;}
 for(const family of ['bt82x','pre82x']) await withServer(family,async c=>{
  const name=family==='bt82x'?'bt82x_read_file':'pre820_read_file';
  for(const relative_path of ['../outside.txt',...(symlink?['outside.txt']:[])]) await check(family+' rejects '+relative_path,async()=>{
   const r=await c.callTool({name,arguments:{relative_path}});const p=JSON.parse(r.content[0].text);assert(p.error);assert(!JSON.stringify(p).includes('OUTSIDE_FIXTURE_SENTINEL'));
  });
 },{EVEAPPS_PRE82X_ROOT:repo,EVEAPPS_BT82X_ROOT:repo});
 await check('missing repository fails without searching cwd',async()=>{
  const env={...process.env,EVE_ASSISTANT_CONFIG:path.join(temp,'missing-config.json')};delete env.EVEAPPS_BT82X_ROOT;delete env.EVEAPPS_PRE82X_ROOT;
  const r=spawnSync(process.execPath,[path.join(root,'scripts/launch.mjs'),'bt82x'],{env,encoding:'utf8'});assert.equal(r.status,1);assert(r.stderr.includes('absolute repository path'));assert.equal(r.stdout,'');
 });
 if(!symlink)results.checks.push({name:'symlink escape tests',status:'Blocked',reason:'OS does not permit symlink creation'});
}finally{await fs.rm(temp,{recursive:true,force:true});}
results.summary={passed:results.checks.filter(x=>x.status==='Passed').length,failed:results.checks.filter(x=>x.status==='Failed').length};
console.log(JSON.stringify(results,null,2));
