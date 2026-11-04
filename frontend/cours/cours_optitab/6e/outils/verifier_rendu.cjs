// Vérifie le rendu réel des contenus avec MathJax, sur ordinateur et téléphone.
// Réutilise le formateur des exercices du composant Vue, sans copie divergente.
const fs=require('fs');
const path=require('path');
const {pathToFileURL}=require('url');
const root=path.resolve(__dirname,'..');
const front=path.resolve(root,'../../..');
const {chromium}=require(path.join(front,'node_modules/playwright'));
const component=fs.readFileSync(path.join(front,'src/components/UI/ExerciceQCM.vue'),'utf8');
const src=component.slice(component.indexOf('function unescapeLatex('),component.indexOf('const IMAGE_PLACEHOLDER_REGEX'));
const format=new Function(src+'; return unescapeLatex;')();
const out=path.join(root,'verifications/rendus');fs.mkdirSync(out,{recursive:true});
const slugs=[...new Set(JSON.parse(fs.readFileSync(path.join(root,'verifications/manifeste.json'),'utf8')).map(x=>x.slug))];
const imageField=txt=>(txt.match(/^Images:\s*(.+)$/m)?.[1]||'').split(',').map(x=>x.trim()).filter(Boolean);
function images(body,names,dir){
  return body.replace(/\[IMAGE_(\d+)\]/g,(_,i)=>'<img alt="Figure pédagogique '+i+'" src="'+pathToFileURL(path.join(dir,names[Number(i)-1])).href+'">');
}
function html(title,body){
  const mj=pathToFileURL(path.join(front,'node_modules/mathjax/es5/tex-svg.js')).href;
  return '<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>'+title+'</title><style>body{margin:0;background:#edf2f7;color:#24364a;font:16px/1.7 Arial,sans-serif}main{box-sizing:border-box;max-width:900px;margin:20px auto;padding:20px;background:white;border-radius:12px}h1{font-size:25px}img{display:block;max-width:100%;height:auto;margin:20px auto}mjx-container{max-width:100%}.step-bullet{margin:12px 0}.step-title{margin:8px 0}code{overflow-wrap:anywhere}@media(max-width:500px){main{margin:8px;padding:12px}h1{font-size:22px}.step-bullet{margin-left:0!important}}</style><script>window.MathJax={tex:{inlineMath:[["$","$"]]},svg:{fontCache:"global"},startup:{typeset:true}}</script><script src="'+mj+'"></script></head><body><main><h1>'+title+'</h1>'+body+'</main></body></html>';
}
(async()=>{
  const {unescapeLatex:formatCourse}=await import(pathToFileURL(path.join(front,'src/utils/scientificRenderer.js')).href);
  const browser=await chromium.launch({headless:true});
  const page=await browser.newPage();const checks=[];
  for(const slug of slugs){
    const raw=fs.readFileSync(path.join(root,'cours_'+slug+'_6e.txt'),'utf8');
    const title=raw.match(/^Titre:\s*(.+)$/m)[1];
    const body=images(formatCourse(raw.slice(raw.indexOf('<div'))),imageField(raw),path.join(root,'images'));
    const rawEx=fs.readFileSync(path.join(front,'exercices/6e','exercice_'+slug+'_6e.txt'),'utf8');
    const block=rawEx.split(/^===\s*$/m).filter(x=>x.trim()).at(-1);
    const enonce=block.split('Énoncé:')[1].split('Étapes:')[0];
    const corrige=block.split('Étapes:')[1].split('Solution:')[0];
    const exBody=images(format(enonce)+'<h2>Correction expliquée</h2>'+format(corrige),imageField(block),path.join(front,'exercices/6e/images'));
    for(const [type,content] of [['cours',body],['exercice',exBody]]){
      const file=path.join(out,slug+'-'+type+'.html');fs.writeFileSync(file,html(title,content));
      for(const width of [1100,390]){
        await page.setViewportSize({width,height:1000});
        await page.goto(pathToFileURL(file).href);
        await page.evaluate(()=>MathJax.startup.promise);
        const metrics=await page.evaluate(()=>({
          erreurs:document.querySelectorAll('mjx-merror,[data-mjx-error]').length,
          imagesManquantes:[...document.images].filter(im=>!im.complete||!im.naturalWidth).length,
          debordement:document.documentElement.scrollWidth>innerWidth+2,
          formules:document.querySelectorAll('mjx-container').length
        }));
        checks.push({slug,type,width,...metrics});
        await page.screenshot({path:path.join(out,slug+'-'+type+'-'+width+'.png')});
        if(type==='exercice'&&width===390){
          await page.getByRole('heading',{name:'Correction expliquée',exact:true}).scrollIntoViewIfNeeded();
          await page.screenshot({path:path.join(out,slug+'-correction-390.png')});
        }
      }
    }
  }
  await browser.close();
  fs.writeFileSync(path.join(root,'verifications/rendu.json'),JSON.stringify(checks,null,2));
  const errors=checks.filter(x=>x.erreurs||x.imagesManquantes||x.debordement);
  console.log(checks.length+' vues contrôlées, '+errors.length+' anomalie(s).');
  for(const e of errors)console.log(e);
  process.exit(errors.length?1:0);
})().catch(e=>{console.error(e);process.exit(1)});
