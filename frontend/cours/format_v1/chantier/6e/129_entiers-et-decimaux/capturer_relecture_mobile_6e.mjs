// Relecture des vues ciblées après l'audit exhaustif. Aucun changement du site.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';
import {createRequire} from 'node:module';
const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.dirname(here);
const require=createRequire(path.resolve(here,'../../../../../package.json'));
const {chromium}=require('playwright-core');
const browser=await chromium.launch({channel:'chrome',headless:true});
for(const code of (process.argv.slice(2).length?process.argv.slice(2):['129','130','131','133','150','151'])){
 const dir=path.join(root,fs.readdirSync(root).find(n=>n.startsWith(code+'_')));
 const shots=path.join(dir,'captures_relecture_6e');fs.mkdirSync(shots,{recursive:true});
 const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});
 await page.goto(pathToFileURL(path.join(dir,'apercu.html')).href);
 await page.waitForFunction('window.__ready !== undefined');await page.evaluate('window.__ready');
 // Le bandeau fixe est un outil de navigation de l'aperçu, à masquer uniquement sur les captures.
 await page.addStyleTag({content:'.ap-top{visibility:hidden!important}'});
 const tabs=await page.$$eval('.ap-tab',bs=>bs.map(b=>b.dataset.tab).filter(t=>t!=='exercices'));
 for(const tab of tabs){
  await page.evaluate(t=>document.querySelector(`.ap-tab[data-tab="${t}"]`).click(),tab);
  await page.waitForFunction(t=>document.getElementById(t).dataset.typeset==='1',tab);
  await page.evaluate('MathJax.startup.promise');
  const h=await page.evaluate(()=>document.documentElement.scrollHeight);
  for(let y=0,k=1;y<h;y+=2100,k++)await page.screenshot({path:path.join(shots,`${tab}-${k}.png`),fullPage:true,clip:{x:0,y,width:390,height:Math.min(2100,h-y)}});
 }
 await page.evaluate(()=>document.querySelector('.ap-tab[data-tab="exercices"]').click());
 for(const k of [0,9,20])for(let i=0;i<2;i++){
  await page.evaluate(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-tab')[i].click(),[k,i]);
  await page.waitForFunction(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-panel')[i].dataset.typeset==='1',[k,i]);
  await page.evaluate('MathJax.startup.promise');
  await page.locator('.ex-card').nth(k).screenshot({path:path.join(shots,`ex${k+1}-${i===0?'enonce':'etapes'}.png`)});
 }
 await page.close();console.log(code,'captures mobiles intégrales terminées');
}
await Promise.race([browser.close(),new Promise(r=>setTimeout(r,2000))]);
