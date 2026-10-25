"""Reconnaissance vocale (Whisper) partagée par audio.py (choix des prises) et verifier_audio.py."""
import re

import numpy as np

EQUIV = {"leah": "lea", "léa": "lea", "lia": "lea", "layah": "lea", "leia": "lea", "okay": "ok", "mizz": "ms",
         "miz": "ms", "mister": "mr", "missus": "mrs", "hiya": "hi", "clark": "clarke", "dialog": "dialogue",
         # homophones : l'oreille ne peut pas les distinguer
         "they're": "ðer", "there": "ðer", "their": "ðer", "you're": "jʊr", "your": "jʊr",
         "high": "hi", "eye": "i", "aye": "i", "hear": "here", "too": "two", "to": "two",
         # prénoms des exercices, transcrits avec une autre orthographe
         "anna": "ana", "marko": "marco", "yuuki": "yuki", "leeam": "liam", "chloe": "chloé",
         "mark": "marc", "sophia": "sofia", "layer": "lea", "phylu": "filou", "filu": "filou", "philou": "filou",
         # autres homophones (la comparaison est symétrique, donc sans risque)
         "sun": "son", "ant": "aunt", "theirs": "there's", "by": "bye", "buy": "bye", "meet": "meat",
         # orthographe britannique (Whisper l'emploie quand la voix est britannique)
         "colour": "color", "grey": "gray", "favourite": "favorite", "centre": "center",
         "neighbour": "neighbor", "theatre": "theater", "travelling": "traveling", "mum": "mom",
         # « a cent », « a dress » : un seul mot pour l'oreille (comparaison sans espaces)
         "ascent": "acent", "address": "adress", "wear": "where", "bored": "board", "ferm": "firm", "ah": "ha", "aha": "ha", "hah": "ha",
         "presence": "presents", "myer": "maya", "ate": "eight", "sea": "see", "sey": "say",
         # « bought » = « bot » en américain ; « met » isolé est compris « Matt » par Whisper
         "bot": "bought", "matt": "met"}
CHIFFRES = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six",
            "7": "seven", "8": "eight", "9": "nine", "10": "ten"}

_modele = None


def modele():
    global _modele
    if _modele is None:
        from faster_whisper import WhisperModel
        _modele = WhisperModel("small.en", device="cpu", compute_type="int8")
    return _modele


UNITES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
          "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
DIZAINES = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy", 8: "eighty", 9: "ninety"}
# Noms des lettres, quand la voix épelle (Whisper écrit « Why » pour Y, « You » pour U…)
LETTRES = {"why": "y", "you": "u", "age": "h", "aged": "h", "aitch": "h", "jay": "j", "kay": "k", "okay": "k", "ok": "k",
           "see": "c", "sea": "c", "bee": "b", "be": "b", "pee": "p", "tea": "t", "tee": "t", "zero": "o",
           "owe": "o", "are": "r", "ex": "x", "eye": "i", "queue": "q", "cue": "q", "gee": "g", "dee": "d",
           "vee": "v", "zee": "z", "em": "m", "en": "n", "el": "l", "ell": "l", "ess": "s", "ef": "f",
           "eff": "f", "double": "w"}


HOMO_LETTRES = {("tea", "t"), ("tee", "t"), ("see", "c"), ("sea", "c"), ("you", "u"), ("are", "r"),
                ("why", "y"), ("eye", "i"), ("bee", "b"), ("pea", "p"), ("queue", "q")}


