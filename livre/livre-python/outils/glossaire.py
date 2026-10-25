"""Génère le glossaire du tome à partir des encadrés « Key term » des chapitres.

Usage : python -X utf8 outils/glossaire.py tome-1
Lit chaque \\begin{definition}{terme} ... \\end{definition} de tome-N/chapitres/chNN-*.tex
et écrit tome-N/annexes/glossaire.tex (ordre alphabétique, une lettre par rubrique).
"""
import re
import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent


def cle_tri(terme):
    t = re.sub(r"\\[a-zA-Z]+\{([^}]*)\}", r"\1", terme)
    return re.sub(r"[^a-z0-9 ]", "", t.lower())


def main():
    tome = RACINE / (sys.argv[1] if len(sys.argv) > 1 else "tome-1")
    entrees = {}
    for f in sorted((tome / "chapitres").glob("ch*.tex")):
        chapitre = int(re.match(r"ch(\d+)", f.stem).group(1))
        texte = f.read_text(encoding="utf-8").replace("\r\n", "\n")
        for m in re.finditer(r"\\begin\{definition\}\{([^}]*)\}\n(.*?)\\end\{definition\}", texte, re.S):
            terme = m.group(1).strip()
            if terme == "key term":
                continue
            definition = " ".join(m.group(2).split())
            cle = cle_tri(terme)
            if cle not in entrees:
                entrees[cle] = (terme, definition, chapitre)
    lignes = ["%% Écrit par outils/glossaire.py — ne pas modifier à la main",
              r"\annexe[glossaire]{Glossary}{The programmer's vocabulary, from A to Z}",
              r"\begin{glossaire}"]
    lettre = None
    for cle in sorted(entrees):
        terme, definition, chapitre = entrees[cle]
        initiale = cle[0].upper()
        if initiale != lettre:
            lettre = initiale
            lignes.append(r"\glolettre{" + lettre + "}")
        lignes.append(r"\gloterme{" + terme + "}{" + definition + "}{" + str(chapitre) + "}")
    lignes.append(r"\end{glossaire}")
    (tome / "annexes" / "glossaire.tex").write_text("\n".join(lignes) + "\n", encoding="utf-8")
    print(len(entrees), "termes dans", tome / "annexes" / "glossaire.tex")


if __name__ == "__main__":
    main()
