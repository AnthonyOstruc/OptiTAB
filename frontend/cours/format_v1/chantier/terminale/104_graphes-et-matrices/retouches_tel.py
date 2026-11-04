# -*- coding: utf-8 -*-
"""Retouches ponctuelles : formules trop larges pour un téléphone."""
from pathlib import Path

ICI = Path(__file__).resolve().parent

REMPL = {
    "cours_112.txt": [
        (r"""(AB)_{11} &= 1 \times 1 + 2 \times (-1) + 3 \times 2 \\
&= 5 \\
(AB)_{12} &= 1 \times 0 + 2 \times 2 + 3 \times 1 = 7 \\
(AB)_{21} &= 4 \times 1 + 5 \times (-1) + 6 \times 2 \\
&= 11 \\
(AB)_{22} &= 4 \times 0 + 5 \times 2 + 6 \times 1 = 16""",
         r"""(AB)_{11} &= 1 \times 1 + 2 \times (-1) + 3 \times 2 \\
&= 5 \\
(AB)_{12} &= 1 \times 0 + 2 \times 2 + 3 \times 1 \\
&= 7 \\
(AB)_{21} &= 4 \times 1 + 5 \times (-1) + 6 \times 2 \\
&= 11 \\
(AB)_{22} &= 4 \times 0 + 5 \times 2 + 6 \times 1 \\
&= 16"""),
        (r"$$\det(A) = aei + bfg + cdh - ceg - afh - bdi$$",
         "$$\n\\begin{aligned}\n\\det(A) = {} & aei + bfg + cdh \\\\\n& - ceg - afh - bdi\n\\end{aligned}\n$$"),
    ],
    "exercices.txt": [
        (r"""&= \frac{1}{10}\begin{pmatrix} 3 \times 4 + 2 \times (-1) & 3 \times (-2) + 2 \times 3 \\ 1 \times 4 + 4 \times (-1) & 1 \times (-2) + 4 \times 3 \end{pmatrix} \\
&= \frac{1}{10}\begin{pmatrix} 10 & 0 \\ 0 & 10 \end{pmatrix}
\end{aligned}
$$""",
         r"""&= \frac{1}{10}\begin{pmatrix} 10 & 0 \\ 0 & 10 \end{pmatrix}
\end{aligned}
$$

avec les coefficients du produit des deux matrices entières :

$$
\begin{aligned}
3 \times 4 + 2 \times (-1) &= 10 \\
3 \times (-2) + 2 \times 3 &= 0 \\
1 \times 4 + 4 \times (-1) &= 0 \\
1 \times (-2) + 4 \times 3 &= 10
\end{aligned}
$$"""),
        (r"""1 \times 1 \times 0 + 2 \times 4 \times 5 + 3 \times 0 \times 6 &= 0 + 40 + 0 \\
&= 40""",
         r"""1 \times 1 \times 0 &= 0 \\
2 \times 4 \times 5 &= 40 \\
3 \times 0 \times 6 &= 0 \\
\text{somme} &= 40"""),
        (r"""3 \times 1 \times 5 + 1 \times 4 \times 6 + 2 \times 0 \times 0 &= 15 + 24 + 0 \\
&= 39""",
         r"""3 \times 1 \times 5 &= 15 \\
1 \times 4 \times 6 &= 24 \\
2 \times 0 \times 0 &= 0 \\
\text{somme} &= 39"""),
    ],
}

for nom, liste in REMPL.items():
    p = ICI / nom
    t = p.read_text(encoding="utf-8")
    for a, b in liste:
        assert t.count(a) == 1, (nom, a[:60])
        t = t.replace(a, b)
    p.write_text(t, encoding="utf-8")
print("ok")
