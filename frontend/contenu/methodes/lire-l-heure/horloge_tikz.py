# -*- coding: utf-8 -*-
"""Horloge à aiguilles en TikZ (fiches PDF et figure de la page « Lire l'heure »).

Mêmes conventions que l'horloge interactive du site : petite aiguille des heures
en bleu marine, grande aiguille des minutes en orange, un trait par minute, un
trait épais toutes les 5 minutes, nombres de 1 à 12.
Angles TikZ : 0° à droite, sens inverse des aiguilles d'une montre ; le 12 est à 90°.
"""
BS = chr(92)


def f(x):
    return f"{x:.3f}".rstrip("0").rstrip(".")


def horloge(cx, cy, r, h=None, m=None, minutes_autour=False, taille_nombres=None):
    """Code TikZ d'une horloge de rayon r (cm) centrée en (cx, cy).
    Sans h et m : cadran sans aiguilles (« dessine les aiguilles »)."""
    t = taille_nombres or round(6.2 * r, 1)
    L = [rf"{BS}draw[otNavy!85!black,line width={f(0.85 * r)}pt,fill=white] ({f(cx)},{f(cy)}) circle ({f(r)});"]
    for k in range(60):
        a = 90 - 6 * k
        cinq = k % 5 == 0
        r1 = r * (0.84 if cinq else 0.91)
        L.append(rf"{BS}draw[{'otNavy!85!black' if cinq else 'otMuted!70'},line width={f(1.1 if cinq else 0.45)}pt,line cap=round] "
                 rf"([shift={{({f(cx)},{f(cy)})}}]{a}:{f(r1)}) -- ([shift={{({f(cx)},{f(cy)})}}]{a}:{f(r * 0.97)});")
    for n in range(1, 13):
        a = 90 - 30 * n
        L.append(rf"{BS}node[inner sep=0pt,text=otNavy!85!black,font={BS}otMedium{BS}bfseries{BS}fontsize{{{t}}}{{{t}}}{BS}selectfont] "
                 rf"at ([shift={{({f(cx)},{f(cy)})}}]{a}:{f(r * 0.68)}) {{{n}}};")
    if minutes_autour:
        for k in range(12):
            a = 90 - 30 * k
            L.append(rf"{BS}node[inner sep=0pt,text=otGreenDark,font={BS}otMedium{BS}fontsize{{{round(t * 0.62, 1)}}}{{{round(t * 0.62, 1)}}}{BS}selectfont] "
                     rf"at ([shift={{({f(cx)},{f(cy)})}}]{a}:{f(r * 1.17)}) {{{k * 5:02d}}};")
    if h is not None:
        ah = 90 - ((h % 12) * 30 + m * 0.5)
        am = 90 - 6 * m
        L.append(rf"{BS}draw[otNavy,line width={f(2.0 * r)}pt,line cap=round] ({f(cx)},{f(cy)}) -- ([shift={{({f(cx)},{f(cy)})}}]{f(ah)}:{f(r * 0.5)});")
        L.append(rf"{BS}draw[otOrange!90!black,line width={f(1.25 * r)}pt,line cap=round] ({f(cx)},{f(cy)}) -- ([shift={{({f(cx)},{f(cy)})}}]{f(am)}:{f(r * 0.8)});")
    L.append(rf"{BS}fill[otNavy!85!black] ({f(cx)},{f(cy)}) circle ({f(r * 0.06)});")
    return "\n".join(L)
