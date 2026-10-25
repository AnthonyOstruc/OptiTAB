"""Lecture des sources LaTeX du livre : extraction des pistes audio et du vocabulaire.

Le livre est la source unique : chaque piste est décrite par l'environnement
qui l'imprime (dialogue, vocabulaire, paires, transcription, tableausons).
"""
import pathlib
import re

ENVS = ("dialogue", "vocabulaire", "grille", "paires", "phrases", "transcription", "pisteaudio", "tableausons")


def lire_arg(s, i):
    """Lit un argument {..} (accolades équilibrées) à partir de s[i] ; renvoie (texte, fin)."""
    while i < len(s) and s[i] in " \t\n":
        i += 1
    assert s[i] == "{", s[i:i + 40]
    prof, j = 0, i
    while True:
        c = s[j]
        if c == "\\":
            j += 2
            continue
        if c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
            if prof == 0:
                return s[i + 1:j], j + 1
        j += 1


def lire_opt(s, i):
    """Lit un argument optionnel [..] s'il est présent ; renvoie (texte ou None, fin)."""
    k = i
    while k < len(s) and s[k] in " \t":
        k += 1
    if k < len(s) and s[k] == "[":
        j = s.index("]", k)
        return s[k + 1:j], j + 1
    return None, i


def lire_args(s, i, n, opt=False):
    o = None
    if opt:
        o, i = lire_opt(s, i)
    args = []
    for _ in range(n):
        a, i = lire_arg(s, i)
        args.append(a)
    return o, args, i


def sans_commentaires(t):
    return "\n".join(re.sub(r"(?<!\\)%.*$", "", l) for l in t.splitlines())


def nettoyer(t):
    """LaTeX -> texte prononcé."""
    t = re.sub(r"\\note\{[^}]*\}", "", t)
    t = re.sub(r"\\ldots(\{\})?", "…", t)
    t = t.replace("\\ ", " ").replace("~", " ").replace("\\,", "").replace("\\-", "").replace("\\_", "_")
    for _ in range(4):
        t = re.sub(r"\\(?:hl|textbf|textit|emph|en|enb|otH|acc|textmd|textsc)\{([^{}]*)\}", r"\1", t)
    t = re.sub(r"\\otH\s*", "", t)
    t = re.sub(r"\\[a-zA-Z]+\*?", "", t)
    t = t.replace("{", "").replace("}", "")
    t = re.sub(r"\s+", " ", t).strip()
    return t


def titre_propre(t):
    t = re.sub(r"\s*\((?:tableau )?p\.~?\\pageref\{[^}]*\}\)", "", t)
    return nettoyer(t)


