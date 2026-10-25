"""Génère les pistes audio d'un tome à partir de ses sources LaTeX.

  python -X utf8 outils/audio.py tome-1            # toutes les pistes
  python -X utf8 outils/audio.py tome-1 1.05 1.09  # seulement ces pistes

Sorties (dans tome-N/audio/) :
  piste-1-05.mp3 …         les fichiers à mettre en ligne (dossier « en-ligne »)
  durees.tex               durées imprimées sur les pastilles du livre
  manifeste.json           liste des pistes (titres, durées, textes attendus)
  unite-01.html, index.html  pages d'écoute (lecteur, enchaînement, téléchargement)

Voix : Kokoro 82M (poids sous licence Apache 2.0, usage commercial autorisé),
modèle local dans outils/modeles/. Les synthèses sont mises en cache.
"""
import hashlib
import html
import json
import pathlib
import re
import sys

import lameenc
import numpy as np
import soundfile as sf
from mutagen.id3 import ID3, TALB, TCON, TIT2, TPE1, TRCK, COMM

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from latex_audio import cle_piste, pistes  # noqa: E402
from oreille import conforme, entendre, via_mp3  # noqa: E402

RACINE = pathlib.Path(__file__).resolve().parent.parent
MODELES = RACINE / "outils" / "modeles"
SR = 24000

# Personnage -> (voix Kokoro, accent)
VOIX = {
    "prof": ("af_heart", "en-us"),    # voix modèle : consignes, vocabulaire, exercices
    "lea": ("af_bella", "en-us"),
    "jack": ("am_michael", "en-us"),
    "emma": ("bf_emma", "en-gb"),     # Emma est londonienne : accent britannique
    "carter": ("am_fenrir", "en-us"),
    "lopez": ("af_sarah", "en-us"),
    "sam": ("am_puck", "en-us"),
    # rôles secondaires (jamais deux fois la même voix dans une scène : vérifié par verifier_unite.py)
    "serveur": ("am_fenrir", "en-us"),
    "serveuse": ("af_kore", "en-us"),
    "vendeur": ("am_puck", "en-us"),
    "vendeuse": ("af_nicole", "en-us"),
    "employe": ("am_fenrir", "en-us"),
    "employee": ("af_nicole", "en-us"),
    "passant": ("am_fenrir", "en-us"),
    "passante": ("af_aoede", "en-us"),
    "radio": ("am_fenrir", "en-us"),
    "coach": ("am_puck", "en-us"),
    "ana": ("af_aoede", "en-us"),
    "marco": ("am_fenrir", "en-us"),
    "yuki": ("af_kore", "en-us"),
    "liam": ("bm_george", "en-gb"),
    "maya": ("af_kore", "en-us"),
    "davis": ("am_puck", "en-us"),
    "sofia": ("af_nicole", "en-us"),
}
# Vitesse de diction par type de piste
VITESSE = {"dialogue": 0.95, "dialogue-lent": 0.78, "vocabulaire": 0.86, "paires": 0.82,
           "transcription": 0.92, "pisteaudio": 0.86, "sons": 0.82}
# Prononciations forcées (texte imprimé -> texte donné à la voix)
DIRE = {"Ms. Clarke": "Mizz Clarke."}
# Mots que la voix américaine prononce mal (« Lyon » lu « lion ») : remplacés dans tout texte dit
PRONONCER = {"Lyon": "Lee-ohn",
             # « they're » doit se dire /ðer/ (une syllabe), comme « there », et non « they-er »
             "They're": "There", "they're": "there"}
NOMBRES = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten",
           "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen",
           "nineteen", "twenty"]

_kokoro = None


def kokoro():
    global _kokoro
    if _kokoro is None:
        from kokoro_onnx import Kokoro
        _kokoro = Kokoro(str(MODELES / "kokoro-v1.0.onnx"), str(MODELES / "voices-v1.0.bin"))
    return _kokoro


_tok = None


def formes_faibles(texte, accent):
    """Phonèmes avec la forme faible de « can » (/kən/) quand il n'est pas en fin de phrase :
    espeak dit toujours /kæn/, alors qu'un anglophone dit « I can swim » /aɪ kən ˈswɪm/.
    Renvoie None si rien ne change (on garde alors la synthèse depuis le texte)."""
    global _tok
    if not re.search(r"\b(can|was|were)\b", texte, re.I):
        return None
    if _tok is None:
        from kokoro_onnx.tokenizer import Tokenizer
        _tok = Tokenizer()
    ph = _tok.phonemize(texte, accent)
    suite = r"(?=\s+[^\s.!?,;:])"  # suivi d'un mot : pas en fin de phrase
    ph2 = re.sub(r"\bk[æa]n" + suite, "kən", ph)
    ph2 = re.sub(r"\bwʌz" + suite, "wəz", ph2)   # « I was at home » /wəz/
    ph2 = re.sub(r"\bwɜː" + suite, "wɚ", ph2)    # « They were late » /wɚ/
    return ph2 if ph2 != ph else None


