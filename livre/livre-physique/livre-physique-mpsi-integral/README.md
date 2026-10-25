# OptiTAB Physique MPSI - Ondes et signaux

Manuscrit commun des chapitres 01 à 10. Un seul PDF, un seul ensemble de
liminaires, un sommaire annuel et une pagination continue.

Les chapitres 01 à 09 développent les rubriques 1.1 à 1.6 du programme national
MPSI (arrêté du 5 janvier 2021, annexe 2). Le chapitre 10 sur les ondes
stationnaires est un approfondissement explicitement annoncé. Le reste du plan
annuel n'est pas présenté comme déjà écrit.

Chaque chapitre comprend diagnostic, cours, schémas vectoriels, TP, numérique,
24 exercices corrigés, 3 défis corrigés, DM et DS avec barèmes. Les liens
authentiques conservent la provenance et le support original des vrais sujets.

## Recompiler le manuscrit

Installer Python 3, LuaLaTeX, les polices Libertinus et Montserrat et les paquets
LaTeX appelés dans `mpsi-livre.sty`. Puis exécuter dans ce dossier :

```text
python compiler.py
```

Le PDF est écrit dans `build/main.pdf`. Le script attend la stabilisation des
renvois et refuse les débordements, caractères manquants et références indéfinies.

Les figures TikZ et PGFPlots sont dans `figures/chNN/`. Les chapitres sont dans
`chapitres/` ; les liminaires et le plan sont communs. Les identifiants de lien et
de figure sont distincts par chapitre, même lorsque les exercices reprennent les
numéros E01 à E24.

## Contrôle éditorial

La fabrication et l'audit sont conservés dans le dossier voisin
`livre-physique-mpsi-suite` : `assembler_livre.py`, `verifier_livre.py` et
`livrer_livre.py`. Les contrôles complètent, sans remplacer, le rendu Poppler et
la relecture visuelle de toutes les pages.

Les énoncés PDF extérieurs ne sont pas redistribués dans les sources du livre.
Les références et les empreintes des documents consultés sont conservées dans
les manifestes de contrôle.
