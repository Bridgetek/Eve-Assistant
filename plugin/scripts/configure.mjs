import fs from 'node:fs';
import path from 'node:path';
import readline from 'node:readline/promises';
import {stdin,stderr} from 'node:process';
import {configPath,loadConfig,validateRepo,validateRustLayout} from './launch.mjs';

const rl=readline.createInterface({input:stdin,output:stderr});
try {
 const cfg=loadConfig();
 console.error('Configure local EVE Assistant paths. No software is downloaded or installed.');
 const oldFlavor=cfg.eabCliFlavor || (cfg.eabToolsPath ? 'auto' : 'rust');
 const flavor=(await rl.question(`EAB CLI edition: rust, legacy or auto [${oldFlavor}]: `)).trim() || oldFlavor;
 if(!['rust','legacy','auto'].includes(flavor)) throw new Error('Choose rust, legacy or auto.');
 cfg.eabCliFlavor=flavor;
 console.error('Rust EAB CLI: https://github.com/Bridgetek/EAB-CLI — extract the complete Windows distribution, including exts/ and dependencies/.');
 for(const [key,label] of [['pre82xRepo','EveApps repository'],['bt82xRepo','EveApps-BT82X repository'],['eabToolsPath','EAB executable']]) {
  const input=(await rl.question(`${label} [${cfg[key] || 'leave blank to configure later'}]: `)).trim();
  if(input) cfg[key]=input;
  if(cfg[key]) {
   if(key.endsWith('Repo')) cfg[key]=validateRepo(cfg[key]);
   else if(!path.isAbsolute(cfg[key]) || !fs.statSync(cfg[key]).isFile()) throw new Error('EAB executable must be an existing absolute file path.');
  }
 }
 if(cfg.eabCliFlavor==='rust' && cfg.eabToolsPath) validateRustLayout(cfg.eabToolsPath);
 const file=configPath();fs.mkdirSync(path.dirname(file),{recursive:true});fs.writeFileSync(file,JSON.stringify(cfg,null,2)+'\n',{mode:0o600});
 console.error(`Saved ${file}. Restart the plugin MCP connections to load it.`);
} catch(err) {console.error(err.message);process.exitCode=1;} finally{rl.close();}
