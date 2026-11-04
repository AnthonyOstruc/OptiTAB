# -*- coding: utf-8 -*-
METHODES = {
    (1, 3): r"On rassemble les critères testés aux questions précédentes : 2340 se termine par 0 (divisible par 2, 5 et 10) et la somme de ses chiffres, §2 + 3 + 4 + 0 = 9§, est divisible par 3 et par 9.",
    (3, 3): r"On regroupe les facteurs premiers identiques trouvés par divisions successives (§420 = 2 \times 2 \times 3 \times 5 \times 7§) et on écrit les facteurs répétés avec un exposant.",
    (5, 3): r"Les multiples cherchés sont §14 \times k§ pour §k§ allant de 5 (§14 \times 5 = 70§) à 9 (§14 \times 9 = 126 \leq 130§) : on compte les valeurs de §k§.",
    (8, 2): r"On teste les diviseurs par paires §d \times \frac{72}{d}§ : §1 \times 72§, §2 \times 36§, §3 \times 24§, §4 \times 18§, §6 \times 12§, §8 \times 9§ ; on s'arrête dès que les paires se croisent, puis on range tout dans l'ordre croissant.",
    (8, 4): r"On compte les nombres de la liste : 6 paires donnent 12 diviseurs (aucun ne se répète, car 72 n'est pas un carré parfait).",
    (9, 1): r"Critère de divisibilité par 2 : un nombre est divisible par 2 si et seulement si son chiffre des unités est pair ; ici le chiffre des unités est §a§.",
    (12, 1): r"MOD(a;b) est la fonction « modulo » du tableur : elle renvoie le reste de la division euclidienne de a par b.",
    (14, 3): r"Les deux lignes repartent ensemble au bout d'un nombre de minutes multiple à la fois de 12 et de 18 ; la première fois, c'est le plus petit multiple commun, 36 min, ajouté à 9 h 00.",
    (18, 5): r"Le stock doit être un multiple de 360 (question 1) ; le plus petit multiple non nul de 360 est 360 lui-même (§360 \times 1§).",
}
