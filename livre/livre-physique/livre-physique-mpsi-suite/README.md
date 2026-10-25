# OptiTAB Physique MPSI : suite du manuel

## Livraison actuelle : un seul livre

Le volume commun est désormais dans `../livre-physique-mpsi-integral/`.
Il réunit les chapitres 01 à 10, avec couverture, liminaires, sommaire, pagination
et navigation communs. Les fascicules ci-dessous décrivent l'étape précédente.

Nouveaux chapitres : 06 résonance ; 07 filtrage ; 08 propagation ;
09 interférences ; 10 ondes stationnaires et corde, explicitement présenté
comme approfondissement de la rubrique 1.6, sans équation d'onde.

Pour reconstruire la livraison actuelle :

1. `python construire.py 6 7 8 9 10`
2. `python assembler_livre.py`
3. `python ../livre-physique-mpsi-integral/compiler.py`
4. `python verifier_livre.py --rendu`
5. Relire toutes les images, consigner la relecture dans le rapport, puis
   `python livrer_livre.py`.

La publication refuse un rendu non relu, un écart d'empreinte, un débordement
ou un lien interne invalide. Elle publie uniquement le PDF commun.

## Fabrication initiale des chapitres 02 à 05

Quatre fascicules dans la charte validée du premier chapitre :

- 02 : Signaux électriques dans l’ARQS (programme 1.2).
- 03 : Circuits linéaires du premier ordre (programme 1.3).
- 04 : L’oscillateur harmonique (début du programme 1.4).
- 05 : Oscillations libres amorties, incluant la réponse à un échelon (partie transitoire de 1.4).

Chaque chapitre comporte le plan annuel, une page de navigation, l’avant-propos,
le diagnostic, un cours développé, 24 exercices et leurs corrigés, 3 défis avec
indications et corrigés, un TP, une activité numérique, un DM et un DS de deux
heures avec barèmes. Les parcours sur des sujets authentiques identifient le
document, la date, les pages et les questions ; les énoncés OptiTAB sont originaux.

Les capacités sur les impédances complexes et la résonance sont réservées au
chapitre 06. Le chapitre 01 et le livre de mathématiques ne sont pas modifiés.

Fabrication avec Python 3, LuaLaTeX (MiKTeX), les polices Libertinus et Montserrat,
Poppler, NumPy, PyMuPDF et Pillow :

1. `python construire.py`
2. Exécuter `python compiler.py` dans chaque dossier de chapitre.
3. `python verifier_suite.py`
4. Inspecter les pages de `chapitre-XX/build/qa/` ; corriger et recommencer si nécessaire.
5. Marquer les pages réellement relues dans le rapport, puis `python livrer_suite.py`.

Les scripts de vérification recalculent les résultats, contrôlent les conditions
initiales, les résidus différentiels et les bilans d’énergie, puis vérifient la
pagination, les liens et la géométrie du texte. La relecture des images complète
ces contrôles. Les erreurs de compilation bloquent la livraison.

Les sources du programme et des vrais sujets sont enregistrées dans
`recherche/sources.json` avec empreintes SHA-256. Les PDF externes ne sont pas
incorporés dans l’archive du livre. La base de charte nécessaire à la reconstruction
est incluse à côté du dossier de la suite dans l’archive de sources.