def synth(perso, texte, vitesse, cache):
    """Synthèse d'une réplique (avec cache), silences de début et de fin retirés."""
    voix, accent = VOIX[perso]
    texte = DIRE.get(texte, texte)
    for mot, dit in PRONONCER.items():
        texte = re.sub(r"\b%s\b" % mot, dit, texte)
    phonemes = formes_faibles(texte, accent)
    cle = hashlib.sha1(f"{voix}|{accent}|{vitesse}|{texte}{'|faible' if phonemes else ''}".encode()).hexdigest()[:16]
    f = cache / f"{cle}.wav"
    if not f.exists():
        if phonemes:
            s, sr = kokoro().create(phonemes, voice=voix, speed=vitesse, lang=accent, is_phonemes=True)
        else:
            s, sr = kokoro().create(texte, voice=voix, speed=vitesse, lang=accent)
        assert sr == SR
        sf.write(f, s, SR)
    s, _ = sf.read(f, dtype="float32")
    return rogner(s)


def rogner(s, seuil=0.012, marge=0.035):
    env = np.abs(s)
    idx = np.where(env > seuil * max(env.max(), 1e-6))[0]
    if len(idx) == 0:
        return s
    a = max(idx[0] - int(marge * SR), 0)
    b = min(idx[-1] + int(marge * 2 * SR), len(s))
    s = s[a:b].copy()
    n = int(0.008 * SR)
    s[:n] *= np.linspace(0, 1, n)
    s[-n:] *= np.linspace(1, 0, n)
    return s


def silence(sec):
    return np.zeros(int(sec * SR), dtype="float32")


def pause_repetition(d):
    """Temps laissé pour répéter après un énoncé de d secondes."""
    return max(1.8, 1.5 * d + 0.8)


def forme_isolee(texte):
    """Mot ou expression courte (3 mots au plus) dit seul : vitesse naturelle, majuscule et
    point final. Ralentie, la voix déforme les mots isolés commençant par une voyelle
    (« air » entendu « there », « eat » entendu « elite ») : vérifié par outils/verifier_audio.py."""
    if len(texte.split()) > 3:
        return texte, None
    t = texte[0].upper() + texte[1:]
    if t[-1] not in ".!?":
        t += "."
    return t, 1.0


# Choix des prises : comme en studio, on garde la première prise que la reconnaissance
# vocale comprend exactement (mémorisé dans build/prises.json pour être reproductible).
PRISES = RACINE / "build" / "prises.json"
_prises = None


def prises():
    global _prises
    if _prises is None:
        _prises = json.loads(PRISES.read_text(encoding="utf-8")) if PRISES.exists() else {}
    return _prises


def prise(perso, texte, vit, isole, cache):
    """Renvoie (signal, texte dit) pour la meilleure prise de cet énoncé."""
    cle = f"{perso}|{texte}|{vit}|{int(isole)}"
    if cle in prises():
        t, v = prises()[cle]
        return synth(perso, t, v, cache), t
    if isole:
        base, _ = forme_isolee(texte)
        cris = base[:-1] + "!"
        candidats = [(base, 1.0), (base, 0.95), (cris, 1.0), (base, 0.9), (cris, 0.95), (base, 1.05)]
    else:
        candidats = [(texte, vit), (texte, round(vit - 0.04, 2)), (texte, round(vit + 0.04, 2)),
                     (texte, round(vit - 0.08, 2))]
    meilleur = None
    for k, (t, v) in enumerate(candidats):
        a = synth(perso, t, v, cache)
        r = entendre(via_mp3(normaliser(np.concatenate([silence(0.3), a, silence(0.3)])), SR))
        if conforme(texte, r):
            meilleur = (t, v)
            if k:
                print(f"         prise {k + 1} retenue pour « {texte} » ({perso})")
            break
        print(f"         prise {k + 1} écartée pour « {texte} » ({perso}) : entendu « {r} »")
    if meilleur is None:
        meilleur = candidats[0]
        print(f"   !!!   AUCUNE PRISE CONFORME pour « {texte} » ({perso}) — prise 1 gardée")
    prises()[cle] = list(meilleur)
    PRISES.write_text(json.dumps(prises(), ensure_ascii=False, indent=0), encoding="utf-8")
    return synth(perso, meilleur[0], meilleur[1], cache), meilleur[0]


