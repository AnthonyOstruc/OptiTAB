# Livre d'exercices OptiTAB — Terminale

- `main.tex` : le livre (assemble les chapitres et les corrigés)
- `optitab-livre.sty` : le template (polices, couleurs, mise en page)
- `chapitres/` : les énoncés, un fichier par chapitre
- `corriges/` : les corrigés, un fichier par chapitre
- `bac/` : les dix sujets type bac (`sujet-01` à `sujet-10`) et leurs corrigés avec barème (`corrige-01` à `corrige-10`)

## Voir l'aperçu

Ouvrir `main.tex` dans VS Code, puis `Ctrl+Alt+V` : le PDF s'ouvre dans un onglet.
Il se régénère à chaque enregistrement (`Ctrl+S`).

## Compiler à la main

```
lualatex -aux-directory=build main.tex
lualatex -aux-directory=build main.tex
```

Deux passes sont nécessaires (onglets de chapitre en bord de page).
