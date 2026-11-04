# -*- coding: utf-8 -*-
"""Construit le cours et la fiche remis en forme d'un chapitre de lycée.

Usage : python outils/construire.py <slug> [--journal]
Entrées : source/cours_<id>.html (copie de la base), specs/<slug>.py, images/*.png
Sorties : sortie/<slug>_cours.html, sortie/<slug>_fiche.html
"""
import sys
from collections import Counter

sys.stdout.reconfigure(encoding="utf-8")

from lycee_commun import (SOURCE, SORTIE, IMAGES, charger_spec, harmoniser, inserer, remplacer_entete, ajouter_fin,
                          max_image, verifier)


def figure(n):
    return f"[IMAGE_{n}]"


def construire(slug, journal=False):
    sp = charger_spec(slug)
    html = (SOURCE / f"cours_{sp.COURS_ID}.html").read_text(encoding="utf-8")
    texte_avant = len(html)
    log = []
    html = harmoniser(html, log, getattr(sp, "ROLES", None))
    html = remplacer_entete(html, sp.ENTETE)
    n0 = max_image(html)
    ajouts = []
    nouvelles = []
    for k, fig in enumerate(sp.FIGURES, n0 + 1):
        assert (IMAGES / fig["fichier"]).exists(), fig["fichier"]
        ajouts.append((fig["ancre"], fig.get("mode", "apres_bloc"), figure(k)))
        nouvelles.append((k, fig["fichier"]))
    ajouts += [(a["ancre"], a.get("mode", "apres_bloc"), a["html"].strip()) for a in sp.AJOUTS]
    html = inserer(html, ajouts)
    html = ajouter_fin(html, sp.ESSENTIEL)
    ok = verifier(html, f"{slug} (cours)")
    (SORTIE / f"{slug}_cours.html").write_text(html, encoding="utf-8")
    fiche = sp.FICHE.strip()
    for k, f in enumerate(sp.FICHE_IMAGES, 1):
        assert (IMAGES / f).exists(), f
        assert f"[IMAGE_{k}]" in fiche, f"fiche : [IMAGE_{k}] non placé"
    ok &= verifier(fiche, f"{slug} (fiche)")
    (SORTIE / f"{slug}_fiche.html").write_text(fiche, encoding="utf-8")
    roles = Counter(r for r, _ in log)
    print(f"[{slug}] cours {texte_avant} -> {len(html)} car. ; encadrés {dict(roles)} ; "
          f"figures ajoutées {[n for n, _ in nouvelles]} ; fiche {len(fiche)} car., {len(sp.FICHE_IMAGES)} image(s)")
    if journal:
        for r, t in log:
            print(f"   {r:5s} {t}")
    return ok


if __name__ == "__main__":
    ok = construire(sys.argv[1], "--journal" in sys.argv)
    sys.exit(0 if ok else 1)
