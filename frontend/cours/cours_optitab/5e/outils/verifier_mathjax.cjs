// Vérifie chaque formule $...$ des fichiers donnés avec MathJax 3 (même moteur que le site).
// Usage : node verifier_mathjax.js fichier1.txt [fichier2.txt ...]
const path = require('path');
const fs = require('fs');
const MJ = require(path.join(__dirname, '../../../../node_modules/mathjax'));
MJ.init({
  loader: {load: ['input/tex', 'output/svg', '[tex]/textmacros']},
  tex: {packages: {'[-]': ['noundefined'], '[+]': ['textmacros']}, formatError: (jax, err) => { throw err; }}
}).then((MathJax) => {
  let nerr = 0, nf = 0;
  for (const f of process.argv.slice(2)) {
    const txt = fs.readFileSync(f, 'utf8');
    const re = /(^|[^$])\$(?!\$)([^$\n]*?)\$(?!\$)/g;
    let m;
    while ((m = re.exec(txt)) !== null) {
      const tex = m[2];
      if (tex === '\\') continue;
      nf++;
      try {
        MathJax.tex2svg(tex, {display: false});
      } catch (e) {
        nerr++;
        const line = txt.slice(0, m.index).split('\n').length;
        console.log(`${path.basename(f)}:${line} : ${e.message} -> ${tex.slice(0, 120)}`);
      }
    }
  }
  console.log(`${nf} formules vérifiées, ${nerr} erreur(s).`);
  const crypto = require('crypto');
  const hashes = Object.fromEntries(process.argv.slice(2).map(f => [path.relative(path.resolve(__dirname,'../../../..'),f), crypto.createHash('sha256').update(fs.readFileSync(f)).digest('hex')]));
  fs.writeFileSync(path.join(__dirname,'../verifications/mathjax.json'), JSON.stringify({formules:nf,erreurs:nerr,empreintes:hashes},null,2));
  process.exit(nerr ? 1 : 0);
}).catch((e) => { console.error(e); process.exit(2); });
