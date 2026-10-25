"""Écrit tome-N/annexes/lexique.tex à partir des entrées \\mot{anglais}{phonétique}{français} des unités.

  python -X utf8 outils/lexique.py tome-1
"""
import pathlib
import re
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from latex_audio import vocabulaire  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent


def cle(anglais):
    t = re.sub(r"\\[a-zA-Z]+\s*", "", anglais).replace("{", "").replace("}", "")
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if c.isalnum() or c == " ")
    return t.strip()


def tri(anglais):
    """Clé de classement : l'article ne compte pas (« a baby » se range à B, comme dans un dictionnaire)."""
    return re.sub(r"^(a|an|the) ", "", cle(anglais))


def main():
    tome = RACINE / sys.argv[1]
    entrees = vocabulaire(tome)
    vues, lignes = set(), []
    for u, en, api, fr in sorted(entrees, key=lambda e: (tri(e[1]), cle(e[1]), e[0])):
        if cle(en) in vues:
            continue
        vues.add(cle(en))
        lignes.append((tri(en)[:1].upper(), r"\lexmot{%s}{%s}{%s}{%d}" % (en, api, fr, u)))
    out = ["%% Écrit par outils/lexique.py — ne pas modifier à la main",
           r"\begin{lexique}"]
    lettre = None
    for l, ligne in lignes:
        if l != lettre:
            out.append(r"\lexlettre{%s}" % l)
            lettre = l
        out.append(ligne)
    out.append(r"\end{lexique}")
    (tome / "annexes" / "lexique.tex").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(len(lignes), "entrées")


if __name__ == "__main__":
    main()
