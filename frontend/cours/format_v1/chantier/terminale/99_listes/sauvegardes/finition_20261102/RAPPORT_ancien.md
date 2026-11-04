# Rapport : Terminale, notion 99 « Listes »

**État : prêt.** Le cours 105, la fiche 37 et les exercices 836, 837, 838, 839 et 840 sont réécrits entièrement au format v1. Ids, titres et difficultés sont inchangés, et aucun exercice n'a été ajouté ni retiré.

## Texte
- **Cours.** Remise à niveau complète, modelée sur le chapitre 22 du livre de Terminale. On y trouve : la création en extension, les indices positifs et négatifs, l'erreur `IndexError`, les méthodes (`append`, `insert`, `remove`, `pop`), les fonctions d'information et le tri (`sort` ou `sorted`). Suivent les parcours par valeurs et par indices, puis 3 algorithmes de référence : somme et moyenne, maximum, filtrage. On construit ensuite des listes par ajouts successifs (termes d'une suite) et en compréhension, conformément au programme. Viennent enfin la différence entre affectation et copie, un exemple complet et les erreurs fréquentes (dont la suppression pendant un parcours). Les tranches sont signalées « Pour aller plus loin ».
- **Fiche.** Elle a été condensée : définitions, tableaux des méthodes et fonctions, parcours, construction, 4 pièges et un réflexe.
- **Exercices.** Chaque exercice a reçu une 3e question, et une 4e pour l'exercice 839 : erreur d'indice, recherche protégée par `in`, `pop`, minimum et son indice, `sorted` face à `sort`, piège `L = L.sort()`. Les corrigés suivent le modèle méthode / étapes / résultat, avec des tableaux de suivi de boucle et des encadrés « attention ».
- **Défauts de l'ancienne version corrigés.** Le convertisseur avait remplacé les guillemets du code par « », ce qui rendait les programmes faux. Il y avait aussi du pseudo-code avec « → » dans des blocs Python, une sortie tronquée (« 3 12 → max = 15 »), des listes à puces fusionnées sur une ligne et des solutions vagues (« affiche les trois étapes »).
- **Exactitude.** Le script `verif_listes.py` exécute les 40 programmes (17 du cours, 1 de la fiche, 22 des exercices) et compare chaque affichage annoncé avec l'affichage réel : tout est identique. Le même script contrôle par 40 assertions les valeurs des tableaux et du texte, ainsi que les messages d'erreur.

## Figures
- 4 nouvelles figures, dessinées en TikZ au style des livres : `liste_indices`, `liste_insertion`, `liste_copie` et `fruits_indices` (réponse en vert).
- Elles occupent 6 emplacements : cours ×3, fiche ×1, exercices 836 et 837 dans les étapes.
- La notion n'avait aucune image en ligne : rien n'est conservé ni supprimé.
- Le détecteur ne signale aucun texte posé sur un trait. Toutes les figures font au plus 893 px de large, et chaque PNG a été regardé.

## Contrôles
- `verifier_notion.py --navigateur` : **OK**, 0 problème.
- Captures regardées au format téléphone : cours (toutes les parties), fiche, étapes des exercices 1 et 4.
- Mesure complémentaire dans Chrome à 390 px : aucune ligne de code ne dépasse la largeur de son bloc. Il faut au plus 35 caractères au premier niveau, 31 dans un encadré « méthode » et 29 dans une « étape ».

## Remarques pour l'orchestrateur
- **Défaut du moteur.** Dans `renderCode` de `optitabDoc.js`, l'étiquette « PYTHON » / « AFFICHAGE » est placée en absolu dans le coin haut-droit, par-dessus la première ligne de code. Une première ligne longue chevauche l'étiquette : par exemple `noms = ["Léo", "Inès", "Zoé"]` dans un encadré « méthode » sur téléphone. Le contrôleur ne le détecte pas. J'ai contourné le problème en raccourcissant les premières lignes ou en ajoutant un commentaire court en tête de programme. Correction suggérée dans le moteur : réserver une ligne à l'étiquette (`padding-top` plus grand) ou placer l'étiquette au-dessus du bloc.
- **Défaut du contrôleur.** Les lignes de code qui débordent d'un bloc placé dans un encadré ne sont pas signalées : seul le bord du panneau est contrôlé, avec 2 px de tolérance. Le défilement horizontal reste donc possible sans alerte. Je l'ai vérifié à part.
- Les tableaux de 3 colonnes ou plus contenant du code sont peu lisibles sur téléphone : je les ai remplacés par des listes ou par des tableaux de 2 colonnes complétés d'un programme exécuté.
