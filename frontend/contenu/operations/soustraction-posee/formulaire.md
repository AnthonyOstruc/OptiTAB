---
{
  "slug": "soustraction-posee",
  "titre": "Soustraction posée : les deux méthodes",
  "titreCourt": "Soustraction posée",
  "titreSeo": "Soustraction posée avec retenue : les deux méthodes expliquées",
  "description": "Comment poser une soustraction avec retenue : méthode par cassage et méthode par compensation, cas du zéro, nombres décimaux et vérification, avec schémas.",
  "chapo": "Les deux méthodes enseignées en France pour poser une soustraction avec retenue, expliquées pas à pas avec des schémas : par cassage (ou par échanges) et par compensation, puis le cas du zéro, les nombres décimaux et la vérification.",
  "resume": "Par cassage ou par compensation",
  "vignette": "carte_soustraction",
  "theme": "Soustraction",
  "niveaux": ["Primaire"],
  "ordre": 2,
  "publie": "2026-11-16",
  "modifie": "2026-11-16",
  "liees": ["fiches/soustractions-posees-ce1", "fiches/soustractions-posees-ce2"],
  "motsCles": ["soustraction posée", "poser une soustraction", "soustraction avec retenue", "soustraction en colonnes", "soustraction par cassage", "méthode par compensation", "soustraction avec un zéro", "soustraction décimaux"],
  "figures": [
    { "nom": "soustraction_simple", "alt": "Soustraction posée de 4 869 moins 2 345, chiffres alignés sous m, c, d, u ; chaque chiffre du haut est plus grand que celui du bas ; le résultat est 2 524." },
    { "nom": "soustraction_cassage", "alt": "Soustraction 642 moins 275 par cassage : le 6 est barré et devient 5, le 4 est barré et devient 13, un petit 1 transforme le 2 en 12 ; le résultat est 367." },
    { "nom": "soustraction_compensation", "alt": "Soustraction 642 moins 275 par compensation : des petits 1 transforment le 2 en 12 et le 4 en 14 en haut, et s’ajoutent au 7 et au 2 en bas ; le résultat est 367." },
    { "nom": "soustraction_zero", "alt": "Soustraction 503 moins 278 posée deux fois : par cassage, le 5 devient 4 et le 0 devient 9, le 3 devient 13 ; par compensation, le 3 devient 13 et le 0 devient 10, avec des retenues en bas ; le résultat est 225." },
    { "nom": "soustraction_decimaux", "alt": "Soustraction 23,50 moins 8,76 par compensation, virgules alignées et zéro gris ajouté après 23,5 ; le résultat est 14,74." },
    { "nom": "carte_soustraction", "alt": "Aperçu : soustraction posée 642 moins 275 par compensation, résultat 367.", "carte": true }
  ],
  "chapitresLies": [
    "ce1/soustraire-en-colonnes",
    "ce2/soustraire-en-colonnes",
    "ce2/calculer-par-compensation",
    "cm1/additionner-et-soustraire",
    "6e/calculer-avec-les-decimaux"
  ],
  "faq": [
    ["Comment poser une soustraction ?", "On écrit le plus grand nombre en haut et le plus petit en dessous, unités sous unités. On soustrait colonne par colonne en commençant par les unités. Si le chiffre du haut est plus petit que celui du bas, on utilise une retenue, par cassage ou par compensation."],
    ["Quelle est la différence entre la méthode par cassage et la méthode par compensation ?", "Par cassage, on casse une dizaine du nombre du haut pour en faire dix unités : on barre le chiffre et on écrit sa nouvelle valeur. Par compensation, on ajoute dix unités en haut et une dizaine en bas, ce qui ne change pas la différence. Les deux méthodes donnent le même résultat."],
    ["Quelle méthode de soustraction est enseignée à l’école ?", "Les deux existent et chaque école choisit. La méthode par cassage, aussi appelée méthode par échanges, s’appuie sur la numération et se comprend bien avec du matériel. La méthode par compensation est la méthode traditionnelle des retenues. L’important est d’en maîtriser une sans les mélanger."],
    ["Comment faire une soustraction avec un zéro ?", "Par cassage, si le chiffre voisin est 0, on va chercher plus loin : dans 503, on casse une centaine, 50 dizaines deviennent 49 dizaines et 10 unités. Par compensation, le 0 devient simplement 10 et on ajoute 1 au chiffre du bas de la colonne suivante."],
    ["Comment poser une soustraction avec des virgules ?", "On aligne les virgules, puis on complète le nombre du haut avec des zéros s’il a moins de chiffres après la virgule : 23,5 devient 23,50. On calcule ensuite comme avec des entiers."],
    ["Comment vérifier une soustraction ?", "On additionne le résultat et le nombre retiré : on doit retrouver le nombre de départ. Pour 642 − 275 = 367, on vérifie que 367 + 275 = 642."]
  ]
}
---
<!-- optitab:1 -->
## I. Poser la soustraction {Primaire}

