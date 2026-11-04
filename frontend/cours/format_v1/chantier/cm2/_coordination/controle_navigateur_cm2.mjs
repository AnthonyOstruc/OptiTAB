// Audit de chaque vue avec le vrai moteur de l'aperçu ; un seul Chrome par appel.
import fs from 'node:fs';import path from 'node:path';
import {fileURLToPath,pathToFileURL} from 'node:url';import {createRequire} from 'node:module';
const here=path.dirname(fileURLToPath(import.meta.url));
const tools=path.resolve(here,'../../../outils');
const require=createRequire(path.resolve(here,'../../../../../package.json'));
const {chromium}=require('playwright-core');
const dir=path.resolve(process.argv[2]);const shots=path.join(dir,'captures_cm2');fs.mkdirSync(shots,{recursive:true});
const original=fs.readFileSync(path.join(tools,'controle_apercu.mjs'),'utf8');
const auditTemplate=original.match(/const AUDIT = (`[\s\S]*?`)\r?\n\r?\n\/\/ Au plus/)[1];
// Le module officiel fournit la même détection : aucun moteur parallèle.
const AUDIT=Function('return '+auditTemplate)().replace("querySelectorAll('mjx-merror')","querySelectorAll('mjx-merror, .mjx-merror, [data-mjx-error]')");
const browser=await chromium.launch({channel:'chrome',headless:true});
const checks=[];const captures=[];const errors=[];
try{
 for(const [format,viewport] of [['mobile',{width:390,height:844}],['desktop',{width:1280,height:900}]]){
  const page=await browser.newPage({viewport,deviceScaleFactor:1});
  page.on('pageerror',e=>errors.push(String(e)));
  await page.goto(pathToFileURL(path.join(dir,'apercu.html')).href);
  await page.waitForFunction('window.__ready !== undefined');await page.evaluate('window.__ready');
  const ready=async()=>{
   await page.evaluate('MathJax.startup.promise');
   await page.evaluate(()=>Promise.all([...document.querySelectorAll('img')].filter(i=>i.getClientRects().length).map(i=>i.decode().catch(()=>{}))));
   await page.evaluate(()=>new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r))));
  };
  const audit=async label=>{
   await ready();const detail=await page.evaluate(AUDIT);
   const broken=await page.evaluate(()=>[...document.querySelectorAll('.sci-doc img')].filter(i=>i.getClientRects().length&&(!i.complete||!i.naturalWidth)).length);
   const ok=detail.overflowX<=0&&!detail.merr.length&&!detail.raw.length&&!detail.imgs.length&&!detail.errs.length&&!detail.wide.length&&!broken;
   checks.push({format,vue:label,ok,...detail,images_cassees:broken});
  };
  const tabs=await page.$$eval('.ap-tab',bs=>bs.map(b=>b.dataset.tab).filter(t=>t!=='exercices'));
  for(const tab of tabs){
   await page.evaluate(t=>document.querySelector(`.ap-tab[data-tab="${t}"]`).click(),tab);
   await page.waitForFunction(t=>document.getElementById(t).dataset.typeset==='1',tab);await audit(tab);
   if(format==='mobile'){
    const h=await page.evaluate(()=>document.documentElement.scrollHeight);
    for(let y=0,k=1;y<h;y+=2100,k++){
     const name=`mobile-${tab}-${k}.png`;
     await page.screenshot({path:path.join(shots,name),fullPage:true,clip:{x:0,y,width:390,height:Math.min(2100,h-y)}});captures.push(name);
    }
   }
  }
  await page.evaluate(()=>document.querySelector('.ap-tab[data-tab="exercices"]').click());
  // Le bandeau est un outil de l'aperçu ; le masquer pour lire toute la carte en capture.
  await page.addStyleTag({content:'.ap-top{visibility:hidden!important}'});
  const count=await page.locator('.ex-card').count();
  for(let k=0;k<count;k++)for(let i=0;i<3;i++){
   await page.evaluate(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-tab')[i].click(),[k,i]);
   await page.waitForFunction(([k,i])=>document.querySelectorAll('.ex-card')[k].querySelectorAll('.ex-panel')[i].dataset.typeset==='1',[k,i]);
   await audit(`ex${k+1}-${['enonce','etapes','solution'][i]}`);
   if(format==='mobile'&&[0,10,count-1].includes(k)&&i<2){
    const name=`mobile-ex${k+1}-${i===0?'enonce':'etapes'}.png`;
    await page.locator('.ex-card').nth(k).screenshot({path:path.join(shots,name)});captures.push(name);
   }
  }
  await page.close();
 }
}finally{await Promise.race([browser.close(),new Promise(r=>setTimeout(r,2000))]);}
const bad=checks.filter(c=>!c.ok);
const report={date:new Date().toISOString(),statut:bad.length||errors.length?'a_corriger':'OK',vues_distinctes:checks.length,anomalies:bad.length+errors.length,controles:checks,captures,erreurs:errors};
fs.writeFileSync(path.join(dir,'audit_navigateur_cm2.json'),JSON.stringify(report,null,2)+'\n');
console.log(JSON.stringify({statut:report.statut,vues_distinctes:checks.length,anomalies:report.anomalies,ecarts:bad,erreurs:errors}));
process.exitCode=report.anomalies?2:0;
