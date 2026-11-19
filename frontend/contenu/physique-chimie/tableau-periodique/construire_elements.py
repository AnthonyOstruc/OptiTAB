# -*- coding: utf-8 -*-
"""Construit elements.json (les 118 éléments du tableau périodique) et le vérifie.

    python -I -X utf8 construire_elements.py <periodictable.csv de PubChem>

Source des valeurs numériques : PubChem (NIH), tableau périodique
https://pubchem.ncbi.nlm.nih.gov/rest/pug/periodictable/CSV (masses atomiques
IUPAC, électronégativités de Pauling, configurations électroniques).
Les noms français, la période, le groupe, le bloc et la famille sont établis
ici, à partir du numéro atomique, puis recoupés avec PubChem.

Conventions de la page :
- masse molaire arrondie au dixième (g/mol) ; élément sans isotope stable et
  sans masse atomique standard : nombre de masse de l'isotope le plus stable
  entre crochets, par exemple [97] pour le technétium ;
- configuration électronique et électrons de valence pour Z ≤ 18 (programme
  de Seconde : sous-couches 1s, 2s, 2p, 3s, 3p).
"""
import csv
import json
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ICI = Path(__file__).resolve().parent

NOMS = """Hydrogène Hélium Lithium Béryllium Bore Carbone Azote Oxygène Fluor Néon
Sodium Magnésium Aluminium Silicium Phosphore Soufre Chlore Argon Potassium Calcium
Scandium Titane Vanadium Chrome Manganèse Fer Cobalt Nickel Cuivre Zinc
Gallium Germanium Arsenic Sélénium Brome Krypton Rubidium Strontium Yttrium Zirconium
Niobium Molybdène Technétium Ruthénium Rhodium Palladium Argent Cadmium Indium Étain
Antimoine Tellure Iode Xénon Césium Baryum Lanthane Cérium Praséodyme Néodyme
Prométhium Samarium Europium Gadolinium Terbium Dysprosium Holmium Erbium Thulium Ytterbium
Lutécium Hafnium Tantale Tungstène Rhénium Osmium Iridium Platine Or Mercure
Thallium Plomb Bismuth Polonium Astate Radon Francium Radium Actinium Thorium
Protactinium Uranium Neptunium Plutonium Américium Curium Berkélium Californium Einsteinium Fermium
Mendélévium Nobélium Lawrencium Rutherfordium Dubnium Seaborgium Bohrium Hassium Meitnérium Darmstadtium
Roentgenium Copernicium Nihonium Flérovium Moscovium Livermorium Tennesse Oganesson""".split()

# Masses atomiques IUPAC plus précises que celles de PubChem, là où l'arrondi au
# dixième en dépend : PubChem donne Li 7.0, Cu 63.55, Yb 173.05 et Pb 207.
MASSES_PRECISES = {3: "6.94", 29: "63.546", 70: "173.045", 82: "207.2"}

# Éléments sans masse atomique standard (aucun isotope stable, pas de composition
# isotopique terrestre caractéristique) : crochets.
SANS_MASSE_STANDARD = {43, 61} | set(range(84, 90)) | set(range(93, 119))

FAMILLES = {
    "alcalin": [3, 11, 19, 37, 55, 87],
    "alcalino-terreux": [4, 12, 20, 38, 56, 88],
    "lanthanide": list(range(57, 72)),
    "actinide": list(range(89, 104)),
    "transition": list(range(21, 31)) + list(range(39, 49)) + list(range(72, 81)) + list(range(104, 113)),
    "metal-pauvre": [13, 31, 49, 50, 81, 82, 83, 84, 113, 114, 115, 116],
    "metalloide": [5, 14, 32, 33, 51, 52],
    "non-metal": [1, 6, 7, 8, 15, 16, 34],
    "halogene": [9, 17, 35, 53, 85, 117],
    "gaz-noble": [2, 10, 18, 36, 54, 86, 118],
}
FAMILLE_DE = {z: f for f, zs in FAMILLES.items() for z in zs}

# Valeurs de contrôle (masses molaires à 0,1 g/mol, connues par ailleurs).
CONTROLE = {1: "1,0", 2: "4,0", 3: "6,9", 4: "9,0", 5: "10,8", 6: "12,0", 7: "14,0", 8: "16,0", 9: "19,0",
            10: "20,2", 11: "23,0", 12: "24,3", 13: "27,0", 14: "28,1", 15: "31,0", 16: "32,1", 17: "35,5",
            18: "39,9", 19: "39,1", 20: "40,1", 22: "47,9", 24: "52,0", 25: "54,9", 26: "55,8", 27: "58,9",
            28: "58,7", 29: "63,5", 30: "65,4", 35: "79,9", 36: "83,8", 47: "107,9", 50: "118,7", 53: "126,9",
            54: "131,3", 55: "132,9", 56: "137,3", 74: "183,8", 78: "195,1", 79: "197,0", 80: "200,6",
            82: "207,2", 83: "209,0", 70: "173,0", 90: "232,0", 91: "231,0", 92: "238,0", 43: "[97]", 61: "[145]",
            84: "[209]", 86: "[222]", 88: "[226]", 94: "[244]"}


