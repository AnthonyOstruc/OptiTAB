État : prêt — révision pédagogique contrôlée le 30 octobre 2026.

21 blocs et leurs identifiants conservés, 114 questions corrigées. 6 exercices remplacés pour diversifier les méthodes ; 0 doublons exacts supplémentaires corrigés. Les titres et les difficultés correspondent aux démarches : 17 découvertes, 2 entraînements, 2 problèmes. Couverture et Id détaillés dans COUVERTURE.md.

Format : même moteur et même syntaxe optitab:1 que la Terminale. Objectifs, sections romaines, propriétés, méthodes courtes, exemples, points d’attention et récapitulation ; fiche synthétique et corrigés question par question. Les constructions ou lectures de graphiques disposent de figures de correction. Les variantes numériques conservées ne sont plus artificiellement classées comme problèmes.

Modifications :

| Id conservé | Travail proposé | Niveau |
|---|---|---|
| 3045 | Relier volumes et capacités | easy |
| 3047 | Reconnaître un patron de cube | easy |
| 3052 | Du patron à la surface d’un cylindre | medium |
| 3054 | Dénombrer un empilement de cubes | medium |
| 3059 | Remplir un aquarium sans déborder | hard |
| 3061 | Adapter une boîte à un produit | hard |

Mathématiques : 386 assertions de l’audit exact OK sur les fichiers finaux ; Id, calculs, conversions et contraintes contrôlés selon la notion. Les propriétés et les arguments qualitatifs ont été relus avec les énoncés et les figures. Preuves : revision_maths_coordination.log, controle_maths_coordination.json, verification_maths.json ; moteur conservé dans la notion 276/verif_notion.py (et correction reportée dans 279/verif_notion.py).

Figures : 8 PNG actifs, sources TikZ et productions précédentes conservées. Toutes les figures actives ont été regardées sur les planches ou individuellement. Compilation et contrôle texte/traits : OK, aucune tolérance ajoutée. Les graduations d’axes emploient le fond blanc autorisé par le guide ; leur ordre de dessin a été corrigé pour éviter que les courbes ou les côtés traversent les chiffres. Les lettres des points restent hors des traits. Preuve : compilation_figures.json.

Rendu final : vérificateur courant et audit renforcé des erreurs MathJax HTML/SVG ; 65 vues mobiles à 390 px et les mêmes 65 vues à 1 280 px, zéro anomalie restante. Absence de caractères de contrôle C0 interdits vérifiée. Journaux : revision_validation.log et revision_navigateur.log ; statut : controles_revision_20261030.json. Les tableaux trop larges des cours ont été compactés quand nécessaire.

Relecture : cours mobile intégral, fiche et exercices 5, 12, 19, 21, énoncés et étapes, regardés dans les captures finales. Preuves : captures_revision_20261030/relecture_documents.png et relecture_revision_1.png, relecture_revision_2.png ; relecture_visuelle_coordination.json.

Outil : copie locale des audits communs, détection MathJax élargie et attente de fermeture Chrome bornée à deux secondes pour le défaut de nettoyage Windows déjà établi. Les audits ne sont pas allégés. Aucun outil commun ou fichier frontend/src modifié.

Sauvegarde antérieure dans sauvegardes/revision_2026-10-30/. Sources exportées conservées, aucun accès ou import en base. Travail limité à la classe de 5e ; programme rentrée 2026 vérifié par la coordination.