On écrit le **plus grand nombre en haut**, le plus petit en dessous, en alignant les unités sous les unités. On soustrait colonne par colonne, en commençant par les unités.

[IMAGE_1]

Ici, chaque chiffre du haut est plus grand que celui du bas : $9 - 5 = 4$, $6 - 4 = 2$, $8 - 3 = 5$ et $4 - 2 = 2$. Donc $4\,869 - 2\,345 = 2\,524$.

Mais dans $642 - 275$, on ne peut pas retirer $5$ unités de $2$ unités. Il existe deux méthodes pour s’en sortir.

## II. Méthode 1 : par cassage {Primaire}

On l’appelle aussi méthode **par échanges**. On transforme le nombre du haut sans changer sa valeur : on **casse une dizaine** pour en faire dix unités.

[IMAGE_2]

::: methode $642 - 275$ par cassage
1. **Unités** : $2 < 5$. On casse une des $4$ dizaines : il reste $3$ dizaines et on a $12$ unités. $12 - 5 = 7$.
2. **Dizaines** : $3 < 7$. On casse une des $6$ centaines : il reste $5$ centaines et on a $13$ dizaines. $13 - 7 = 6$.
3. **Centaines** : $5 - 2 = 3$.
:::

On barre le chiffre cassé et on écrit sa nouvelle valeur au-dessus. Donc $642 - 275 = 367$.

## III. Méthode 2 : par compensation {Primaire}

C’est la méthode **traditionnelle des retenues**. Elle repose sur une propriété : si l’on ajoute **le même nombre** aux deux termes, la différence ne change pas. On ajoute $10$ unités au nombre du haut et $1$ dizaine, c’est-à-dire aussi $10$ unités, au nombre du bas.

[IMAGE_3]

::: methode $642 - 275$ par compensation
1. **Unités** : $2 < 5$. On ajoute $10$ unités en haut : $12 - 5 = 7$. En compensation, on ajoute $1$ dizaine en bas : le $7$ devient $8$.
2. **Dizaines** : $4 < 8$. On ajoute $10$ dizaines en haut : $14 - 8 = 6$. En compensation, on ajoute $1$ centaine en bas : le $2$ devient $3$.
3. **Centaines** : $6 - 3 = 3$.
:::

Le petit $1$ du haut se met devant le chiffre (il en fait $12$), celui du bas se met à côté du chiffre de la colonne suivante.

::: conseil Laquelle choisir ?
Les deux donnent le même résultat. Le cassage se comprend bien avec du matériel (des barres de dix et des cubes) ; la compensation va plus vite quand il y a des zéros. L’essentiel est de suivre **une seule** méthode, sans mélanger les deux dans un même calcul.
:::

## IV. Quand il y a un zéro en haut {Primaire}

[IMAGE_4]

Dans $503 - 278$, on ne peut pas retirer $8$ de $3$, et il n’y a aucune dizaine à casser.

- **Par cassage** : on casse une **centaine**. Les $50$ dizaines deviennent $49$ dizaines et $10$ unités : on barre le $5$ (qui devient $4$) et le $0$ (qui devient $9$), et le $3$ devient $13$. Puis $13 - 8 = 5$, $9 - 7 = 2$, $4 - 2 = 2$.
- **Par compensation** : $13 - 8 = 5$, on retient $1$ sous les dizaines ; $10 - 8 = 2$, on retient $1$ sous les centaines ; $5 - 3 = 2$.

Dans les deux cas, $503 - 278 = 225$.

::: attention Erreur fréquente
Retirer le petit chiffre du grand dans chaque colonne, quelle que soit sa place : $8 - 3 = 5$, $7 - 0 = 7$, $5 - 2 = 3$, ce qui donne $375$. C’est faux : on retire toujours le chiffre **du bas** de celui **du haut**.
:::

## V. Soustraire des nombres décimaux {Primaire}

[IMAGE_5]

On aligne **les virgules**, puis on complète le nombre du haut avec des zéros : $23{,}5 = 23{,}50$. On calcule ensuite comme avec des entiers, ici par compensation : $10 - 6 = 4$, $15 - 8 = 7$, $13 - 9 = 4$, $2 - 1 = 1$. Donc $23{,}5 - 8{,}76 = 14{,}74$.

::: attention Erreur fréquente
Oublier le zéro et « descendre » le $6$ des centièmes : on obtient $14{,}86$ au lieu de $14{,}74$. Le zéro ajouté ne change pas le nombre ($23{,}50 = 23{,}5$), mais il est indispensable au calcul.
:::

## VI. Vérifier une soustraction {Primaire}

::: methode La preuve par l’addition
On additionne le résultat et le nombre retiré : on doit retrouver le nombre de départ.
$$367 + 275 = 642$$
:::

On peut aussi estimer : $642 - 275$ est proche de $640 - 280 = 360$, le résultat $367$ est vraisemblable.
