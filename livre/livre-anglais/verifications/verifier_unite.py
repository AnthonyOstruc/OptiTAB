"""Vérifications d'une unité ou d'un bilan du tome 1 (énoncés, corrigés, transcriptions, audio, phonétique).

  python -X utf8 verifications/verifier_unite.py 1 2 3     # unités 1, 2 et 3
  python -X utf8 verifications/verifier_unite.py B1        # bilan 1
  python -X utf8 verifications/verifier_unite.py tout      # tout le tome

Contrôles :
  - 12 exercices par unité, un corrigé par exercice ; dans chaque exercice à trous, les réponses
    des trous sont exactement celles du corrigé, dans le même ordre ;
  - test express : 10 questions, la lettre du corrigé est la bonne réponse marquée dans la source
    (\\qcm[b]{…}), réponses bien réparties ;
  - notes des dialogues numérotées dans l'ordre, chacune expliquée ; nombre d'expressions annoncé exact ;
  - pistes numérotées sans trou ni doublon ; chaque exercice audio a sa transcription ;
  - jamais deux personnages de la même scène avec la même voix ;
  - bilans : barème de 20 points ;
  - phonétique : comparaison (indicative) avec le dictionnaire de prononciation d'espeak.
"""
import pathlib
import re
import sys

RACINE = pathlib.Path(__file__).resolve().parent.parent
T1 = RACINE / "tome-1"
sys.path.insert(0, str(RACINE / "outils"))
from latex_audio import lire_args, nettoyer, pistes, sans_commentaires  # noqa: E402
from audio import VOIX  # noqa: E402

N, ECHECS, INFOS = 0, [], []


def ok(cond, msg):
    global N
    N += 1
    if not cond:
        ECHECS.append(msg)


def norm(t):
    t = re.sub(r"\\(trou|rep)\[[^\]]*\]", r"\\\1", t)
    return re.sub(r"\s+", " ", nettoyer(t)).strip()


def args_de(source, macro, n, opt=False):
    res = []
    for m in re.finditer(r"\\%s(?![a-zA-Z])" % macro, source):
        o, a, _ = lire_args(source, m.end(), n, opt=opt)
        res.append((o, a) if opt else a)
    return res


def lire(p):
    return sans_commentaires(p.read_text(encoding="utf-8")) if p.exists() else ""


def blocs_corriges(C):
    out = {}
    for m in re.finditer(r"\\begin\{corrige\}\{(\d+)\}", C):
        fin = C.index(r"\end{corrige}", m.end())
        out[int(m.group(1))] = C[m.end():fin]
    m = re.search(r"\\begin\{corrigetest\}(.*?)\\end\{corrigetest\}", C, re.S)
    if m:
        out["test"] = m.group(1)
    return out


def trous(ex):
    t = [norm(a[0]) for a in args_de(re.sub(r"\\trou\[[^\]]*\]", r"\\trou", ex), "trou", 1)]
    t += [norm(a[5]) for a in args_de(ex, "otCarteHeure", 6)]
    t += [norm(a[3]) for a in args_de(ex, "otCarteObjet", 4)]
    t += [norm(a[2]) for a in args_de(ex, "otCartePrepo", 4)]
    t += [norm(a[4]) for a in args_de(ex, "otCarteAction", 5)]
    return t


def reps(c):
    return [norm(a[0]) for a in args_de(c, "rep", 1)]


TOUTES = {p["id"]: p for p in pistes(T1)}


