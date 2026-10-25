# Physique-chimie 5e - manuel complet OptiTAB

Le manuel complet prolonge la maquette de deux chapitres validée par l’utilisateur.
Les deux copies du PDF d’aperçu ont été supprimées à la demande de l’utilisateur ;
le manuel complet les remplace.

## Maquette actuelle : charte du livre de Terminale

À la demande de l’utilisateur, la version livrée est désormais composée avec
LuaLaTeX et les styles du livre `../livre-pc-terminale/`. Le livre de Terminale
reste intact. Les adaptations propres au collège figurent dans
`cinquieme-charte.tex` : corps de texte de 12 points, ouvertures sur deux lignes,
repères de navigation et décors des quatre thèmes. Les schémas originaux sont
insérés comme PDF vectoriels. Les contenus pédagogiques restent dans les
fichiers Python décrits plus bas.
Les sauts de page de `equilibrage-template.json` ont été déterminés à
partir des hauteurs mesurées par LuaLaTeX pour équilibrer les fins de séries.

Reconstruction de la version actuelle, depuis ce dossier :

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python construire_template_terminale.py
python verifier_template_terminale.py
```

La compilation exige LuaLaTeX, les polices Libertinus et Montserrat et les
paquets utilisés par la charte de Terminale. Les sources générées et le PDF
sont dans `template-terminale/`. Les journaux, contrôles, pages PNG, planches
de relecture et épreuves Poppler sont dans `template-terminale/build/`.
Le contrôle compare les textes des énoncés, corrigés, cours et annexes au PDF,
vérifie les destinations et contrôle les limites des schémas.

Après relecture de toutes les planches et des épreuves détaillées, renseigner
`template-terminale/build/qa/relecture-visuelle.json` avec l’empreinte exacte
du PDF relu, puis exécuter `python livrer_template_terminale.py`.

Les commandes ReportLab ci-dessous permettent de retrouver l’ancienne
maquette. Elles ne constituent plus le circuit de livraison de la version
actuelle.

## Organisation éditoriale

Révision livrée le 24 octobre 2026 : **346 pages**, 194 figures vectorielles
distinctes et 276 insertions. Les exercices concernés comportent leur document
local : 61 énoncés et 85 corrigés illustrés, avec 27 explications de méthode
supplémentaires. Neuf corrigés de défis et treize missions de bilan reçoivent
également des constructions ou modèles complémentaires. Les 763 contrôles
du PDF et les 471 contrôles de révision passent sans échec ; 1 993 contenus
sont comparés aux sources. Les 29 planches finales, les six planches de
nouveaux schémas et 18 pages critiques rendues avec Poppler ont été inspectées.
Les bilans conservent toutes leurs questions et les encadrés de reprise restent
avec leur dernière correction. Les fiches tiennent sans réduction automatique.
Le PDF classé et sa copie du Bureau ont la même empreinte.

20 chapitres, 300 exercices progressifs, 20 défis et 4 bilans de thème.
Les 20 missions des bilans s’ajoutent aux 300 exercices des chapitres.
Tous les exercices, défis, activités et bilans possèdent des éléments de réponse.
Les fiches méthode et les 80 entrées du lexique facilitent l’utilisation autonome.

1. Organisation et transformations de la matière : chapitres 1 à 8.
2. Mouvement et interactions : chapitres 9 à 11.
3. Énergie, transferts et conversions : chapitres 12 à 16.
4. Signaux pour observer et communiquer : chapitres 17 à 20.

Les trois niveaux sont « Je démarre », « Je m’entraîne » et « Je raisonne ».
Les numéros d’exercices et de corrigés se répondent par des liens internes.
Le sommaire, les repères, les bilans et le lexique sont également navigables.
Les schémas sont vectoriels ; les graduations et courbes reposent sur les
valeurs annoncées dans les énoncés.

Le texte de référence est le programme de cycle 4 du BO n° 31 du 30 juillet
2020, confirmé par Éduscol pour 2026-2027 au 23 octobre 2026. Ce texte fixe les
attendus du cycle : le manuel propose une progression de 5e, avec une approche
expérimentale et descriptive pour les notions formalisées plus tard.
Le manuel est indépendant et ne revendique pas d’homologation ministérielle.

Les textes, exercices, corrigés et schémas sont originaux. Les références
officielles guident le programme et les démarches, sans reprise de banques
d’exercices éditoriaux. Les séries de mesures fictives sont identifiées comme
données pédagogiques ou données d’entraînement.

## Fichiers sources

- `construire_complet.py` : assemblage et pagination en deux passes.
- `chapitres_matiere.py` : chapitres 3 à 8.
- `chapitres_mouvement.py` : chapitres 9 à 11.
- `chapitres_energie.py` : chapitres 12 à 16.
- `chapitres_signaux.py` : chapitres 17 à 20.
- `annexes_completes.py` : quatre bilans, méthodes et lexique.
- `programme_complet.py` : structure des données et références complémentaires.
- `schemas_complets.py` : dessins supplémentaires.
- `contenu.py`, `construire.py`, `maquette.py`, `schemas.py` : socle de la maquette initiale.
- `verifier_complet.py` : contrôles et rendu intégral.
- `livrer_complet.py` : livraison conditionnée par les contrôles et la relecture.

Construction depuis ce dossier :

```powershell
$env:PYTHONIOENCODING = 'utf-8'
python construire_complet.py
python verifier_complet.py
```

Les intermédiaires sont dans `build-complet/`. Les pages PNG, planches,
agrandissements des schémas et contrôles sont dans `build-complet/qa/`.
Toute modification du PDF exige un nouveau contrôle et une actualisation de
la relecture visuelle avec l’empreinte exacte du fichier effectivement inspecté.

Après relecture, `python livrer_complet.py` copie uniquement ce PDF vers
`../output/pdf/France/Physique-chimie/OptiTAB - Physique-chimie - Cinquième (5e) - Manuel complet.pdf` et crée son relevé de
vérification dans `../output/verification/`.

## Points scientifiques surveillés

- Masse conservée dans un système fermé ; volume non nécessairement conservé.
- Soluté présent après dissolution ; saturation et durée de dissolution distinctes.
- Filtration sans garantie de potabilité ni retrait des espèces dissoutes.
- Test positif de présence sans conclusion de pureté.
- Vitesse moyenne sur distance et durée du même trajet, pauses comprises si demandées.
- Interactions décrites sans formalisme des forces de fin de cycle.
- Branches électriques, chemins de retour et court-circuit distingués.
- Courant, énergie et sens de rotation du moteur distingués.
- W, Wh et kWh employés pour les bonnes grandeurs.
- Lumière entrant dans l’œil ; ombres construites avec rayons limites.
- Son transmis dans un milieu matériel ; écho compté en aller-retour.
- Signal physique et information interprétée distingués ; code et synchronisation précisés.

