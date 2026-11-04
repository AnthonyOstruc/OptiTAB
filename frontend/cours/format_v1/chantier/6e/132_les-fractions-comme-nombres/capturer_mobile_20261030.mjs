// Captures réelles des documents entiers et de trois exercices de difficultés distinctes.
import path from 'node:path'
import fs from 'node:fs'
import {createRequire} from 'node:module'
import {fileURLToPath} from 'node:url'
const here=path.dirname(fileURLToPath(import.meta.url))
const require=createRequire(path.resolve(here,'../../../../../package.json'))
const {chromium}=require('playwright-core')
const folder=path.resolve(process.argv[2]),out=path.join(folder,process.argv[3]?'captures_doublons_2026-11-01':'captures_mobile_2026-10-30')
fs.mkdirSync(out,{recursive:true})
const browser=await chromium.launch({channel:'chrome',headless:true})
const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1})
await page.goto('file:///'+path.join(folder,'apercu.html').replace(/\\/g,'/'))
await page.waitForFunction('window.__ready !== undefined');await page.evaluate('window.__ready')
// Le bandeau fixe de l’aperçu ne doit pas masquer le haut d’un document capturé.
await page.addStyleTag({content:'.ap-top { position: static !important; }'})
const tabs=await page.$$eval('.ap-tab',els=>els.map(x=>x.dataset.tab).filter(x=>x!=='exercices'))
let total=0,errors=[]
for(const tab of tabs){
 await page.click(`.ap-tab[data-tab="${tab}"]`)
 await page.waitForFunction(id=>document.getElementById(id).dataset.typeset==='1',tab)
 await page.evaluate('MathJax.startup.promise')
 await page.locator('#'+tab).screenshot({path:path.join(out,`mobile-${tab}-entier.png`)})
 total++
}
await page.click('.ap-tab[data-tab="exercices"]')
const cards=await page.locator('.ex-card').count(),selected=process.argv[3]?process.argv[3].split(',').map(x=>Number(x)-1):cards===8?[0,4,7]:[1,8,19]
for(const k of selected){
 await page.evaluate(k=>document.querySelectorAll('.ex-card').forEach((e,i)=>{e.style.display=i===k?'':'none'}),k)
 for(const i of [0,1]){
  await page.evaluate(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-tab')[i].click(),[k,i])
  await page.waitForFunction(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-panel')[i].dataset.typeset==='1',[k,i])
  await page.evaluate('MathJax.startup.promise')
  await page.locator('.ex-card').nth(k).screenshot({path:path.join(out,`mobile-ex${k+1}-${i?'etapes':'enonce'}.png`)})
  errors.push(...await page.$$eval('mjx-merror,.mjx-merror,[data-mjx-error],.MathJax_Error',els=>els.map(x=>x.getAttribute('data-mjx-error')||x.textContent)))
  total++
 }
}
fs.writeFileSync(path.join(out,'preuves_captures.json'),JSON.stringify({viewport:{width:390,height:844},documents_entiers:tabs,exercices_indices:selected.map(x=>x+1),captures:total,erreurs_mathjax:errors},null,2))
await Promise.race([browser.close(),new Promise(r=>setTimeout(r,2000))])
process.stdout.write(`${total} captures mobiles ; ${errors.length} erreur(s) MathJax.\n`,()=>process.exit(errors.length?1:0))