def verifier(cle):
    bilan = cle.startswith("B")
    if bilan:
        n = int(cle[1:])
        U = lire(T1 / "bilans" / f"bilan-{n}.tex")
        C = lire(T1 / "annexes" / f"corriges-b{n}.tex")
        prefixe = f"B{n}."
        corps = U
    else:
        n = int(cle)
        fic = sorted((T1 / "unites").glob(f"u{n:02d}-*.tex"))
        ok(len(fic) == 1, f"unité {n} : fichier introuvable")
        if not fic:
            return
        U = lire(fic[0])
        C = lire(T1 / "annexes" / f"corriges-u{n:02d}.tex")
        prefixe = f"{n}."
        corps = U.split(r"\rubrique{pratique}")[1].split(r"\rubrique{bilan}")[0] if r"\rubrique{pratique}" in U else ""
    nom = f"{'bilan' if bilan else 'unité'} {n}"
    exos = re.split(r"\\exercice(?=\[)", corps)[1:]
    cor = blocs_corriges(C)
    if not bilan:
        ok(len(exos) == 12, f"{nom} : 12 exercices attendus, {len(exos)} trouvés")
    ok(sorted(k for k in cor if k != "test") == list(range(1, len(exos) + 1)),
       f"{nom} : corrigés {sorted(k for k in cor if k != 'test')} pour {len(exos)} exercices")
    for i, ex in enumerate(exos, 1):
        t = trous(ex)
        if t and i in cor:
            ok(t == reps(cor[i]), f"{nom}, ex. {i} : énoncé {t} ≠ corrigé {reps(cor[i])}")
        m = re.match(r"\[([^\]]*)\]", ex)
        opts = m.group(1) if m else ""
        mp = re.search(r"piste=([\dB.]+)", opts)
        if mp:
            ok(mp.group(1) in TOUTES and TOUTES[mp.group(1)]["type"] == "transcription",
               f"{nom}, ex. {i} : piste {mp.group(1)} sans transcription")
    # test express
    if not bilan:
        q = args_de(U, "qcm", 4, opt=True)
        ok(len(q) == 10 and all(o for o, _ in q), f"{nom} : 10 questions marquées attendues")
        lettres = reps(cor.get("test", ""))
        ok([o for o, _ in q] == lettres, f"{nom} : test express, source {[o for o, _ in q]} ≠ corrigé {lettres}")
        ok(max((lettres.count(x) for x in "abc"), default=0) <= 5, f"{nom} : test express mal réparti {lettres}")
        notes = re.findall(r"\\note\{(\d+)\}", U)
        ok(notes == [str(i) for i in range(1, len(notes) + 1)], f"{nom} : notes {notes}")
        ok(re.findall(r"\\pointnote\{(\d+)\}", U) == notes, f"{nom} : explications des notes")
        nb_mots = 0
        for m in re.finditer(r"\\begin\{vocabulaire\}", U):
            nb_mots += len(re.findall(r"\\mot(?![a-zA-Z])", U[m.end():U.index(r"\end{vocabulaire}", m.end())]))
        for m in re.findall(r"(\d+) expressions", U):
            ok(int(m) == nb_mots, f"{nom} : {m} expressions annoncées, {nb_mots} dans les tableaux")
    else:
        pts = [int(p) for p in re.findall(r"points=(\d+)", corps)]
        ok(sum(pts) == 20, f"{nom} : barème {pts} = {sum(pts)} points")
    # pistes
    ids = sorted((p for p in TOUTES if p.startswith(prefixe)), key=lambda x: int(x.split(".")[1]))
    ok([int(x.split(".")[1]) for x in ids] == list(range(1, len(ids) + 1)), f"{nom} : pistes {ids}")
    if not bilan:
        ok(len(ids) >= 12, f"{nom} : {len(ids)} pistes seulement")
    imprimees = re.findall(r"\\(?:qrpiste(?:\[[^\]]*\])?|blocaudio)\{([\dB.]+)\}", U)
    imprimees += re.findall(r"piste=([\dB.]+)", U)
    for m in re.finditer(r"\\begin\{(?:dialogue)\}", U):
        _, a, _ = lire_args(U, m.end(), 5)
        imprimees += [a[3], a[4]]
    for m in re.finditer(r"\\begin\{(?:vocabulaire)\}", U):
        _, a, _ = lire_args(U, m.end(), 2)
        imprimees.append(a[1])
    for m in re.finditer(r"\\begin\{(?:paires|phrases)\}", U):
        _, a, _ = lire_args(U, m.end(), 2)
        imprimees.append(a[0])
    for m in re.finditer(r"\\begin\{(?:grille)\}", U):
        _, a, _ = lire_args(U, m.end(), 3)
        imprimees.append(a[0])
    for pid in ids:
        ok(pid in imprimees, f"{nom} : la piste {pid} n'a pas de QR code dans le livre")
    # voix distinctes dans chaque scène
    for pid in ids:
        persos = {e[1] for e in TOUTES[pid]["evts"] if e[0] == "dit"}
        for p in persos:
            ok(p in VOIX, f"{nom}, piste {pid} : personnage « {p} » sans voix")
        voix = [VOIX[p][0] for p in persos if p in VOIX]
        ok(len(voix) == len(set(voix)), f"{nom}, piste {pid} : deux personnages ont la même voix ({sorted(persos)})")
    # phonétique (indicatif)
    if not bilan:
        phonetique(U, nom)


_tok = None


def squelette(api):
    api = re.sub(r"[ˈˌ.,?!·\s\-]", "", api)
    api = api.replace("lj", "li").replace("ʌɹ", "ɝ").replace("ʌr", "ɝ").replace("ɹ", "r").replace("ɛ", "e").replace("ɾ", "t").replace("ᵻ", "ɪ").replace("ɐ", "ə")
    api = api.replace("ɜː", "ɝː").replace("i", "iː").replace("iːː", "iː").replace("ɑː", "ɑ").replace("ɑ", "ɑː")
    api = api.replace("əl", "l").replace("ɔːr", "oːr").replace("ɔr", "oːr")
    api = re.sub(r"[ˈˌ.,?!\s\-]", "", api)
    return api.replace("ː", "").replace("ɚ", "ər").replace("ɝ", "ər").replace("ɔɪ", "oɪ").replace("ɔ", "ɑ")


def phonetique(U, nom):
    global _tok
    if _tok is None:
        from kokoro_onnx.tokenizer import Tokenizer
        _tok = Tokenizer()
    items = []
    for m in re.finditer(r"\\begin\{vocabulaire\}", U):
        corps = U[m.end():U.index(r"\end{vocabulaire}", m.end())]
        for o, a in args_de(corps, "mot", 3, opt=True):
            items.append((o or nettoyer(a[0]), a[1]))
    for a in args_de(U, "sonpaire", 6):
        items += [(nettoyer(a[0]), a[1]), (nettoyer(a[3]), a[4])]
    ecarts = []
    for mot, api in items:
        ref = _tok.phonemize(mot, "en-us")
        if squelette(api) != squelette(ref):
            ecarts.append(f"{mot:30} livre /{api}/   espeak /{ref}/")
    INFOS.append(f"{nom} : phonétique {len(items) - len(ecarts)}/{len(items)} identique au dictionnaire")
    INFOS.extend("     " + e for e in ecarts)


def main():
    cles = sys.argv[1:]
    if cles == ["tout"]:
        cles = [str(i) for i in range(1, 21) if list((T1 / "unites").glob(f"u{i:02d}-*.tex"))]
        cles += [f"B{i}" for i in range(1, 6) if (T1 / "bilans" / f"bilan-{i}.tex").exists()]
    for c in cles:
        verifier(c)
    print(f"{N} vérifications, {len(ECHECS)} échec(s)")
    for e in ECHECS:
        print("  ÉCHEC :", e)
    for i in INFOS:
        print(i)
    sys.exit(1 if ECHECS else 0)


if __name__ == "__main__":
    main()