def assembler(p, cache):
    v = VITESSE[p["type"]]
    lent = p["type"] == "dialogue-lent"
    morceaux, attendu, segments = [silence(0.45)], [], []

    def dire(perso, texte, vit=v, isole=False):
        a, dit = prise(perso, texte, vit, isole, cache)
        debut = sum(len(x) for x in morceaux) / SR
        morceaux.append(a)
        attendu.append(dit)
        segments.append([round(debut, 3), round(debut + len(a) / SR, 3), dit])
        return len(a) / SR

    for e in p["evts"]:
        t = e[0]
        if t == "dit" and e[1] == "prof" and "…" in e[2]:
            # « hi … hi » : le même mot répété, avec un vrai silence entre les deux
            for i, bout in enumerate(x.strip() for x in e[2].split("…") if x.strip()):
                if i:
                    morceaux.append(silence(1.1))
                dire("prof", bout, isole=True)
            morceaux.append(silence(2.0))
        elif t == "dit":
            dire(e[1], e[2])
            morceaux.append(silence(0.85 if lent else 0.6))
        elif t == "annonce":
            dire("prof", e[1], 0.92)
            morceaux.append(silence(1.0))
        elif t == "repere":
            txt = e[1] if not e[1].isdigit() else "Number %s" % NOMBRES[int(e[1])]
            dire("prof", txt + ".", 0.92)
            morceaux.append(silence(0.8))
        elif t == "num":
            dire("prof", "Number %s." % NOMBRES[int(e[1])], 0.92)
            morceaux.append(silence(0.7))
            for i, bout in enumerate(x.strip() for x in e[2].split("…") if x.strip()):
                if i:
                    morceaux.append(silence(1.1))
                dire("prof", bout, isole=True)
            morceaux.append(silence(2.6))
        elif t == "silence":
            morceaux.append(silence(e[1]))
        elif t == "didascalie":
            morceaux.append(silence(1.4))
        elif t in ("mot", "repete"):
            d = dire("prof", e[-1], isole=True)
            morceaux.append(silence(pause_repetition(d)))
        elif t == "paire":
            d1 = dire("prof", e[1], isole=True)
            morceaux.append(silence(0.75))
            d2 = dire("prof", e[2], isole=True)
            morceaux.append(silence(pause_repetition(d1 + d2) + 0.6))
        elif t == "paire-repete":
            for x in e[1:]:
                d = dire("prof", x, isole=True)
                morceaux.append(silence(pause_repetition(d)))
        else:
            raise ValueError(e)
    morceaux.append(silence(0.6))
    return normaliser(np.concatenate(morceaux)), attendu, segments


def normaliser(s, cible_db=-19.0, crete_db=-1.0):
    voix = np.abs(s) > 0.02 * np.abs(s).max()
    rms = np.sqrt(np.mean(s[voix] ** 2)) if voix.any() else 1e-3
    s = s * (10 ** (cible_db / 20) / rms)
    crete = np.abs(s).max()
    lim = 10 ** (crete_db / 20)
    if crete > lim:
        s = s * (lim / crete)
    return s


def mp3(s, chemin, p, tome):
    enc = lameenc.Encoder()
    enc.set_bit_rate(96)
    enc.set_in_sample_rate(SR)
    enc.set_channels(1)
    enc.set_quality(2)
    data = enc.encode((np.clip(s, -1, 1) * 32767).astype("<i2").tobytes()) + enc.flush()
    chemin.write_bytes(data)
    tags = ID3()
    tags.add(TIT2(encoding=3, text=f"{p['id']} · {p['titre']}"))
    tags.add(TPE1(encoding=3, text="OptiTAB"))
    tags.add(TALB(encoding=3, text=f"OptiTAB · Anglais · Tome {tome}"))
    tags.add(TRCK(encoding=3, text=p["id"]))
    tags.add(TCON(encoding=3, text="Speech"))
    tags.add(COMM(encoding=3, lang="fra", desc="", text="Voix de synthèse · optitab.net"))
    tags.save(chemin)


def mmss(sec):
    sec = int(round(sec))
    return f"{sec // 60}:{sec % 60:02d}"


def unite_de(pid):
    u = pid.split(".")[0]
    return u if u.startswith("B") else int(u)


TOME = "1"


