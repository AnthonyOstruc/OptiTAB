// Captures de relecture seulement : les audits complets restent dans leurs rapports.
import fs from 'node:fs';import path from 'node:path';import {fileURLToPath,pathToFileURL} from 'node:url';import {createRequire} from 'node:module';
const here=path.dirname(fileURLToPath(import.meta.url));const root=path.dirname(here);
const require=createRequire(path.resolve(here,'../../../../../package.json'));const {chromium}=require('playwright-core');
const browser=await chromium.launch({channel:'chrome',headless:true});
try{
 for(const n of process.argv.slice(2).map(Number)){
  const name=fs.readdirSync(root).find(x=>x.startsWith(String(n).padStart(2,'0')+'_'));const d=path.join(root,name);
  const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});
  await page.goto(pathToFileURL(path.join(d,'apercu.html')).href);await page.waitForFunction('window.__ready !== undefined');await page.evaluate('window.__ready');
  await page.addStyleTag({content:'.ap-top{visibility:hidden!important}'});
  await page.evaluate(()=>document.querySelector('.ap-tab[data-tab="exercices"]').click());
  for(const k of [0,10,20])for(let i=0;i<2;i++){
   await page.evaluate(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-tab')[i].click(),[k,i]);
   await page.waitForFunction(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-panel')[i].dataset.typeset==='1',[k,i]);await page.evaluate('MathJax.startup.promise');
   await page.locator('.ex-card').nth(k).screenshot({path:path.join(d,'captures_cm2',`mobile-ex${k+1}-${i===0?'enonce':'etapes'}.png`)});
  }
  await page.close();console.log(n,'captures entières, sans bandeau superposé');
 }
}finally{await Promise.race([browser.close(),new Promise(r=>setTimeout(r,2000))]);}
