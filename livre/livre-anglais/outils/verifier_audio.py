"""Réécoute chaque piste (reconnaissance vocale Whisper) et la compare au texte du livre.

  python -X utf8 outils/verifier_audio.py tome-1 [1.05 ...]

Deux contrôles sur le MP3 final :
  1. piste entière : similarité (en mots) entre le texte attendu et le texte reconnu ;
  2. segment par segment : chaque réplique ou mot est découpé dans le MP3 et réécouté seul
     (indispensable pour les listes de mots, où les longs silences trompent la reconnaissance).
Une piste est conforme si chaque segment est reconnu (aux homophones près) ou si la piste
entière dépasse le seuil. Écrit verifications/audio-tome-N.txt ; code 1 en cas d'écart.
"""
import difflib
import json
import pathlib
import re
import sys

import numpy as np
from faster_whisper import WhisperModel

RACINE = pathlib.Path(__file__).resolve().parent.parent
SEUIL = 0.95

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from oreille import conforme, mots  # noqa: E402


def charger_mp3(f):
    import av  # fourni avec faster-whisper
    with av.open(str(f)) as c:
        res = av.AudioResampler(format="s16", layout="mono", rate=16000)
        bouts = []
        for fr in c.decode(audio=0):
            for r in res.resample(fr):
                bouts.append(r.to_ndarray().reshape(-1))
    return np.concatenate(bouts).astype("float32") / 32768.0


def reconnaitre(modele, x):
    segs, _ = modele.transcribe(x, language="en", beam_size=5, vad_filter=False,
                                condition_on_previous_text=False)
    return " ".join(s.text.strip() for s in segs)


def main():
    tome_dir = RACINE / sys.argv[1]
    filtre = set(sys.argv[2:])
    manif = json.loads((tome_dir / "audio" / "manifeste.json").read_text(encoding="utf-8"))
    modele = WhisperModel("small.en", device="cpu", compute_type="int8")
    lignes, echecs, n_seg, n_pistes = [], 0, 0, 0
    for m in manif:
        if filtre and m["id"] not in filtre:
            continue
        n_pistes += 1
        audio = charger_mp3(tome_dir / "audio" / "en-ligne" / m["fichier"])
        # 1. piste entière
        a, b = mots(" ".join(m["attendu"])), mots(reconnaitre(modele, audio))
        ratio = difflib.SequenceMatcher(a=a, b=b, autojunk=False).ratio()
        # 2. segment par segment
        ecarts = []
        for debut, fin, texte in m.get("segments", []):
            i, j = int(max(debut - 0.05, 0) * 16000), int((fin + 0.08) * 16000)
            x = np.concatenate([np.zeros(6400, "float32"), audio[i:j], np.zeros(6400, "float32")])
            n_seg += 1
            brut = reconnaitre(modele, x)
            att, ent = mots(texte), mots(brut)
            if not conforme(texte, brut) and difflib.SequenceMatcher(a=att, b=ent).ratio() < 0.75:
                ecarts.append((texte, " ".join(ent)))
        ok = not ecarts or ratio >= SEUIL
        echecs += not ok
        lignes.append(f"{'OK   ' if ok else 'ÉCART'} {m['id']:>6}  piste {ratio:.3f} · "
                      f"{len(m.get('segments', [])) - len(ecarts)}/{len(m.get('segments', []))} segments  {m['titre']}")
        for t, e in ecarts:
            lignes.append(f"             segment « {t} »  entendu « {e} »")
        print("\n".join(lignes[-1 - len(ecarts):]), flush=True)
    rapport = RACINE / "verifications" / f"audio-{sys.argv[1]}.txt"
    rapport.parent.mkdir(exist_ok=True)
    bilan = f"{n_pistes} pistes, {n_seg} segments réécoutés, {echecs} piste(s) en écart"
    rapport.write_text("\n".join(lignes) + "\n\n" + bilan + "\n", encoding="utf-8")
    print(bilan, "— rapport :", rapport)
    sys.exit(1 if echecs else 0)


if __name__ == "__main__":
    main()
