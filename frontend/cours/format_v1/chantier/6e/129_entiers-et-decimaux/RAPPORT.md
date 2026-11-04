# Notion 129 (6e) : Entiers et décimaux

## Refonte 10 exercices 2026-11-04

**État : prêt** (refonte-6e-129, 2026-11-04). Référence : `source_en_ligne/` (ré-export du 04/11). 10 exercices gardés (Id inchangés, tous réécrits de zéro), 11 retirés (`exercices_retires.txt`), aucun `nouveau-N`, aucune ligne `Id:` modifiée. Sauvegarde des fichiers finaux et figures d'avant la refonte : `sauvegardes/avant_refonte_20261104/`.

Programme vérifié : cycle 3, arrêté du 10 avril 2025 (BO n° 16 du 17 avril 2025), en vigueur en 6e. Nouveautés de 6e intégrées : vocabulaire « nombre mixte », « un entier est un décimal », « un pourcentage est un nombre », conversions de mesures par ×10, ×100, ×1 000 (pas de tableau de conversion). Comparaison, encadrement, arrondi → notion 130 ; 1/3 non décimal → notion 132 (simple renvoi dans le cours).

### Cours et fiche
- **Cours 132 réécrit façon manuel** (titre inchangé) : objectifs, prérequis ; I. grands nombres (chiffres, rangs, classes, tableau, lecture, liens ×10 / ×1 000, écrire en chiffres, règles d'écriture en lettres — orthographe recommandée : traits d'union, million/milliard noms, mille invariable, accords de vingt et cent —, décomposition) ; II. chiffre des… / nombre de… (figure, erreur fréquente) ; III. dixièmes, centièmes, millièmes, fractions décimales ; IV. nombres décimaux (virgule, partie entière / partie décimale, valeur de chaque chiffre en tableau natif, un entier est décimal, pourcentage, erreurs) ; V. passer d'une écriture à l'autre (fraction décimale, nombre mixte, décomposition, trois méthodes, droite graduée et loupe, rôle des zéros) ; VI. mesures ; « À retenir ».
- **Fiche 198 refaite** : grands nombres, unités de numération, tableau des quatre écritures, 5 erreurs classiques ; 2 figures.
- Exemples du cours ($4\,207\,350\,018$ ; $63{,}507$ ; $2{,}47$…) tous différents de ceux des exercices. Aucune mention du brevet.

### Exercices gardés (10)
| Id | Titre | Capacités |
|---|---|---|
| 3167 | Découverte - Lire et écrire les grands nombres | tableau de numération, lettres ↔ chiffres, classes vides, accords |
| 3170 | Découverte - Dixièmes et centièmes en images | bande de 10, carrés de 100, fraction décimale, virgule, nombre mixte, 0,6 / 0,06 |
| 3169 | Découverte - Fractions décimales et écriture à virgule | fraction ↔ virgule (12 conversions), 0,5 = 5/10 = 50/100 = 500/1 000, erreur de Tom |
| 3168 | Entraînement - Partie entière et valeur des chiffres | tableau décimal, partie entière / décimale, valeur des chiffres, décomposition, zéros intérieurs |
| 3171 | Entraînement - Le chiffre des… ou le nombre de… ? | entiers et décimaux, erreur de Léa (6,25 : 62 dixièmes, 625 centièmes) |
| 3172 | Entraînement - Plusieurs écritures d'un même nombre | écritures de 3,4, fraction ↔ nombre mixte, zéros inutiles, entier décimal, 35 % |
| 3177 | Problème - Lire des longueurs sur une règle graduée | droite au dixième + loupe au centième, fractions décimales, nombres mixtes, mm |
| 3173 | Problème - Les mesures du goûter | L/mL, kg/g, m/cm, erreur 2,75 kg, canette, quantité manquante |
| 3174 | Problème - Des grands nombres pour décrire le monde | distances (150 millions, 4,5 milliards de km), population (ONU, INSEE 2025), vis en boîtes et cartons |
| 3181 | Synthèse - Enquête sur deux nombres mystères | partie A grand nombre (chiffres, lettres, nombre de…) ; partie B 3,408 (toutes les écritures, centièmes, zéro intérieur) |

Progression : 3 Découverte, 3 Entraînement, 3 Problème, 1 Synthèse. Chaque corrigé : méthode, étapes détaillées, résultat encadré, erreur fréquente ou « À retenir » ; `Solution:` courte. Couverture détaillée : `COUVERTURE.md`.

### Exercices retirés (11)
3175, 3176, 3178, 3179, 3180, 3182, 3183, 3184, 3185, 3186, 3187 : les 21 exercices en ligne étaient 7 énoncés répétés en « Parcours 1, 2, 3 » (mêmes questions, autres valeurs). Le thème « Décimal ou non décimal ? » (1/3) relève de la notion 132.

### Figures (16 neuves, style livre, `figures/figures.py`)
- L'ancienne image du cours (deux carrés quadrillés) est remplacée ; il n'y avait aucune autre image (0 conservée).
- Cours (5) : tableau de numération des entiers, chiffre / nombre de millions (accolade et flèche), unité partagée en 10 et en 100, tableau décimal (partie entière | partie décimale, en-têtes verticaux), droite graduée au dixième avec loupe au centième. Fiche (2) : unités, tableau décimal.
- Exercices : 3167 tableau vide / rempli en vert ; 3170 bandes et carrés énoncé / corrigé en vert ; 3168 tableau décimal vide / rempli ; 3171 accolade et flèche en vert ; 3177 règle + loupe énoncé / corrigé (valeurs et points placés en vert) ; 3181 deux tableaux remplis en vert.
- `figures_livre.py` : 0 chevauchement texte / trait, aucune tolérance, toutes ≤ 900 px. Après la 1re passe téléphone : tableaux rétrécis (en-têtes verticaux), légende des carrés sous la figure, droites resserrées.

### Contrôles
- `verif_129.py` : **196 contrôles** sympy en rationnels exacts (cours, fiche, chaque question, figures cohérentes avec les textes, écriture en lettres recalculée par un générateur aux règles de l'orthographe recommandée, structure des corrigés, absence de « brevet » et de caractères de contrôle) — tout juste.
- `verifier_notion.py --navigateur` : **OK, 0 problème** (notes : 10 titres changés, 11 exercices retirés volontairement). `controle_apercu.mjs` avec captures (`captures_refonte/`) : « Aucun problème détecté ».
- Captures téléphone regardées en deux passes groupées (cours, fiche, 10 exercices). Corrigé après la 1re passe : formules coupées ou réduites (classes, unités, décomposition, écritures de 63,507, chaînes des exercices 3172, 3173, 3174, 3181) découpées en lignes alignées ou en listes ; question 1 de 3172 en liste lettrée.

### Pour l'orchestrateur
- Après `publier_lot.ps1 6e 129`, lancer `retirer_exercices.py` (11 Id).
- Le dossier contient aussi des scripts et journaux de l'ancienne coordination 6e (publier_6e.py, captures_6e/…) : non modifiés.

---

## Historique : 1er novembre 2026
Notion 129 — prête le 1er novembre 2026. Cours réécrit, fiche compacte, 21 exercices (sept familles × trois parcours), 1 figure. Sauvegardes dans `sauvegardes/avant_revision_20261030`.
