# Physique-Chimie de Terminale sur le site (demande du 2026-11-03, soir)

Demande du propriétaire : ajouter la physique-chimie (« essentielle ») au site, en
commençant par la Terminale ; MÊMES RÈGLES que les maths (schémas importants, tout
ce qu'il faut, interface propre, professionnelle, épurée, impeccable). D'abord la
liste des chapitres, puis UN premier chapitre pour validation par le propriétaire.

## En base (PROD) — tout INACTIF tant que le propriétaire n'a pas validé
`outils/creer_pc_terminale.py` : matière 5 « Physique-Chimie » (inactive, pas sur
l'accueil), contexte 55 (Terminale), thèmes 130–134, notions 432–458 (inactives),
cours + fiche vides au format v1 pour chacune. Chantier : `chantier/terminale-pc/`
(exporter.py : contexte 55 → `terminale-pc`). Activation (matière, contexte,
thèmes, notions) seulement après validation.

Source : le livre OptiTAB `livre/livre-physique/livre-pc-terminale/` (27 chapitres,
programme officiel de spécialité, figures TikZ, exercices et corrigés) — matériau
de départ, à adapter au site (jamais copié tel quel : format v1, téléphone).

| Thème | Notions |
|---|---|
| 130 Constitution et transformations de la matière | 432 Transformations acide-base · 433 Méthodes physiques d'analyse · 434 Titrages pH-métriques et conductimétriques · 435 Cinétique chimique · 436 Mécanismes réactionnels · 437 Décroissance radioactive · 438 Équilibre chimique et sens d'évolution · 439 Piles et oxydoréduction · 440 Force des acides et des bases · 441 Électrolyse et stockage de l'énergie · 442 Structure des molécules organiques · 443 Stratégies de synthèse organique |
| 131 Mouvement et interactions | 444 Décrire un mouvement · 445 Deuxième loi de Newton · 446 Mouvement dans un champ uniforme · 447 Mouvement dans un champ de gravitation · 448 Écoulement des fluides |
| 132 L'énergie : conversions et transferts | 449 Modèle du gaz parfait · 450 Premier principe de la thermodynamique · 451 Transferts thermiques et bilans |
| 133 Ondes et signaux | 452 Intensité sonore et atténuation · 453 Diffraction et interférences · 454 Effet Doppler · 455 Lunette astronomique · 456 Photons et effet photoélectrique · 457 Circuit RC et capteurs capacitifs |
| 134 Mesure et incertitudes | 458 Mesures et incertitudes |

## Consigne de chapitre (à lire par chaque agent)
Les règles de `GUIDE_CHANTIER.md` et de `FILE_4E.md` (« Consigne de lot ») s'appliquent,
avec ces adaptations à la physique-chimie :
1. **Programme** : spécialité Physique-Chimie de Terminale (BO 2019, en vigueur),
   capacités exigibles du chapitre toutes couvertes ; vocabulaire officiel.
2. **Cours** façon manuel (définitions, lois, méthodes, exemples, erreurs fréquentes,
   « À retenir »), **fiche** dense. Titres = intitulé de la notion.
3. **Exercices** : 12 à 15, COMPLETS et PÉDAGOGIQUES, progression Découverte →
   Entraînement → Problème → Type bac (exercices ajoutés en `Id: nouveau-N`).
   Corrigé : méthode, étapes, résultat encadré avec **unité et chiffres
   significatifs**, erreur fréquente / à retenir. Titres « Type - Sujet ».
4. **Écriture** : formules chimiques et équations avec mhchem `$\ce{…}$`
   (`$\ce{CH3COOH + H2O <=> CH3COO- + H3O+}$`), unités avec espace insécable,
   grandeurs en italique, vecteurs avec `\vec`. Schémas de Lewis, montages,
   courbes, chronophotographies : en FIGURES (pas en texte).
5. **Figures** : style des livres (`figures_livre.py`, on peut reprendre/adapter le TikZ
   du livre : `livre/livre-physique/livre-pc-terminale/figures`, `chapitres/`), partout
   où elles aident : cours, fiche, énoncé (sans la réponse) et corrigé (complété en vert).
   Jamais de texte sur un trait, lisibles sur téléphone.
6. **Calculs** : tous vérifiés avec sympy (`verif_*.py`), y compris unités et arrondis.
7. **Fin** : `verifier_notion.py --navigateur` = 0 problème, captures téléphone
   regardées, `etat.json` = « pret », RAPPORT.md.
Interdits : aucune écriture en base, aucun git, seulement son dossier ; respecter
`outils/.verrous` ; fichiers temporaires préfixés par l'id de la notion.

## Journal
- 2026-11-03 ~23 h : squelette créé en base (inactif) ; MathJax du site + aperçus :
  extension mhchem ajoutée (index.html, apercu.mjs, apercu_notion.mjs). Chapitre 432
  lancé (pilote, pour validation du propriétaire).
