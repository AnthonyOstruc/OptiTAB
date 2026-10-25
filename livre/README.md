# Livres OptiTAB

Tous les livres OptiTAB sont rangés ici, et seulement ici.

```
livre/
├── output/                      ← TOUS LES PDF, prêts à lire ou à imprimer
│   ├── README.md                   catalogue complet (liens, nombre de pages)
│   ├── Mathématiques/              01 - Petite section (PS).pdf  …  16 - MPSI.pdf
│   ├── Physique-chimie/            10 - Cinquième (5e).pdf  …  16 - MPSI - Chapitre ….pdf
│   ├── Anglais/                    un dossier par tome : Tome 1 - Premiers pas (A1)/ (PDF + Audios)
│   └── Python/                     un dossier par volume : Volume 1 - First Steps/
│
├── livre-maths/                 ← les sources des livres de maths (un dossier par classe)
├── livre-physique/              ← les sources des livres de physique-chimie
├── livre-anglais/               ← la méthode d'anglais (tome 1 et ses audios)
├── livre-python/                ← la méthode Python (volume 1)
│
├── SUIVI-LIVRES.md              ← état d'avancement de tous les livres
├── OptiTAB - Suivi des livres.xlsx
├── outils/ranger_pdf.py         ← range les PDF livrés et refait le catalogue
└── archives/                    ← anciennes versions, sources zippées, rapports, brouillons
```

## Les dossiers de sources

**`livre-maths/`**

| Dossier | Livre |
| --- | --- |
| `livre-maternelle/` | Petite, moyenne et grande section |
| `livre-cp/`, `livre-ce1/`, `livre-ce2/`, `livre-cm1/`, `livre-cm2/` | Primaire |
| `livre-sixieme/`, `livre-cinquieme/`, `livre-quatrieme/`, `livre-troisieme/` | Collège |
| `livre-quatrieme-2027/`, `livre-troisieme-2028/` | Collège, nouveaux programmes |
| `livre-seconde/`, `livre-premiere/` | Lycée |
| `livre-terminale/`, `livre-terminale-2027/` | Terminale spécialité (2026 et programme 2027) |
| `livres-options-terminale/` | Mathématiques complémentaires et expertes (génère les deux dossiers suivants) |
| `livre-maths-complementaires/`, `livre-maths-expertes/` | Options de Terminale |
| `livre-fiches-terminale/` | Fiches « L'essentiel » de Terminale |
| `livre-mpsi/` | Prépa MPSI |

**`livre-physique/`**

| Dossier | Livre |
| --- | --- |
| `livre-pc-cinquieme/`, `livre-pc-quatrieme/`, `livre-pc-brevet/` | Collège |
| `livre-pc-seconde/`, `livre-pc-premiere/`, `livre-pc-terminale/` | Lycée |
| `livre-physique-mpsi/`, `livre-physique-mpsi-suite/`, `livre-physique-mpsi-integral/` | Prépa MPSI (physique) |

Chaque dossier de livre contient son propre `README.md` : comment compiler, vérifier et livrer.

## Après une livraison

Certains scripts `livrer.py` déposent encore leurs PDF selon l'ancien rangement
(`…/output/pdf/France/…`). Il suffit ensuite de lancer, depuis ce dossier :

```
python -X utf8 outils/ranger_pdf.py
```

Le script renomme chaque PDF (« OptiTAB - Mathématiques - CE1 - Manuel complet.pdf » devient
« 05 - CE1.pdf ») et le pose directement dans le dossier de sa matière, déplace les rapports dans `archives/` et refait
`output/README.md`. Il ne modifie jamais le contenu d'un PDF.
