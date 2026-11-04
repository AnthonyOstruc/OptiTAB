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
  await page.evaluate(()=>document.querySelectorAll('.ex-card')[2].querySelectorAll('.ex-tab')[0].click())
  await page.waitForFunction(()=>document.querySelectorAll('.ex-card')[2].querySelectorAll('.ex-panel')[0].dataset.typeset==='1')
  const imageErrors=await page.$$eval('img',imgs=>imgs.filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src.slice(0,100)))
  if(imageErrors.length)throw new Error('Images manquantes : '+imageErrors.join(', '))
  fs.mkdirSync(path.join(here,'captures'),{recursive:true})
  await page.locator('.ex-card').nth(2).screenshot({path:path.join(here,'captures/mobile-ex03-enonce.png')})
  console.log('Capture supplémentaire mobile ex03, images réellement chargées : OK')
} catch(error) {console.error(error);process.exitCode=1}
finally {await Promise.race([browser.close(),new Promise(resolve=>setTimeout(resolve,2000))])}
await new Promise(resolve=>process.stdout.write('',resolve))
process.exit(process.exitCode||0)