def pistes(racine):
    """Renvoie la liste des pistes, dans l'ordre des numéros.

    Chaque piste : {"id", "titre", "type", "evts"} ; evts = liste d'événements :
      ("dit", perso, texte) · ("annonce", texte) · ("repere", texte) · ("silence", s)
      ("didascalie",) · ("repete", texte) · ("paire", a, b) · ("mot", texte)
      ("num", n, texte)
    """
    racine = pathlib.Path(racine)
    res = {}
    for f in sorted(racine.rglob("*.tex")):
        s = sans_commentaires(f.read_text(encoding="utf-8"))
        for m in re.finditer(r"\\begin\{(" + "|".join(ENVS) + r")\}", s):
            env = m.group(1)
            fin = s.index("\\end{%s}" % env, m.end())
            if env == "dialogue":
                _, a, k = lire_args(s, m.end(), 5)
                corps = s[k:fin]
                evts = evenements(corps)
                titre = "Dialogue %s · %s" % (a[0], nettoyer(a[1]))
                res[a[3]] = {"id": a[3], "titre": titre + " (version lente)", "type": "dialogue-lent",
                             "evts": evts, "source": f.name}
                res[a[4]] = {"id": a[4], "titre": titre + " (version normale)", "type": "dialogue",
                             "evts": evts, "source": f.name}
            elif env == "vocabulaire":
                _, a, k = lire_args(s, m.end(), 2)
                evts = [("annonce", "Listen and repeat.")]
                for mm in re.finditer(r"\\mot\b", s[k:fin]):
                    o, b, _ = lire_args(s[k:fin], mm.end(), 3, opt=True)
                    evts.append(("mot", o if o else nettoyer(b[0])))
                res[a[1]] = {"id": a[1], "titre": "Vocabulaire · " + nettoyer(a[0]), "type": "vocabulaire",
                             "evts": evts, "source": f.name}
            elif env == "grille":
                _, a, k = lire_args(s, m.end(), 3)
                evts = [("annonce", "Listen and repeat.")]
                for mm in re.finditer(r"\\grcase\b", s[k:fin]):
                    o, b, _ = lire_args(s[k:fin], mm.end(), 3, opt=True)
                    evts.append(("mot", o if o else nettoyer(b[2] or b[0])))
                res[a[0]] = {"id": a[0], "titre": "Vocabulaire · " + nettoyer(a[1]), "type": "vocabulaire",
                             "evts": evts, "source": f.name}
            elif env == "phrases":
                _, a, k = lire_args(s, m.end(), 2)
                evts = [("annonce", "Listen and repeat.")]
                for mm in re.finditer(r"\\phrase\b", s[k:fin]):
                    o, b, _ = lire_args(s[k:fin], mm.end(), 2, opt=True)
                    evts.append(("repete", "prof", o if o else nettoyer(b[0])))
                res[a[0]] = {"id": a[0], "titre": "Prononciation · phrases à répéter", "type": "pisteaudio",
                             "evts": evts, "source": f.name}
            elif env == "paires":
                _, a, k = lire_args(s, m.end(), 2)
                evts = [("annonce", "Listen and repeat.")]
                for mm in re.finditer(r"\\sonpaire\b", s[k:fin]):
                    _, b, _ = lire_args(s[k:fin], mm.end(), 6)
                    evts.append(("paire", nettoyer(b[0]), nettoyer(b[3])))
                res[a[0]] = {"id": a[0], "titre": "Prononciation · paires de mots", "type": "paires",
                             "evts": evts, "source": f.name}
            elif env in ("transcription", "pisteaudio"):
                _, a, k = lire_args(s, m.end(), 2)
                res[a[0]] = {"id": a[0], "titre": titre_propre(a[1]), "type": env,
                             "evts": evenements(s[k:fin]), "source": f.name}
            elif env == "tableausons":
                _, a, k = lire_args(s, m.end(), 2)
                evts = [("annonce", "Listen and repeat.")]
                for mm in re.finditer(r"\\son\b", s[k:fin]):
                    _, b, _ = lire_args(s[k:fin], mm.end(), 4)
                    evts.append(("mot", nettoyer(b[1])))
                res[a[0]] = {"id": a[0], "titre": "Les sons de l'anglais · " + nettoyer(a[1]), "type": "sons",
                             "evts": evts, "source": f.name}
    return [res[k] for k in sorted(res, key=cle_piste)]


def cle_piste(pid):
    """Ordre des pistes : 0.xx (guide), 1.xx … 4.xx, B1.xx (bilan 1, après l'unité 4), 5.xx…"""
    u, n = pid.split(".")
    rang = 4 * int(u[1:]) + 0.5 if u.startswith("B") else int(u)
    return (rang, int(n))


def evenements(corps):
    evts = []
    motif = re.compile(r"\\(dit|annonce|repere|silence|didascalie|dire|repete|repetepaire|numdire)\b")
    for m in motif.finditer(corps):
        c = m.group(1)
        i = m.end()
        if c == "dit":
            o, a, _ = lire_args(corps, i, 3, opt=True)
            evts.append(("dit", a[0], o if o else nettoyer(a[1])))
        elif c in ("dire", "repete"):
            o, a, _ = lire_args(corps, i, 1, opt=True)
            evts.append(("dit" if c == "dire" else "repete", o or "prof", nettoyer(a[0])))
        elif c == "repetepaire":
            _, a, _ = lire_args(corps, i, 2)
            evts.append(("paire-repete", nettoyer(a[0]), nettoyer(a[1])))
        elif c == "numdire":
            _, a, _ = lire_args(corps, i, 2)
            evts.append(("num", a[0], nettoyer(a[1])))
        elif c == "annonce":
            _, a, _ = lire_args(corps, i, 1)
            evts.append(("annonce", nettoyer(a[0])))
        elif c == "repere":
            _, a, _ = lire_args(corps, i, 1)
            evts.append(("repere", nettoyer(a[0])))
        elif c == "silence":
            _, a, _ = lire_args(corps, i, 1)
            evts.append(("silence", float(a[0])))
        elif c == "didascalie":
            evts.append(("didascalie",))
    return evts


def vocabulaire(racine):
    """Entrées \\mot{anglais}{phonétique}{français} de chaque unité : (unité, anglais, api, français)."""
    out = []
    for f in sorted(pathlib.Path(racine).rglob("u[0-9][0-9]-*.tex")):
        unite = int(f.name[1:3])
        s = sans_commentaires(f.read_text(encoding="utf-8"))
        for m in re.finditer(r"\\begin\{vocabulaire\}", s):
            corps = s[m.end():s.index(r"\end{vocabulaire}", m.end())]
            for mm in re.finditer(r"\\mot(?![a-zA-Z])", corps):
                _, b, _ = lire_args(corps, mm.end(), 3, opt=True)
                out.append((unite, b[0], b[1], b[2]))
    return out
