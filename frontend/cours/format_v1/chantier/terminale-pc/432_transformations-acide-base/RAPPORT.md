# Rapport : notion 432, Transformations acide-base (Terminale, physique-chimie) — PILOTE

## État
Prêt (pilote réduit, consigne du coordinateur du 2026-11-03 : cours, fiche et UN exercice).
`verifier_notion.py --navigateur` : OK, 0 problème. `verif_432.py` (sympy) : 38 contrôles, « TOUT EST JUSTE ».

## Texte
- **Cours 433** (« Transformations acide-base »), écrit à partir du chapitre 1 du livre de Terminale, adapté au téléphone :
  I. Acides et bases de Brönsted, couples, demi-équations ; II. Réaction acide-base (méthode des demi-équations, indices expérimentaux, flèche ou double flèche) ; III. Couples à connaître, espèces amphotères ; IV. Schémas de Lewis (acide carboxylique, carboxylate, amine, ammonium ; sites acide et basique ; charge d’un atome) ; V. pH et $[\ce{H3O+}] = c^\circ \times 10^{-\mathrm{pH}}$, chiffres significatifs ; VI. Test de la relation pH-concentration avec l’acide chlorhydrique (activité expérimentale du programme).
- **Découpage avec le chapitre 9** (« Force des acides et des bases », notion 440) : acide fort / base forte, produit ionique, pH d’une base forte sont laissés à la notion 440 (renvoi « Pour aller plus loin »). Ici, seule la réaction totale de HCl avec l’eau sert au test de la relation, comme le demande le programme.
- **Fiche 371** (« Résumé : Transformations acide-base ») : couples, équation type, couples à connaître, Lewis, pH, 4 erreurs classiques.
- **Exercice** (`nouveau-1`) : « Entraînement - Une amine et son ion ammonium » (éthylamine) : Lewis, site basique, ion éthylammonium et charge, réaction non totale avec l’eau, pH 11,8 → $[\ce{H3O+}] = 2 \times 10^{-12}$ mol·L⁻¹ (1 chiffre significatif). Corrigé : méthode, étapes, résultat encadré, 2 erreurs fréquentes, « À retenir ». Aucun autre exercice n’a été écrit (pas de brouillon).

## Figures (5 fichiers, 8 emplacements, style des livres, `figures/figures.py`)
- `c_transfert` (transfert de H⁺ entre deux couples), `c_lewis_acide`, `c_lewis_amine` (groupe caractéristique en vert), `c_echelle_ph` (verticale, lisible au téléphone) : cours ; les trois dernières aussi dans la fiche.
- `ex_lewis_ethylamine` : corrigé, ce que l’élève ajoute (doublet non liant, charge) en vert.
- Lewis en chemfig, formules en mhchem (mode mathématique : même police que MathJax). Contrôle des chevauchements : 0 erreur, 0 avertissement.
- Abandonnées sur consigne (« seulement l’indispensable ») : montage pH-mètre, dilution, graphe pH = f(−log c), espèces amphotères.

## Contrôles
- verifier_notion OK ; controle_apercu : 10 vues sur 10 sans défaut (téléphone + ordinateur).
- Captures téléphone regardées : cours (5), fiche (2), exercice (énoncé, étapes). Corrigé après relecture : tableaux trop larges remplacés par des listes, formules de pH découpées, Lewis passés en disposition verticale (ils étaient réduits à ~75 % sur téléphone).
- `\ce{…}` s’affiche bien sur le site et dans l’aperçu : formules droites, charges et indices corrects, `<=>` rendu en ⇌. Ni `valider_v1` ni `verifier_notion` n’ont rien refusé de propre à la chimie.

## Remarques pour l’orchestrateur (chapitres suivants)
- **Piège MathJax** : dans `\begin{aligned}`, une ligne qui commence par `[` (ex. `[\ce{H3O+}] &= …`) est lue comme argument optionnel : le membre de gauche disparaît, sans erreur signalée par les contrôles. Écrire `{[\ce{H3O+}]} &= …`. À signaler à tous les agents de chimie.
- **Tableaux** : au-delà de 2 colonnes avec des formules chimiques, ils débordent au téléphone ; préférer des listes.
- **chemfig** : `\chemmove` (cadres autour d’un groupe) exige deux compilations, or `figures_livre.py` n’en fait qu’une : cadres mal placés. Mettre le groupe en couleur à la place (fait ici).
- **Lewis** : disposition verticale (acide en haut, base en bas) pour rester à taille réelle sur téléphone.
- Le préambule chimie (mhchem, chemfig, `\cm`, `\G`, `lewis_ligne`, `echelle_ph`) est réutilisable tel quel depuis ce `figures.py`.
