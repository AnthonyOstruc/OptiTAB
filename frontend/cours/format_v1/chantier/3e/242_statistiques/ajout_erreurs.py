# -*- coding: utf-8 -*-
"""Ajoute un encadré « Erreur fréquente » à la fin du corrigé de chaque exercice qui n'en a pas."""
import re
from pathlib import Path

E = {
    2317: r"Diviser par le nombre de valeurs **différentes** ($5$) au lieu de l'effectif total ($6$) : la fréquence de $4$ n'est pas $\dfrac{2}{5}$ mais $\dfrac{2}{6}$.",
    2318: r"Diviser par un effectif partiel (par exemple $12 + 9 = 21$) : le dénominateur d'une fréquence est toujours l'effectif du groupe entier, ici $30$.",
    2319: r"Diviser par un mauvais nombre de valeurs : compter les valeurs de la série **avant** de diviser la somme.",
    2320: r"Prendre la valeur du milieu de la série **non rangée** : on range toujours la série avant de chercher la médiane.",
    2321: r"Soustraire la première et la dernière valeur d'une série non rangée : l'étendue utilise la **plus grande** et la **plus petite** valeur de toute la série.",
    2322: r"Confondre la valeur (la note, lue en abscisse) et l'effectif (la hauteur du bâton).",
    2323: r"Calculer la moyenne des notes sans les effectifs : $\dfrac{6 + 8 + 10 + 12 + 16}{5} = 10{,}4$ est faux ; la bonne moyenne pondérée est $11$.",
    2324: r"Oublier de multiplier par l'angle d'une réponse : l'angle de B n'est pas $18^\circ$ mais $18 \times 9^\circ = 162^\circ$.",
    2325: r"Estimer la moyenne avec les bornes des classes (0, 10, 20…) au lieu de leurs **centres** (5, 15, 25, 35).",
    2326: r"Utiliser `=MOYENNE(A2:A4)` : on obtient $\dfrac{4 + 7 + 12}{3} \approx 7{,}67$ en ignorant les effectifs, au lieu de la moyenne pondérée $7{,}1$.",
    2327: r"Faire la moyenne des deux moyennes : c'est faux dès que les deux groupes n'ont pas le même effectif. On additionne les **sommes**.",
    2328: r"Raisonner directement sur les moyennes : on passe toujours par les **sommes** (somme = moyenne × nombre de notes).",
    2329: r"Conclure que deux séries de même moyenne se ressemblent : il faut aussi comparer la médiane et l'étendue.",
    2330: r"Croire que la médiane bouge autant que la moyenne : une valeur extrême déplace beaucoup la moyenne, mais très peu la médiane.",
    2331: r"Calculer la nouvelle moyenne par $\dfrac{14 + 24}{2} = 19$ : il faut repartir de la somme des $10$ valeurs, $\dfrac{126 + 24}{10} = 15$.",
    2332: r"Comparer les hauteurs des barres sans regarder où commence l'axe vertical.",
    2333: r"Comparer seulement les moyennes : sans la médiane et l'étendue, on ne voit ni la répartition ni la dispersion des notes.",
    2335: r"Chercher la note en faisant la moyenne entre la moyenne actuelle et la moyenne visée : on raisonne sur les **sommes** de notes.",
    2336: r"Diviser par le nombre de catégories ($4$) au lieu de l'effectif total ($200$) pour calculer une fréquence.",
}

p = Path(__file__).with_name("exercices.txt")
t = p.read_text(encoding="utf-8")
for ident, txt in E.items():
    i = t.index("Id: %d\n" % ident)
    f = t.index("\nSolution:", i)
    b = t[i:f]
    if "::: attention" in b:
        continue
    box = "::: attention Erreur fréquente\n" + txt + "\n:::\n\n"
    k = b.rfind("::: retenir")
    if k >= 0:
        b = b[:k] + box + b[k:]
    else:
        b = b.rstrip("\n") + "\n\n" + box.rstrip("\n") + "\n"
    t = t[:i] + b + t[f:]
p.write_text(t, encoding="utf-8")
print("ok")
