// Relecture mobile : un nouvel exercice easy, medium et hard, rendu réel.
import path from 'node:path'
import fs from 'node:fs'
import {createRequire} from 'node:module'
import {fileURLToPath} from 'node:url'
const here=path.dirname(fileURLToPath(import.meta.url))
const require=createRequire(path.resolve(here,'../../../../../package.json'))
const {chromium}=require('playwright-core')
const folder=path.resolve(process.argv[2])
const out=path.join(folder,'captures_revision_2026-10-30')
fs.mkdirSync(out,{recursive:true})
const browser=await chromium.launch({channel:'chrome',headless:true})
const page=await browser.newPage({viewport:{width:390,height:844}})
await page.goto('file:///'+path.join(folder,'apercu.html').replace(/\\/g,'/'))
await page.waitForFunction('window.__ready !== undefined')
await page.evaluate('window.__ready')
await page.click('.ap-tab[data-tab="exercices"]')
for (const k of [4,11,18]) {
  await page.evaluate(k=>document.querySelectorAll('.ex-card').forEach((el,i)=>{el.style.display=i===k?'':'none'}),k)
  for (const i of [0,1]) {
    await page.evaluate(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-tab')[i].click(),[k,i])
    await page.waitForFunction(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-panel')[i].dataset.typeset==='1',[k,i])
    await page.evaluate('MathJax.startup.promise')
    await page.evaluate(()=>window.scrollTo(0,0))
    await page.screenshot({path:path.join(out,`revision-mobile-ex${String(k+1).padStart(2,'0')}-${i?'etapes':'enonce'}.png`),fullPage:true})
  }
}
await Promise.race([browser.close(),new Promise(resolve=>setTimeout(resolve,2000))])
process.stdout.write('Six vues des nouveaux exercices enregistrées.\n',()=>process.exit(0))
