// Vérifie tous les panneaux typesettés, y compris les erreurs SVG MathJax.
import path from 'node:path'
import fs from 'node:fs'
import {createRequire} from 'node:module'
import {fileURLToPath} from 'node:url'
const here=path.dirname(fileURLToPath(import.meta.url))
const require=createRequire(path.resolve(here,'../../../../../package.json'))
const {chromium}=require('playwright-core')
const base=path.dirname(here)
const browser=await chromium.launch({channel:'chrome',headless:true})
let failures=0
for(const code of [261,262,263,264,265]) {
 const folder=path.join(base,fs.readdirSync(base).find(x=>x.startsWith(code+'_')))
 const page=await browser.newPage({viewport:{width:390,height:844}})
 await page.goto('file:///'+path.join(folder,'apercu.html').replace(/\\/g,'/'))
 await page.waitForFunction('window.__ready !== undefined')
 await page.evaluate('window.__ready')
 const tabs=await page.$$eval('.ap-tab',bs=>bs.map(x=>x.dataset.tab).filter(x=>x!=='exercices'))
 for(const tab of tabs) {
   await page.click(`.ap-tab[data-tab="${tab}"]`)
   await page.waitForFunction(id=>document.getElementById(id).dataset.typeset==='1',tab)
   await page.evaluate('MathJax.startup.promise')
 }
 await page.click('.ap-tab[data-tab="exercices"]')
 const count=await page.locator('.ex-card').count()
 for(let k=0;k<count;k++) for(let i=0;i<3;i++) {
   await page.evaluate(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-tab')[i].click(),[k,i])
   await page.waitForFunction(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-panel')[i].dataset.typeset==='1',[k,i])
   await page.evaluate('MathJax.startup.promise')
 }
 const errors=await page.$$eval('mjx-merror,.mjx-merror,[data-mjx-error],.MathJax_Error',els=>els.map(x=>({message:x.getAttribute('data-mjx-error')||x.textContent,html:x.outerHTML.slice(0,250)})))
 const raw=await page.locator('.sci-doc').allTextContents()
 const inputErrors=raw.filter(x=>x.includes('Math input error'))
 const report={date:'2026-10-30',panneaux_typesettes:tabs.length+count*3,selecteurs:'mjx-merror, .mjx-merror, [data-mjx-error], .MathJax_Error',erreurs:errors,math_input_error:inputErrors}
 fs.writeFileSync(path.join(folder,'controle_mathjax_etendu.json'),JSON.stringify(report,null,2)+'\n')
 failures+=errors.length+inputErrors.length
 console.log(code,report.panneaux_typesettes,'panneaux,',errors.length+inputErrors.length,'erreur(s)')
 await page.close()
}
await Promise.race([browser.close(),new Promise(resolve=>setTimeout(resolve,2000))])
process.stdout.write('Contrôle MathJax étendu terminé.\n',()=>process.exit(failures?1:0))
