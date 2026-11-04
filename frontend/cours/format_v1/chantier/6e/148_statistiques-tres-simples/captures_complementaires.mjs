// Capture réelle de l'énoncé du troisième exercice, en complément de l'outil commun.
import fs from 'node:fs'
import path from 'node:path'
import {createRequire} from 'node:module'
import {fileURLToPath} from 'node:url'
const here=path.dirname(fileURLToPath(import.meta.url))
const require=createRequire(path.resolve(here,'../../../../../package.json'))
const {chromium}=require('playwright-core')
const browser=await chromium.launch({channel:'chrome',headless:true})
try {
  const page=await browser.newPage({viewport:{width:390,height:844},deviceScaleFactor:1})
  await page.goto('file:///'+path.join(here,'apercu.html').replaceAll('\\','/'))
  await page.waitForFunction('window.__ready !== undefined')
  await page.evaluate('window.__ready')
  await page.click('.ap-tab[data-tab="exercices"]')
  // Prise de vue seulement : l’en-tête ne doit pas recouvrir la carte.
  await page.addStyleTag({content:'.ap-top{position:static!important}'})
  fs.mkdirSync(path.join(here,'captures'),{recursive:true})
  for (const k of [0,9,20]) for (const i of [0,1]) {
    await page.evaluate(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-tab')[i].click(),[k,i])
    await page.evaluate(async([k,i])=>{
      const p=document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-panel')[i]
      await MathJax.startup.promise
      await MathJax.typesetPromise([p])
      tuneMathOverflow(p)
    },[k,i])
    await page.locator('.ex-card').nth(k).screenshot({path:path.join(here,`captures/mobile-ex${String(k+1).padStart(2,'0')}-${i?'etapes':'enonce'}.png`)})
  }
  const imageErrors=await page.$$eval('img',imgs=>imgs.filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src.slice(0,100)))
  if(imageErrors.length)throw new Error('Images manquantes : '+imageErrors.join(', '))
  console.log('Captures mobiles ex01, ex10 et ex21, images réellement chargées : OK')
} catch(error) {console.error(error);process.exitCode=1}
finally {await Promise.race([browser.close(),new Promise(resolve=>setTimeout(resolve,2000))])}
await new Promise(resolve=>process.stdout.write('',resolve))
process.exit(process.exitCode||0)
