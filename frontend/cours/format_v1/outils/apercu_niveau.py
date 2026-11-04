# -*- coding: utf-8 -*-
"""Aperçu d'un niveau entier, à faire valider par le propriétaire (publication en artifact).

    python apercu_niveau.py <niveau> <dossier_sortie> ["Titre du niveau"] [--tous]

Produit <sortie>/index.html (page d'accueil, au format artifact : sans
doctype ni head) et <sortie>/notions/n<id>.html (aperçu complet de chaque
notion au statut « pret », ou de toutes avec --tous), puis affiche la
commande de publication (Artifact : file_path=index.html, files=notions/…).
"""
import html
import json
import re
import subprocess
import sys
from pathlib import Path

ICI = Path(__file__).resolve().parent
CHANTIER = ICI.parent / "chantier"


def statut(d):
    e = d / "etat.json"
    return json.loads(e.read_text(encoding="utf-8")).get("statut", "a_faire") if e.exists() else "a_faire"


def infos(d):
    meta = json.loads((d / "source_en_ligne" / "meta.json").read_text(encoding="utf-8"))
    corr_p = d / "figures" / "correspondance.json"
    corr = json.loads(corr_p.read_text(encoding="utf-8")) if corr_p.exists() else {}
    fichiers = {v["fichier"] if isinstance(v, dict) else v
                for g in corr.values() for m in g.values() for v in m.values()}
    return meta, len(fichiers)


def page_index(titre, lignes):
    cartes = []
    for l in lignes:
        lien = f'notions/n{l["id"]}.html'
        puces = [f'{l["ex"]} exercice{"s" if l["ex"] > 1 else ""}'] if l["ex"] else []
        if l["fig"]:
            puces.append(f'{l["fig"]} figure{"s" if l["fig"] > 1 else ""} neuve{"s" if l["fig"] > 1 else ""}')
        cartes.append(
            f'<li class="ch"><a class="ch-a" href="{lien}">'
            f'<span class="ch-t">{html.escape(l["titre"])}</span>'
            f'<span class="ch-m">Cours · Fiche{" · " if puces else ""}{" · ".join(puces)}</span>'
            f'</a></li>')
    total_ex = sum(l["ex"] for l in lignes)
    total_fig = sum(l["fig"] for l in lignes)
    return f"""<title>{html.escape(titre)} OptiTAB</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Montserrat:wght@500;600;700&display=swap">
<style>
/* Mise en page : en-tête sobre aux couleurs du logo, puis liste des chapitres (une ligne par chapitre, lien vers son aperçu). */
:root {{
  --page: #f4f6fb; --card: #ffffff; --line: #e1e7f2; --ink: #1c2130; --muted: #5f6880;
  --navy: #1b3c8e; --green: #3b8544; --hover: #eef2fb;
  --display: Montserrat, "Segoe UI", system-ui, sans-serif;
  --text: "Segoe UI", system-ui, -apple-system, Roboto, sans-serif;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --page: #11151f; --card: #191e2b; --line: #2a3142; --ink: #e8ebf3; --muted: #9aa3b8;
  --navy: #8fb0ff; --green: #7cc77f; --hover: #202740; color-scheme: dark; }} }}
:root[data-theme="dark"] {{
  --page: #11151f; --card: #191e2b; --line: #2a3142; --ink: #e8ebf3; --muted: #9aa3b8;
  --navy: #8fb0ff; --green: #7cc77f; --hover: #202740; color-scheme: dark; }}
body {{ background: var(--page); color: var(--ink); font-family: var(--text); font-size: 15px; line-height: 1.5; }}
.wrap {{ max-width: 760px; margin: 0 auto; padding-block: 28px 56px;
  padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px));
  display: grid; gap: 22px; }}
.kicker {{ font: 700 11px/1.4 var(--display); letter-spacing: .12em; text-transform: uppercase; color: var(--green); }}
h1 {{ font: 700 clamp(24px, 6vw, 32px)/1.2 var(--display); color: var(--navy); margin: 4px 0 8px; text-wrap: balance; }}
.intro {{ color: var(--muted); max-width: 62ch; margin: 0; }}
.chiffres {{ font-variant-numeric: tabular-nums; color: var(--ink); font-weight: 600; }}
ol {{ list-style: none; margin: 0; padding: 0; display: grid; gap: 10px; }}
.ch-a {{ display: grid; gap: 4px; padding: 14px 16px; background: var(--card); border: 1px solid var(--line);
  border-radius: 12px; text-decoration: none; color: inherit; }}
.ch-a:hover, .ch-a:focus-visible {{ background: var(--hover); border-color: var(--navy); outline: none; }}
.ch-t {{ font: 600 16px/1.35 var(--display); color: var(--navy); text-wrap: balance; }}
.ch-m {{ font-size: 13px; color: var(--muted); font-variant-numeric: tabular-nums; }}
.note {{ font-size: 13px; color: var(--muted); margin: 0; }}
</style>
<main class="wrap">
  <header>
    <div class="kicker">Aperçu à valider · nouveau format</div>
    <h1>{html.escape(titre)}</h1>
    <p class="intro">Chaque chapitre s'ouvre tel qu'il apparaîtra aux élèves : cours, fiche de synthèse et exercices avec leurs étapes et solutions.
    <span class="chiffres">{len(lignes)} chapitres · {total_ex} exercices · {total_fig} figures refaites ou ajoutées.</span></p>
  </header>
  <ol>
    {"".join(cartes)}
  </ol>
  <p class="note">Aperçu hors ligne : le site actuel n'est pas modifié tant que ce niveau n'est pas validé.</p>
</main>
"""


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    niveau, sortie = args[0], Path(args[1])
    titre = args[2] if len(args) > 2 else niveau.capitalize()
    tous = "--tous" in sys.argv
    (sortie / "notions").mkdir(parents=True, exist_ok=True)
    lignes = []
    for d in sorted(p.parent for p in (CHANTIER / niveau).glob("*/source_en_ligne")):
        if not tous and statut(d) not in ("pret", "importe"):
            print(f"   (pas prête : {statut(d)}) {d.name}")
            continue
        meta, n_fig = infos(d)
        out = sortie / "notions" / f"n{meta['notion']}.html"
        r = subprocess.run(["node", str(ICI / "apercu_notion.mjs"), str(d), str(out), "--retour", "../index.html"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace", stdin=subprocess.DEVNULL)
        if r.returncode != 0:
            print(f"✗ {d.name} : {r.stderr[-300:]}")
            continue
        taille = out.stat().st_size / 1e6
        print(f"✓ {d.name} : {taille:.1f} Mo")
        if taille > 15.5:
            print(f"  ⚠ page trop lourde pour une publication ({taille:.1f} Mo > 16 Mo)")
        lignes.append({"id": meta["notion"], "titre": meta["titre"], "ex": len(meta["exercices"]), "fig": n_fig,
                       "ordre": (meta.get("theme") or 0, int(re.match(r"\d+", d.name).group()))})
    lignes.sort(key=lambda l: l["ordre"])
    (sortie / "index.html").write_text(page_index(titre, lignes), encoding="utf-8")
    total = sum(f.stat().st_size for f in (sortie / "notions").glob("*.html")) / 1e6
    print(f"{len(lignes)} chapitre(s), {total:.1f} Mo au total → {sortie / 'index.html'}")


if __name__ == "__main__":
    main()
