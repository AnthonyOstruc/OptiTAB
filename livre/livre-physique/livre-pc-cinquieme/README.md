# Physique-chimie 5e - aperçu OptiTAB

Maquette de validation : sommaire du livre et deux premiers chapitres complets.
Les deux copies du PDF d’aperçu ont été supprimées à la demande de l’utilisateur.
Le manuel complet les remplace : voir `README-complet.md` pour la version de
20 chapitres et ses sources. Les informations ci-dessous décrivent l’ancien aperçu.

## Contenu livré

- 43 pages A4, avec navigation interne et signets.
- Sommaire de 20 chapitres couvrant les quatre thèmes du cycle 4.
- Chapitre 1 : La matière et ses états.
- Chapitre 2 : Mesurer une masse et un volume.
- Cours illustrés, activités, synthèses, 30 exercices progressifs et 2 défis.
- Corrigés expliqués de tous les exercices et des deux défis.
- 25 insertions de schémas vectoriels, avec graduations calculées.
- Références et présentation des choix de progression.

Il s’agit d’un ouvrage indépendant fondé sur le programme français, sans
homologation ni validation institutionnelle revendiquée. Les énoncés, les
corrigés et les illustrations sont des créations originales. Les documents
officiels sont des références pédagogiques, pas une banque d’exercices recopiés.

## Références de programme

Texte applicable vérifié au 23 octobre 2026 : programme du cycle 4 publié au
BO n° 31 du 30 juillet 2020. Les attendus portent sur le cycle 4 ; l’ordre des
chapitres est une proposition pédagogique pour la 5e.

- [Programmes applicables - Éduscol](https://eduscol.education.gouv.fr/4362/enseigner-au-cycle-4)
- [Programme complet, physique-chimie pages 96 à 105](https://eduscol.education.fr/document/621/download)
- [Ressources de physique-chimie](https://eduscol.education.gouv.fr/5739/ressources-d-accompagnement-du-programme-de-physique-chimie-au-cycle-4)
- [Repères de progression](https://eduscol.education.fr/document/17731/download)

La grandeur quotient masse volumique et les lois formalisées des niveaux
suivants ne sont pas introduites dans ces deux chapitres. Le repère
« 1 mL d’eau a une masse d’environ 1 g » est limité à l’eau à température
ambiante et ne constitue pas une égalité entre unités.

## Sources et construction

- `contenu.py` : plan, exercices, corrigés et références.
- `schemas.py` : illustrations vectorielles paramétrées.
- `maquette.py` : gabarit A4, typographie, tableaux et liens.
- `construire.py` : génération en deux passes pour résoudre la pagination.
- `verifier.py` : contrôles et rendu intégral des pages.
- `livrer.py` : copie du PDF dont l’empreinte correspond aux contrôles et à la relecture.
- `recherche/` : copies de travail des textes de référence consultés.
- `build/qa/` : rendus, planches et traces de vérification.

Dépendances : Python, ReportLab, PyMuPDF, Pillow et Poppler. La maquette utilise
les polices Calibri et Segoe UI installées sous Windows ; elles sont incorporées
au PDF. Les logos proviennent des ressources OptiTAB déjà présentes dans le projet.

Depuis ce dossier :

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python construire.py
python verifier.py
```

Après toute nouvelle génération, inspecter les PNG et les planches, contrôler
les pages sensibles avec Poppler, puis actualiser
`build/qa/relecture-visuelle.json` avec l’empreinte effectivement relue.
`python livrer.py` refuse une livraison si l’empreinte n’a pas été relue.

Le PDF destiné à la validation se trouve dans
`../output/pdf/optitab-physique-chimie-5e-apercu.pdf`.

