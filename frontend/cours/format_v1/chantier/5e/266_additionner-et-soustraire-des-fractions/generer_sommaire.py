"""Sommaire local des vingt aperçus de cinquième."""
from pathlib import Path
import json
from html import escape
D=Path(__file__).resolve().parent
bilan=json.loads((D/'bilan_5e.json').read_text(encoding='utf-8'))
cards='\n'.join(f'<a class="chapitre" href="../{escape(n["dossier"])}/apercu.html"><span>Chapitre {i:02d}</span><strong>{escape(n["titre"])}</strong><small>Cours · Fiche · 21 exercices →</small></a>' for i,n in enumerate(bilan['detail'],1))
html='''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>OptiTAB — Aperçus de 5e</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#f4f6fb;color:#1c2130;font:16px/1.5 "Segoe UI",sans-serif}main{max-width:1120px;margin:auto;padding:40px 24px 64px}.marque{color:#3b8544;letter-spacing:.12em;font-size:12px;font-weight:700}h1{font-size:clamp(28px,5vw,42px);line-height:1.2;color:#1b3c8e;margin:10px 0 12px}.intro{color:#606a7c;margin-bottom:30px}.grille{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px}.chapitre{display:flex;flex-direction:column;gap:12px;padding:22px;background:white;border:1px solid #dce3ef;border-radius:14px;color:inherit;text-decoration:none;box-shadow:0 4px 15px #1b3c8e05}.chapitre:hover,.chapitre:focus-visible{border-color:#1b3c8e;box-shadow:0 5px 20px #1b3c8e12}.chapitre span{color:#3b8544;font-size:12px;font-weight:700}.chapitre strong{font-size:18px;color:#1b3c8e}.chapitre small{margin-top:auto;color:#606a7c}footer{margin-top:28px;color:#6b7385;font-size:14px}
</style></head><body><main><div class="marque">OPTITAB · PRÉVISUALISATION LOCALE</div><h1>Mathématiques — 5e</h1><p class="intro">Choisis un chapitre, puis utilise les onglets Cours, Fiche de synthèse et Exercices. Dans chaque exercice, les étapes et la solution sont accessibles séparément.</p><div class="grille">'''+cards+'''</div><footer>Révision du 30 octobre 2026 · 20 cours · 20 fiches · 420 exercices. Version préparée sur cet ordinateur, en attente d’import sur le site.</footer></main></body></html>'''
(D/'sommaire_5e.html').write_text(html,encoding='utf-8')
print(D/'sommaire_5e.html')
