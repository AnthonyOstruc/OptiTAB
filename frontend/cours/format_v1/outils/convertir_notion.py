# -*- coding: utf-8 -*-
"""Convertit une notion exportée (dossier du chantier) au format OptiTAB v1.

    python convertir_notion.py <dossier_notion> [<dossier_notion> …]
    python convertir_notion.py --tout            # tout le chantier (rapport)
    --force : régénère même une notion verrouillée par etat.json (écrase les corrections !)

Entrée  : <dossier>/source_en_ligne/ (export lecture seule de la base)
Sortie  : <dossier>/cours_<id>.txt, fiche_<id>.txt, exercices.txt
Puis    : <dossier>/corrections.py s'il existe (corrections de fond rejouables),
          contrôle de syntaxe (valider_v1).
"""
import importlib.util
import io
import sys
from contextlib import redirect_stdout
from pathlib import Path

ICI = Path(__file__).resolve().parent
sys.path.insert(0, str(ICI))
import convertir_cours  # noqa: E402
import convertir_exercices  # noqa: E402
import valider_v1  # noqa: E402

CHANTIER = ICI.parent / "chantier"


def verrouillee(dossier):
    """Notion en relecture ou prête (etat.json) : ses fichiers finaux ne sont plus régénérés."""
    import json
    etat = Path(dossier) / "etat.json"
    if not etat.exists():
        return False
    return json.loads(etat.read_text(encoding="utf-8")).get("statut") in ("en_cours", "pret", "importe")


def convertir(dossier, force=False):
    dossier = Path(dossier)
    if verrouillee(dossier) and not force:
        return [f"IGNORÉE : etat.json indique une relecture en cours ou terminée (--force pour régénérer, ce qui ÉCRASE les corrections)"], []
    src = dossier / "source_en_ligne"
    rapport = []
    for f in sorted(src.glob("cours_*.txt")) + sorted(src.glob("fiche_*.txt")):
        for w in convertir_cours.convert_file(f, dossier / f.name):
            rapport.append(f"{f.name} : {w}")
    if (src / "exercices.txt").exists() and (src / "exercices.txt").read_text(encoding="utf-8").strip():
        _, avert = convertir_exercices.convert_file(src / "exercices.txt", dossier / "exercices.txt")
        rapport += [f"exercices : {w}" for w in avert]
    corr = dossier / "corrections.py"
    if corr.exists():
        spec = importlib.util.spec_from_file_location("corrections", corr)
        mod = importlib.util.module_from_spec(spec)
        buf = io.StringIO()
        with redirect_stdout(buf):
            spec.loader.exec_module(mod)
            if hasattr(mod, "appliquer_tout"):
                mod.appliquer_tout()
        rapport.append("corrections : " + buf.getvalue().strip())
    problemes = []
    for f in sorted(dossier.glob("cours_*.txt")) + sorted(dossier.glob("fiche_*.txt")) + [dossier / "exercices.txt"]:
        if f.exists():
            valider_v1.check_file(f, problemes)
    return rapport, problemes


if __name__ == "__main__":
    args = sys.argv[1:]
    force = "--force" in args
    args = [a for a in args if a != "--force"]
    dossiers = sorted(p.parent for p in CHANTIER.glob("*/*/source_en_ligne")) if args == ["--tout"] else [Path(a) for a in args]
    total_p = 0
    for d in dossiers:
        rapport, problemes = convertir(d, force)
        total_p += len(problemes)
        if rapport or problemes or len(dossiers) == 1:
            print(f"== {d.parent.name}/{d.name} : {len(problemes)} problème(s), {len(rapport)} avertissement(s)")
            for r in rapport:
                print("   ·", r)
            for p in problemes:
                print("   ✗", p)
    print(f"\n{len(dossiers)} notion(s) converties, {total_p} problème(s) de syntaxe")
