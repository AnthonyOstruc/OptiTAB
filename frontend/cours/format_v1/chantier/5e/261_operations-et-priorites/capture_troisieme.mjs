// Complète les captures officielles par l’énoncé du troisième exercice.
import path from 'node:path'
import {createRequire} from 'node:module'
import {fileURLToPath} from 'node:url'
const here=path.dirname(fileURLToPath(import.meta.url))
const require=createRequire(path.resolve(here,'../../../../../package.json'))
const {chromium}=require('playwright-core')
const folder=path.resolve(process.argv[2])
const browser=await chromium.launch({channel:'chrome',headless:true})
const page=await browser.newPage({viewport:{width:390,height:1200}})
await page.goto('file:///'+path.join(folder,'apercu.html').replace(/\\/g,'/'))
await page.waitForFunction('window.__ready !== undefined')
await page.evaluate('window.__ready')
await page.click('.ap-tab[data-tab="exercices"]')
await page.evaluate(()=>document.querySelectorAll('.ex-card')[2].querySelectorAll('.ex-tab')[0].click())
await page.waitForFunction(()=>document.querySelectorAll('.ex-card')[2].querySelectorAll('.ex-panel')[0].dataset.typeset==='1')
await page.evaluate('MathJax.startup.promise')
await page.evaluate(()=>window.scrollBy(0,document.querySelectorAll('.ex-card')[2].getBoundingClientRect().top-160))
await page.locator('.ex-card').nth(2).screenshot({path:path.join(folder,'captures/mobile-ex03-enonce.png')})
await Promise.race([browser.close(), new Promise(resolve=>setTimeout(resolve,2000))])
process.stdout.write('Capture mobile du troisième énoncé enregistrée.\n',()=>process.exit(0))
