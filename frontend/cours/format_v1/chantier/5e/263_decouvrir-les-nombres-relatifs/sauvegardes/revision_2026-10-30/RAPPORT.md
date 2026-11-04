État : prêt — chantier local de 5e terminé le 28 octobre 2026.

Texte : Cours recentré sur abscisse, opposé et distance à zéro, sans imposer la notation de valeur absolue. Fiche condensée. Les 126 questions sont expliquées avec tableaux des distances.

Mathématiques : Erreur source corrigée dans l’exercice 2761, question 6 : B et C sont à la même distance 3 de zéro. L’ancienne réponse affirmait « Aucune égalité ». Les égalités de distances sont désormais recalculées systématiquement. La question 1 demande désormais une abscisse « strictement négative » : cette précision évite d’exclure abusivement O alors que zéro est négatif au sens large, conformément au cours.
Audit conservé : `verif_numerique.py` (moteur commun dans la notion 261), calcul rationnel exact SymPy et recomputation indépendante des réponses depuis les énoncés. Premier contrôle du lot : 1 332 vérifications, zéro échec après correction de neuf retours typographiques échappés.

Figures : 22 PNG actifs produits en TikZ, utilisés à 22 positions ; aucune ancienne image conservée ; 22 anciennes positions retirées au profit du texte, de tableaux natifs ou pour éviter les doublons. Les anciens visuels et les nouveaux PNG ont été relus. Compilation et contrôle texte/traits : OK quand des figures sont nécessaires. Les anciennes variantes intermédiaires restent conservées, conformément à la demande de ne rien perdre.

Contrôles : calculs vérifiés par les scripts conservés ; identifiants, titres, difficultés et nombre d'exercices comparés aux sources, sans écart. Vérificateur commun OK ; 130 vues Chrome contrôlées (390 et 1 280 px), zéro débordement, formule invalide, image manquante, bloc en erreur ou élément trop large. Cours mobile intégral, fiche, énoncés et étapes des exercices 1, 2 et 3 regardés. Captures et planches de relecture conservées dans captures/. Preuves : resultats_controles.json, validation.log, captures.log.

Outil : certains contrôles restaient bloqués après les audits dans le nettoyage du profil temporaire Chrome sous Windows. Une copie locale conserve tous les audits et borne uniquement l'attente de browser.close à deux secondes, puis termine après vidage de la sortie. Les outils communs et le moteur du site sont inchangés.

Programme : [BO du 5 mars 2026, annexe mathématiques](https://www.education.gouv.fr/sites/default/files/document/Bulletin%20officiel%20n%C2%B0%2010%20du%205%20mars%202026-480833.pdf), applicable à la 5e depuis la rentrée 2026 ; les prolongements sont signalés. Sources exportées conservées ; aucune commande manage.py, aucun accès ni import en base.
