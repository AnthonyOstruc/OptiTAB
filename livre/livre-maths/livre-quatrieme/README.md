# OptiTAB — Mathématiques de Quatrième

Édition France 2026-2027 du 22 octobre 2026. Le nouveau programme de Quatrième
entre en application en 2027-2028. Les sources figurent dans le PDF et dans
liminaires_contenu.py.

18 chapitres, 270 exercices progressifs, 18 défis, deux bilans et tous leurs
corrigés. Données originales et charte graphique de la collection OptiTAB.

## Reproduction

Python 3, SymPy, PyMuPDF et Pillow ; LuaLaTeX (MiKTeX avec les paquets du modèle),
polices Montserrat et polices mathématiques de la charte ; Poppler pour la
seconde vérification visuelle. Les six fichiers du cache _modele_collection
et les logos sont inclus ; aucun autre dossier de livre n'est nécessaire.

Depuis la racine du projet :

    python livre-quatrieme/verifier_contenu.py
    python livre-quatrieme/verifier_figures.py
    python livre-quatrieme/construire.py
    python livre-quatrieme/compiler.py
    python livre-quatrieme/controler_pdf.py
    python livre-quatrieme/rendre_poppler.py

Le constructeur génère les fichiers LaTeX. Le compilateur travaille sur une
copie isolée, stabilise les renvois et vérifie que les sources ne changent pas.
Ne pas modifier les sources LaTeX pendant son exécution. Les journaux restent
dans build/.

Le contrôle PDF produit une image par page et des planches de douze pages.
Relire tout le livre et les pages critiques à grande taille. La relecture
manuelle doit identifier l'empreinte du PDF effectivement relu. Le script de
livraison exige ces contrôles avant de copier les livrables.

Les contrôles de calcul soutiennent une relecture pédagogique et visuelle
séparée ; ils ne remplacent pas une expertise humaine indépendante.