def periode_groupe(z):
    for p, (debut, fin) in enumerate([(1, 2), (3, 10), (11, 18), (19, 36), (37, 54), (55, 86), (87, 118)], start=1):
        if debut <= z <= fin:
            break
    if p == 1:
        return p, 1 if z == 1 else 18
    if p in (2, 3):
        k = z - debut
        return p, k + 1 if k < 2 else k + 11
    if p in (4, 5):
        return p, z - debut + 1
    k = z - debut
    if k < 2:
        return p, k + 1
    if (p == 6 and 57 <= z <= 71) or (p == 7 and 89 <= z <= 103):
        return p, None
    return p, z - (68 if p == 6 else 100)


def bloc(z, groupe):
    if groupe is None:
        return "f"
    if z == 2 or groupe in (1, 2):
        return "s"
    if 3 <= groupe <= 12:
        return "d"
    return "p"


SOUS_COUCHES = [("1s", 2), ("2s", 2), ("2p", 6), ("3s", 2), ("3p", 6)]


def configuration(z):
    reste, morceaux = z, []
    for nom, place in SOUS_COUCHES:
        n = min(reste, place)
        if n:
            morceaux.append((nom, n))
        reste -= n
    texte = " ".join(f"{nom}{n}" for nom, n in morceaux)
    couche = max(int(nom[0]) for nom, _ in morceaux)
    valence = sum(n for nom, n in morceaux if int(nom[0]) == couche)
    return texte, valence


def developper(conf_pubchem):
    """« [Ne]3s2 3p5 » → « 1s2 2s2 2p6 3s2 3p5 » (Z ≤ 18)."""
    coeurs = {"[He]": "1s2", "[Ne]": "1s2 2s2 2p6"}
    t = conf_pubchem.strip()
    for k, v in coeurs.items():
        t = t.replace(k, v + " ")
    return " ".join(t.split())


# Superlourds : nombre de masse des tableaux usuels (IUPAC). PubChem retient
# pour ces cinq éléments un isotope voisin, à la durée de vie mal établie.
NOMBRES_DE_MASSE = {109: 278, 110: 281, 112: 285, 114: 289, 118: 294}


def masse(z, poids):
    if z in NOMBRES_DE_MASSE:
        return f"[{NOMBRES_DE_MASSE[z]}]"
    if z in SANS_MASSE_STANDARD:
        return f"[{int(Decimal(poids).quantize(Decimal('1'), ROUND_HALF_UP))}]"
    return str(Decimal(poids).quantize(Decimal("0.1"), ROUND_HALF_UP)).replace(".", ",")


def main():
    lignes = list(csv.DictReader(open(sys.argv[1], encoding="utf-8")))
    assert len(lignes) == 118 and len(NOMS) == 118, (len(lignes), len(NOMS))
    elements, remarques = [], []
    for z, (ligne, nom) in enumerate(zip(lignes, NOMS), start=1):
        assert int(ligne["AtomicNumber"]) == z
        p, g = periode_groupe(z)
        en = ligne["Electronegativity"].strip()
        el = {
            "z": z, "s": ligne["Symbol"], "nom": nom, "m": masse(z, MASSES_PRECISES.get(z, ligne["AtomicWeight"])),
            "periode": p, "groupe": g, "bloc": bloc(z, g), "famille": FAMILLE_DE[z],
            "en": en.replace(".", ",") if en else None,
        }
        if z <= 18:
            conf, val = configuration(z)
            assert conf == developper(ligne["ElectronConfiguration"]), (z, conf, ligne["ElectronConfiguration"])
            el["config"], el["valence"] = conf, val
        if z in CONTROLE:
            assert el["m"] == CONTROLE[z], (z, el["m"], CONTROLE[z])
        if FAMILLE_DE[z] != {"Alkali metal": "alcalin", "Alkaline earth metal": "alcalino-terreux", "Lanthanide": "lanthanide",
                             "Actinide": "actinide", "Transition metal": "transition", "Post-transition metal": "metal-pauvre",
                             "Metalloid": "metalloide", "Nonmetal": "non-metal", "Halogen": "halogene",
                             "Noble gas": "gaz-noble"}.get(ligne["GroupBlock"]):
            remarques.append(f"{z} {ligne['Symbol']} : famille {FAMILLE_DE[z]} ici, « {ligne['GroupBlock']} » chez PubChem")
        elements.append(el)

    # Contrôles de structure
    assert sum(1 for e in elements if e["groupe"] is None) == 30
    assert {e["s"] for e in elements if e["groupe"] == 18} == {"He", "Ne", "Ar", "Kr", "Xe", "Rn", "Og"}
    assert {e["s"] for e in elements if e["groupe"] == 17} == {"F", "Cl", "Br", "I", "At", "Ts"}
    assert {e["s"] for e in elements if e["groupe"] == 1} == {"H", "Li", "Na", "K", "Rb", "Cs", "Fr"}
    assert [e["s"] for e in elements if e["periode"] == 4 and e["groupe"] == 8] == ["Fe"]
    assert [e["s"] for e in elements if e["periode"] == 6 and e["groupe"] == 11] == ["Au"]
    assert sum(len(v) for v in FAMILLES.values()) == 118
    places = {(e["periode"], e["groupe"]) for e in elements if e["groupe"]}
    assert len(places) == 88, len(places)
    for e in elements:
        assert e["s"][0].isupper() and len(e["s"]) <= 2

    (ICI / "elements.json").write_text(json.dumps(elements, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"elements.json : {len(elements)} éléments, tous les contrôles passent")
    for r in remarques:
        print("  à relire :", r)


if __name__ == "__main__":
    main()
