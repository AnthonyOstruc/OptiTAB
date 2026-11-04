# Rapport : Terminale, notion 101 « Conditions / Logique »

**État : prêt.** Le cours 103, la fiche 35 et les exercices 826, 827, 828, 829 et 830 sont réécrits entièrement au format v1. Ids, titres et difficultés sont inchangés, et aucun exercice n'a été ajouté ni retiré.

## Texte
- **Cours.** Remise à niveau complète, modelée sur le chapitre 20 du livre de Terminale. On y trouve :
  - booléens et comparaisons, avec leur notation mathématique ;
  - `=` ou `==`, encadrement `18 <= age <= 65`, comparaison de flottants à une tolérance près (`0.1 + 0.2 == 0.3` est faux) ;
  - `and`, `or`, `not`, table de vérité, lois de De Morgan, évaluation paresseuse (« Pour aller plus loin ») ;
  - `if … else`, `if` seul, `if … elif … else` et l'importance de l'ordre des tests, conditions imbriquées ;
  - fonctions qui renvoient un booléen (`est_pair`, année bissextile) ;
  - test des cas limites (tarifs aux frontières) et 7 erreurs classiques, dont le piège `if x == 1 or 2:`, démontré par un programme.
- **Fiche.** Elle a été condensée : comparaisons, table de vérité, De Morgan, structure `elif` avec organigramme, 5 pièges et un réflexe.
- **Exercices.** Chaque exercice a reçu une 3e question : condition sans imbrication, négation de De Morgan, erreur d'ordre des `elif` à corriger, cas limites, parité.
- **Défauts de l'ancienne version corrigés.**
  - 828 : classification de films incohérente (« Tout public (tout âge) » et « Interdit -16 » pour 14 ans), remplacée par une classification claire.
  - 830 : le programme de sécurité laissait `message` indéfini pour un niveau inconnu ; le code contenait `$\ast$` au lieu de `*` ; une analyse était tronquée (« 15 18 »).
  - Le convertisseur avait mis des « » dans le code.
  - Des corrigés se réduisaient à « le programme affiche … » sans raisonnement.
- **Exactitude.** Le script `verif_conditions.py` exécute les 29 programmes et compare chaque affichage annoncé avec l'affichage réel : tout est identique. Deux gabarits de syntaxe ne sont pas exécutés. `verif_conditions_assertions.py` contrôle De Morgan de façon exhaustive, la négation de l'encadrement sur les âges de 0 à 119, toutes les frontières de tarifs, les prix des billets, l'équivalence de la fonction bissextile sur les années 1 à 3000, etc.

## Figures
- 3 nouvelles figures, dessinées en TikZ au style des livres :
  - `organigramme_elif` (cours et fiche) ;
  - `negation_intervalle` (cours et exercice 827) ;
  - `arbre_cinema` (exercice 829, chemin de la réponse en vert).
- Elles occupent 5 emplacements. La notion n'avait aucune image en ligne.
- Le détecteur ne signale aucun texte posé sur un trait. Les figures font au plus 868 px de large, et chaque PNG a été regardé.

## Contrôles
- `verifier_notion.py --navigateur` : **OK**, 0 problème.
- Captures regardées : cours (partie I) et étapes de l'exercice 830 au format téléphone. J'y ai repéré un calcul aligné réduit et illisible, que j'ai remplacé par une liste.
- Mesure complémentaire dans Chrome : aucune ligne de code ne dépasse son bloc, et aucune première ligne ne passe sous l'étiquette « PYTHON » / « AFFICHAGE ».

## Remarques pour l'orchestrateur
- Mêmes défauts du moteur que pour la notion 99 :
  - l'étiquette du bloc de code chevauche une première ligne longue ;
  - une formule `aligned` large est fortement réduite sur téléphone sans être signalée.
- **Défaut du contrôleur** `controle_apercu.mjs`. Un élément trop large dans l'onglet d'un exercice reste compté pour tous les onglets suivants : les panneaux déjà ouverts restent visibles. Une seule erreur réelle (code en ligne trop long dans la solution de l'exercice 829) produisait ainsi 13 vues signalées.
- Dans les étapes, les programmes sont placés hors des encadrés « étape » : la largeur y est de 35 caractères au lieu de 29.
