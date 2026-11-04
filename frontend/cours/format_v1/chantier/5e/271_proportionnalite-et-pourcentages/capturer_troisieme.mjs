// Complète les captures du contrôleur par un troisième énoncé sur téléphone.
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
const here=path.dirname(fileURLToPath(import.meta.url));
const require=createRequire(path.resolve(here,'../../../../../package.json'));
const {chromium}=require('playwright-core');
const d=path.resolve(process.argv[2]);
const shots=path.resolve(process.argv[3]||path.join(d,'captures'));
const selected=(process.argv[4]||'2').split(',').map(Number);
const browser=await chromium.launch({channel:'chrome',headless:true});
try {
  const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1});
  await page.goto('file:///'+path.join(d,'apercu.html').replaceAll('\\','/'));
  await page.waitForFunction('window.__ready !== undefined');await page.evaluate('window.__ready');
  await page.click('.ap-tab[data-tab="exercices"]');
  for(const k of selected){
    await page.evaluate(k=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-tab')[0].click(),k);
    await page.waitForFunction(k=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-panel')[0].dataset.typeset==='1',k);
    await page.evaluate('MathJax.startup.promise');
    await page.locator('.ex-card').nth(k).screenshot({path:path.join(shots,`mobile-ex${String(k+1).padStart(2,'0')}-enonce.png`)});
    console.log(`Énoncé mobile ${k+1} capturé.`);
  }
} finally {await Promise.race([browser.close(),new Promise(resolve=>setTimeout(resolve,2000))]);}
await new Promise(resolve=>process.stdout.write('',resolve));process.exit(0);
