# Audit des figures et précisions scientifiques du 24 octobre 2026

Le manuel de Première est en rédaction dans un autre travail du même espace.
L’audit a porté sur les chapitres présents : 12 dans le PDF disponible au début
de la révision, puis 20 dans les sources au moment du dernier inventaire.
Les exercices demandant une construction ont été rapprochés de leurs corrigés.
Les schémas TikZ, les graphiques et les formules de Lewis en `chemfig` sont
comptés comme figures, y compris lorsqu’ils sont intégrés au texte. Aucun
dessin manquant n’a été trouvé parmi les consignes de construction explicites
des chapitres alors disponibles. Ce repérage ne dispense pas du contrôle final
du livre terminé et de ses éventuelles pages ajoutées ultérieurement.

Deux précisions sont intégrées aux sources du chapitre 6, énoncés et corrigés :

- Exercice 12 : la polarité et la tendance à s’orienter dans un champ électrique
  ne suffisent pas à comparer les vitesses de chauffage. Le liquide modèle
  apolaire est distingué d’une huile alimentaire réelle ; absorption, masse et
  capacité thermique sont citées.
- Exercice 14 : le monoxyde de carbone comporte une liaison triple et un doublet
  non liant par atome. Le schéma indique les charges **formelles** C− et O+,
  de somme nulle. Sa polarité s’appuie sur une donnée expérimentale fournie dans
  l’énoncé. Les charges formelles ne sont pas assimilées aux charges partielles.

Références primaires consultées pour ces précisions :

- [NIST, table des moments dipolaires expérimentaux](https://cccbdb.nist.gov/diplistx.asp)
  : faible dipôle permanent de CO, environ 0,112 D.
- [FDA, Microwave ovens](https://www.fda.gov/radiation-emitting-products/resources-you-radiation-emitting-products/microwave-ovens)
  : interaction des micro-ondes avec les aliments et chauffage.

Les douze scripts numériques de chapitre disponibles au début de l’audit
passent. Les modifications ont été compilées dans une copie isolée de 295 pages,
avec renvois stabilisés et sans débordement LaTeX. Les pages physiques 85, 86,
224 et 225 de cette épreuve interne ont été rendues avec Poppler et inspectées :
formules, charges, doublets et encadrés restent lisibles et dans leurs marges.
Cette épreuve partielle n’est pas publiée comme manuel complet. La construction
en cours dans le dossier principal est conservée ; sa compilation finale devra
reprendre ces corrections.