def main():
    global TOME
    tome_dir = RACINE / sys.argv[1]
    tome = TOME = sys.argv[1].split("-")[-1]
    filtre = set(sys.argv[2:])
    sortie = tome_dir / "audio"
    en_ligne = sortie / "en-ligne"
    cache = RACINE / "build" / "cache-voix"
    for d in (sortie, en_ligne, cache):
        d.mkdir(parents=True, exist_ok=True)
    manif_f = sortie / "manifeste.json"
    ancien = {m["id"]: m for m in json.loads(manif_f.read_text(encoding="utf-8"))} if manif_f.exists() else {}
    liste = pistes(tome_dir)
    manifeste = []
    for p in liste:
        nom = "piste-%s.mp3" % p["id"].replace(".", "-")
        if filtre and p["id"] not in filtre and p["id"] in ancien and (en_ligne / nom).exists():
            manifeste.append(ancien[p["id"]])
            continue
        s, attendu, segments = assembler(p, cache)
        mp3(s, en_ligne / nom, p, tome)
        d = len(s) / SR
        manifeste.append({"id": p["id"], "fichier": nom, "titre": p["titre"], "type": p["type"],
                          "duree": round(d, 2), "attendu": attendu, "segments": segments,
                          "source": p["source"]})
        print(f"{p['id']:>6}  {mmss(d):>5}  {p['titre']}")
    manif_f.write_text(json.dumps(manifeste, ensure_ascii=False, indent=1), encoding="utf-8")
    ecrire_durees(manifeste, sortie / "durees.tex")
    ecrire_pages(manifeste, en_ligne, tome)
    total = sum(m["duree"] for m in manifeste)
    print(f"{len(manifeste)} pistes, {mmss(total)} au total")


def ecrire_durees(manifeste, f):
    lignes = ["%% Écrit par outils/audio.py — ne pas modifier à la main"]
    par_unite = {}
    for m in manifeste:
        lignes.append(r"\otDuree{%s}{%s}" % (m["id"], mmss(m["duree"])))
        par_unite.setdefault(unite_de(m["id"]), []).append(m["duree"])
    for u, ds in par_unite.items():
        minutes = max(1, round(sum(ds) / 60))
        lignes.append(r"\otUniteAudio{%s}{%d}{%d min}" % (u, len(ds), minutes))
    f.write_text("\n".join(lignes) + "\n", encoding="utf-8")


CSS = """
:root{--navy:#1B3C8E;--navy2:#122A66;--green:#5FAC60;--greenD:#3B8544;--ink:#1C2130;--muted:#6B7385;--rule:#D5DAE3;--tint:#F3F5FA}
*{box-sizing:border-box}body{margin:0;font-family:Montserrat,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;color:var(--ink);background:#fff}
header{background:var(--navy);color:#fff;padding:28px 18px 22px;border-bottom:4px solid var(--green)}
header .wrap,main{max-width:760px;margin:0 auto}
.pill{display:inline-block;background:var(--green);color:#fff;font-weight:600;font-size:12px;letter-spacing:.14em;text-transform:uppercase;padding:5px 10px;border-radius:4px}
.surtitre{opacity:.8;font-size:12px;letter-spacing:.12em;text-transform:uppercase;margin-left:10px}
h1{font-size:34px;margin:14px 0 4px}h1+p{margin:0;opacity:.88;font-weight:300;font-size:18px}
main{padding:18px}
.conseil{background:var(--tint);border-left:4px solid var(--navy);padding:12px 14px;border-radius:6px;font-size:14px;line-height:1.5;margin:4px 0 18px}
.piste{border:1px solid var(--rule);border-radius:10px;padding:12px 14px;margin:10px 0;display:grid;grid-template-columns:auto 1fr;gap:4px 12px;align-items:center}
.piste.actif{border-color:var(--navy);box-shadow:0 0 0 2px rgba(27,60,142,.12)}
.num{background:var(--navy);color:#fff;font-weight:600;font-size:13px;border-radius:999px;padding:4px 10px;white-space:nowrap}
.titre{font-weight:600;font-size:15px}.duree{color:var(--muted);font-weight:400;font-size:13px;margin-left:6px}
audio{grid-column:1/-1;width:100%;height:40px;margin-top:6px}
.dl{grid-column:1/-1;font-size:12px}.dl a{color:var(--greenD)}
.unites a{display:flex;justify-content:space-between;align-items:center;text-decoration:none;color:var(--ink);border:1px solid var(--rule);border-radius:10px;padding:14px 16px;margin:10px 0}
.unites a:hover{border-color:var(--navy)}.unites b{color:var(--navy)}
footer{color:var(--muted);font-size:12px;text-align:center;padding:26px 18px 40px;line-height:1.6}
label{font-size:14px;display:inline-flex;gap:8px;align-items:center;margin-bottom:6px}
"""

