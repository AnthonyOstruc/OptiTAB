# -*- coding: utf-8 -*-
"""Remplace le doublon de 3464, sans changer l'identifiant 3465."""
from pathlib import Path
import re,json
d=Path(__file__).parent
p=d/'exercices.txt'
t=p.read_text(encoding='utf-8')
blocks=re.split(r'^===[ \t]*$',t,flags=re.M)
replacement=r'''
Découverte — Retrouver deux distances et distinguer deux points
Id: 3465
Difficulté: easy

Énoncé:
<!-- optitab:1 -->
Les points $P$ et $Q$ appartiennent à la médiatrice du segment $[AB]$. On sait que $PB=6$ cm et $QA=9$ cm.

1. Déterminer $PA$ sans mesurer.
2. Déterminer $QB$ sans mesurer.
3. Les points $P$ et $Q$ peuvent-ils être confondus ? Justifier.

Étapes:
<!-- optitab:1 -->

## Question 1 : Déterminer $PA$ sans mesurer.

::: methode
Relier la distance cherchée à la distance connue par l’équidistance.
:::
::: etape Utiliser l’appartenance
$P$ appartient à la médiatrice de $[AB]$, donc $PA=PB$.
:::
::: etape Remplacer par la donnée
La longueur connue est $PB=6$ cm. L’égalité donne donc $PA=6$ cm.
:::
::: resultat
$PA=6$ cm.
:::

## Question 2 : Déterminer $QB$ sans mesurer.

::: methode
Appliquer la propriété au second point, avec ses propres données.
:::
::: etape Écrire l’égalité
$Q$ appartient à la médiatrice de $[AB]$, donc $QA=QB$.
:::
::: etape Reporter la longueur
Comme $QA=9$ cm, on obtient $QB=9$ cm.
:::
::: resultat
$QB=9$ cm.
:::

## Question 3 : Les points $P$ et $Q$ peuvent-ils être confondus ? Justifier.

::: methode
Comparer les distances des deux points à un même point de référence.
:::
::: etape Envisager un même point
Si $P$ et $Q$ étaient confondus, les segments $[PA]$ et $[QA]$ seraient le même segment. Leurs longueurs seraient égales.
:::
::: etape Confronter les longueurs
Or $PA=6$ cm et $QA=9$ cm ; ces longueurs sont différentes. L’hypothèse est donc impossible.
:::
::: resultat
$P$ et $Q$ sont deux points distincts de la même médiatrice.
:::

::: attention
L’équidistance compare, pour un même point, ses distances à $A$ et à $B$. Elle ne donne pas la même distance pour tous les points de la médiatrice.
:::

Solution:
<!-- optitab:1 -->
1. $PA=PB=6$ cm.
2. $QB=QA=9$ cm.
3. Non : $PA\ne QA$, donc $P$ et $Q$ ne sont pas confondus.
'''
found=False
for i,b in enumerate(blocks):
    if re.search(r'^Id:\s*3465\s*$',b,re.M):blocks[i]=replacement;found=True
assert found
p.write_text('\n\n===\n'.join(blocks).rstrip()+'\n',encoding='utf-8')
p=d/'verification_math.json'
data=json.loads(p.read_text(encoding='utf-8'))
data['checks']['3465']=[
 '6>8/2 and 9>8/2',
 'abs(math.hypot(4,math.sqrt(6**2-4**2))-6)<1e-10',
 'abs(math.hypot(4,math.sqrt(9**2-4**2))-9)<1e-10',
 '6!=9',
]
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
(d/'etat.json').write_text(json.dumps({'statut':'en_cours','agent':'geometrie','maj':'2026-11-01','raison':'Vérification finale du remplacement de 3465'},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