def en_lettres(n):
    """Nombre (0 à 999) en mots anglais, sans « and » : 27 → twenty seven."""
    if n < 20:
        return [UNITES[n]]
    if n < 100:
        return [DIZAINES[n // 10]] + ([UNITES[n % 10]] if n % 10 else [])
    if n == 100:
        return ["a", "hundred"]
    return [UNITES[n // 100], "hundred"] + (en_lettres(n % 100) if n % 100 else [])


MOIS = {"jan": "january", "feb": "february", "aug": "august", "sep": "september", "oct": "october",
        "nov": "november", "dec": "december"}
ORDINAUX = ["zeroth", "first", "second", "third", "fourth", "fifth", "sixth", "seventh", "eighth", "ninth",
            "tenth", "eleventh", "twelfth", "thirteenth", "fourteenth", "fifteenth", "sixteenth",
            "seventeenth", "eighteenth", "nineteenth"]
ORD_DIZAINES = {2: "twentieth", 3: "thirtieth", 4: "fortieth", 5: "fiftieth", 6: "sixtieth", 7: "seventieth",
                8: "eightieth", 9: "ninetieth"}


def en_ordinal(n):
    """Ordinal en mots : 15 → [fifteenth] ; 21 → [twenty, first] ; 30 → [thirtieth]."""
    if n < 20:
        return [ORDINAUX[n]]
    if n % 10 == 0:
        return [ORD_DIZAINES[n // 10]]
    return [DIZAINES[n // 10], ORDINAUX[n % 10]]


def mots(t, heure=False):
    """Mots normalisés. heure=True : « 945 » est lu comme une heure (nine forty-five)."""
    t = t.lower().replace("’", "'").replace("…", " ").replace("u.s.", "us").replace("u.k.", "uk")
    t = re.sub(r"\bt2\b", "tea too", t)  # « tea too » transcrit « T2 »
    # anglais parlé : « gonna », « wanna », « gotta » valent la forme complète
    t = re.sub(r"\bgonna\b", "going to", t)
    t = re.sub(r"\bwanna\b", "want to", t)
    t = re.sub(r"\bgotta\b", "got to", t)
    if heure:
        t = re.sub(r"\b(\d{1,2})([0-5]\d)\b", r"\1 \2", t)
    t = re.sub(r"\b(leon|lee-ohn|lion)\b", "lyon", t)
    # prix : « $40 » → « 40 dollars » ; « $9.99 » → « 9 99 »
    t = re.sub(r"\$(\d+)\.(\d{2})\b", r"\1 \2", t)
    t = re.sub(r"\$(\d+)", r"\1 dollars", t)
    # adresses e-mail écrites par Whisper : « leah.martin@example.com »
    t = re.sub(r"(?<=[a-z])\.(?=[a-z])", " dot ", t).replace("@", " at ")
    t = re.sub(r"(\d{1,2})[:.](\d{2})\b", r"\1 \2", t)  # heures : « 9.15 », « 8:30 » → « 9 15 »
    t = re.sub(r"\b(\d{1,2}) 00\b", r"\1 o'clock", t)   # « 9:00 » → « 9 o'clock »
    t = re.sub(r"\blay a\b", "lea", t)
    t = re.sub(r"(\w)'s\b", r"\1 's", t)  # génitif : « leia's » → « leia 's »
    # mois abrégés par Whisper : « Oct. 31 »
    t = re.sub(r"\b(jan|feb|aug|sept?|oct|nov|dec)\b\.?", lambda m: MOIS[m.group(1)[:3]], t)
    t = re.sub(r"[^a-zàâçéèêëîïôûùüÿ0-9' ]", " ", t)
    out = []
    for w in t.split():
        w = w.strip("'")
        m = re.fullmatch(r"(\d{1,2})(st|nd|rd|th|s)", w)
        if m:  # ordinaux écrits en chiffres : « 15th » → fifteenth, « 21st » → twenty first
            out += en_ordinal(int(m.group(1)))
            continue
        if w.isdigit():
            # « 27 » → twenty seven ; « 917 », « 0148 » (numéros de téléphone) → chiffre par chiffre
            if len(w) >= 3 and not (len(w) == 3 and w.endswith("00")):  # « 200 » : two hundred
                out += [UNITES[int(c)] for c in w]
            else:
                out += en_lettres(int(w))
            continue
        w = CHIFFRES.get(w, w)
        if w == "theirs":  # homophone de « there's », découpé comme lui
            out += ["ðer", "s"]
            continue
        out.append(EQUIV.get(w, w))
    # Whisper écrit « Number eight » sous la forme « 8. » : le mot « number » est ignoré ;
    # au téléphone, 0 se dit « oh » : il équivaut à « zero »
    return ["zero" if w == "oh" else w for w in out if w and w != "number"]


def vers16k(s, sr):
    n = int(len(s) * 16000 / sr)
    return np.interp(np.linspace(0, len(s) - 1, n), np.arange(len(s)), s).astype("float32")


def via_mp3(s, sr):
    """Aller-retour MP3 (96 kb/s) : la prise est jugée telle que l'acheteur l'entendra."""
    import io
    import av
    import lameenc
    enc = lameenc.Encoder()
    enc.set_bit_rate(96)
    enc.set_in_sample_rate(sr)
    enc.set_channels(1)
    enc.set_quality(2)
    data = enc.encode((np.clip(s, -1, 1) * 32767).astype("<i2").tobytes()) + enc.flush()
    with av.open(io.BytesIO(data)) as c:
        res = av.AudioResampler(format="s16", layout="mono", rate=16000)
        b = [r.to_ndarray().reshape(-1) for fr in c.decode(audio=0) for r in res.resample(fr)]
    return np.concatenate(b).astype("float32") / 32768.0


def entendre(x16):
    """Texte reconnu dans un signal à 16 kHz (avec marges de silence)."""
    x = np.concatenate([np.zeros(6400, "float32"), x16.astype("float32"), np.zeros(6400, "float32")])
    segs, _ = modele().transcribe(x, language="en", beam_size=5, vad_filter=False,
                                  condition_on_previous_text=False)
    return " ".join(s.text.strip() for s in segs)


def joindre_lettres(lst):
    """Regroupe les suites de lettres isolées : [martin, m, a, r, t, i, n] → [martin, martin]."""
    out, run = [], []
    for x in lst + [None]:
        if x is not None and len(x) == 1 and x.isalpha():
            run.append(x)
            continue
        if run:
            out.append("".join(run) if len(run) > 1 else run[0])
            run = []
        if x is not None:
            out.append(x)
    return out


def numerique(lst):
    """Les nombres en chiffres, collés : [fifteen, one, five] et [one, five, one, five] → « 1515 ».
    Les ordinaux comptent comme les cardinaux (Whisper écrit « October 31 » pour « October thirty-first »)."""
    dizaines = {v: k for k, v in DIZAINES.items()}
    dizaines.update({v: k for k, v in ORD_DIZAINES.items()})
    unites = {w: n for n, w in enumerate(UNITES)}
    unites.update({w: n for n, w in enumerate(ORDINAUX)})
    out, i = [], 0
    while i < len(lst):
        w = lst[i]
        if w in dizaines:
            suiv = lst[i + 1] if i + 1 < len(lst) else None
            u = unites[suiv] if suiv in unites and 1 <= unites[suiv] <= 9 else 0
            out.append(str(dizaines[w] * 10 + u))
            i += 2 if u else 1
            continue
        out.append(str(unites[w]) if w in unites else " " + w + " ")
        i += 1
    return "".join(out).split()


def conforme(attendu, reconnu):
    a, b = mots(attendu), mots(reconnu)
    if b[:1] == ["a"] and a[:1] != ["a"]:  # « a » parasite en tête : « a six and some cheese »
        b = b[1:]
    if numerique(a) == numerique(b):
        return True
    if a == b or joindre_lettres(a) == joindre_lettres(b) or a == mots(reconnu, heure=True):
        return True
    if "".join(a).replace("'", "") == "".join(b).replace("'", ""):  # « JackSister »
        return True
    # mots homophones de lettres : « Tea, of course » transcrit « T, of course »
    if len(a) == len(b) and all(x == y or (x, y) in HOMO_LETTRES or (y, x) in HOMO_LETTRES
                                for x, y in zip(a, b)):
        return True
    # « Jack's sister » transcrit « JackSister » : le s du génitif se fond dans le s suivant
    if "".join(x for x in a if x != "s") == "".join(x for x in b if x != "s"):
        return True
    # lettres épelées : on compare lettre à lettre, aux noms des lettres près
    if a and all(len(x) == 1 for x in a):
        if "".join(a) == "".join(b):  # « B, R, O, O, K, S » transcrit « BROOKS »
            return True
        b = [LETTRES.get(x, x) for x in b]
        b = [c for x in b for c in (x if len(x) <= 3 and x.isalpha() and x not in LETTRES.values() else [x])]
        return a == b
    return False