JS = """
const a=[...document.querySelectorAll('audio')];
a.forEach((x,i)=>{x.addEventListener('play',()=>{a.forEach(y=>{if(y!==x)y.pause()});
document.querySelectorAll('.piste').forEach(p=>p.classList.remove('actif'));x.closest('.piste').classList.add('actif')});
x.addEventListener('ended',()=>{const c=document.getElementById('enchainer');if(c&&c.checked&&a[i+1]){a[i+1].play()}})});
"""


def titres_unites():
    """Titres anglais des unités, lus dans tome-N/plan.tex."""
    import re
    from latex_audio import lire_args, nettoyer, sans_commentaires
    f = RACINE / f"tome-{TOME}" / "plan.tex"
    s = sans_commentaires(f.read_text(encoding="utf-8")) if f.exists() else ""
    out = {}
    for m in re.finditer(r"\\planUnite\b", s):
        _, a, _ = lire_args(s, m.end(), 2)
        out[int(a[0])] = nettoyer(a[1])
    return out


def ecrire_pages(manifeste, dossier, tome):
    par_unite = {}
    for m in manifeste:
        par_unite.setdefault(unite_de(m["id"]), []).append(m)
    noms = {0: "Les sons de l'anglais"}
    def page(u):
        return "sons.html" if u == 0 else f"bilan-{u[1:]}.html" if isinstance(u, str) else f"unite-{u:02d}.html"

    def nom(u):
        return noms[0] if u == 0 else f"Bilan {u[1:]}" if isinstance(u, str) else f"Unit {u}"

    for u, ms in par_unite.items():
        titre = nom(u)
        pistes_html = "\n".join(
            f'<div class="piste" id="p{m["id"]}"><span class="num">&#127911; {m["id"]}</span>'
            f'<span class="titre">{html.escape(m["titre"])}<span class="duree">{mmss(m["duree"])}</span></span>'
            f'<audio controls preload="none" src="{m["fichier"]}"></audio>'
            f'<span class="dl"><a href="{m["fichier"]}" download>Télécharger le fichier MP3</a></span></div>'
            for m in ms)
        html_page = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{titre} · Anglais Tome {tome} · OptiTAB</title><style>{CSS}</style></head><body>
<header><div class="wrap"><span class="pill">{html.escape(titre)}</span><span class="surtitre">Anglais · Tome {tome} · Premiers pas</span>
<h1>Les audios {"du guide de prononciation" if u == 0 else "du bilan " + u[1:] if isinstance(u, str) else "de l'unité " + str(u)}</h1><p>{len(ms)} pistes · {mmss(sum(m["duree"] for m in ms))}</p></div></header>
<main><div class="conseil">Écoutez chaque piste en suivant le livre. Pendant les pauses, répétez à voix haute.
Le numéro de piste (par exemple {ms[0]["id"]}) est imprimé dans le livre à côté de chaque QR code.</div>
<label><input type="checkbox" id="enchainer" checked> Enchaîner les pistes automatiquement</label>
{pistes_html}
<p style="margin-top:24px"><a href="index.html" style="color:var(--navy)">← Toutes les unités du tome {tome}</a></p></main>
<footer>OptiTAB · Anglais · Tome {tome} — enregistrements réalisés avec des voix de synthèse.<br>© SWEELCO · optitab.net</footer>
<script>{JS}</script></body></html>"""
        (dossier / page(u)).write_text(html_page, encoding="utf-8")
    titres = titres_unites()
    liens = "\n".join(
        f'<a href="{page(u)}"><span><b>{"Guide" if u == 0 else nom(u)}</b> · '
        f'{html.escape(noms[0] if u == 0 else "révisions" if isinstance(u, str) else titres.get(u, ""))} '
        f'<span class="duree">{len(ms)} pistes</span></span>'
        f'<span>{mmss(sum(m["duree"] for m in ms))} ›</span></a>'
        for u, ms in sorted(par_unite.items(), key=lambda kv: cle_piste(f"{kv[0]}.0")))
    index = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Audios · Anglais Tome {tome} · OptiTAB</title><style>{CSS}</style></head><body>
<header><div class="wrap"><span class="pill">Tome {tome}</span><span class="surtitre">Anglais · Premiers pas · A1</span>
<h1>Tous les audios du livre</h1><p>{len(manifeste)} pistes · {mmss(sum(m["duree"] for m in manifeste))}</p></div></header>
<main><div class="unites">{liens}</div></main>
<footer>OptiTAB · Anglais · Tome {tome} — enregistrements réalisés avec des voix de synthèse.<br>© SWEELCO · optitab.net</footer>
</body></html>"""
    (dossier / "index.html").write_text(index, encoding="utf-8")


if __name__ == "__main__":
    main()
