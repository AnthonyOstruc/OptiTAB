"""Vérifie TOUT le code du livre Python et exporte les fichiers d'accompagnement.

Usage :
    python -X utf8 outils/verifier_code.py tome-1            # tous les fichiers du tome
    python -X utf8 outils/verifier_code.py tome-1 ch01 ch02  # seulement ces fichiers
    python -X utf8 outils/verifier_code.py tome-1 --exporter # + écrit tome-1/code/

Contrôles :
  * chaque bloc « code » suivi d'une ou plusieurs « sortie » / « erreur » est exécuté
    (une exécution par bloc affiché ; «texte» = saisie de l'utilisateur) et la
    transcription doit être identique, caractère pour caractère, à celle du livre ;
  * une « erreur » exige que le programme s'arrête sur une exception ;
  * \\cible{clé} avant une sortie : elle doit être produite par un bloc code
    portant l'option cible=clé (en général la solution, en fin de livre) ;
  * chaque « console » (et « idleshell ») est rejouée dans un Shell IDLE simulé
    (outils/console_idle.py) ; \\suiteconsole la fait continuer la précédente ;
  * les autres blocs de code sont compilés (erreur de syntaxe = échec), sauf
    options trous, bug, nocheck ;
  * longueur des lignes de code ≤ 79 caractères (PEP 8), pas de tabulation ;
  * options : file=, suite (reprend le bloc précédent), bug, trous, norun, nocheck,
    cible=, aleatoire (la sortie n'est pas comparée, seule l'absence d'erreur l'est).
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent
OUTILS = RACINE / "outils"
ENVS = ("code", "sortie", "erreur", "console", "idleshell", "idleediteur")
DEBUT = re.compile(r"^\s*\\begin\{(" + "|".join(ENVS) + r")\}(.*)$")

def lire_accolades(s):
    """Renvoie (contenu, reste) pour une chaîne qui commence par « { »."""
    s = s.lstrip()
    if not s.startswith("{"):
        return None, s
    prof = 0
    for i, c in enumerate(s):
        if c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
            if prof == 0:
                return s[1:i], s[i + 1:]
    return s[1:], ""


def options(chaine):
    """file=a.py, marks={1,2}, run -> dict."""
    res, cle, val, prof, morceau = {}, None, None, 0, ""
    morceaux = []
    for c in chaine:
        if c == "{":
            prof += 1
        elif c == "}":
            prof -= 1
        if c == "," and prof == 0:
            morceaux.append(morceau)
            morceau = ""
        else:
            morceau += c
    morceaux.append(morceau)
    for m in morceaux:
        m = m.strip()
        if not m:
            continue
        if "=" in m:
            cle, val = m.split("=", 1)
            res[cle.strip()] = val.strip().strip("{}")
        else:
            res[m] = True
    return res


class Bloc:
    def __init__(self, env, opts, lignes, fichier, num_ligne, chapitre):
        self.env, self.opts, self.lignes = env, opts, lignes
        self.fichier, self.num_ligne, self.chapitre = fichier, num_ligne, chapitre
        self.executions = []   # blocs sortie / erreur rattachés
        self.precedent = None  # pour suite
        self.cible = None
        self.libre = False
        self.suiteconsole = None
        self.exercice = None

    def lieu(self):
        return f"{self.fichier.name}:{self.num_ligne}"


def nettoyer(lignes):
    # « <<2>> » en fin de ligne d'écran : pastille de renvoi, ignorée
    lignes = [re.sub(r"\s*<<\d+>>$", "", l.rstrip()) for l in lignes]
    while lignes and not lignes[0].strip():
        lignes.pop(0)
    while lignes and not lignes[-1].strip():
        lignes.pop()
    return lignes


def analyser(fichier):
    texte = fichier.read_text(encoding="utf-8").replace("\r\n", "\n").split("\n")
    m = re.search(r"ch(\d+)", fichier.stem)
    chapitre = int(m.group(1)) if m else 0
    blocs, i = [], 0
    dernier_code, rattachable = None, False
    cible_en_attente, libre_en_attente, suite_console = None, False, False
    exercice = None
    precedent_console = None
    while i < len(texte):
        ligne = texte[i]
        d = DEBUT.match(ligne)
        if not d:
            s = ligne.strip()
            mc = re.match(r"\\cible\{([^}]*)\}", s)
            if mc:
                cible_en_attente = mc.group(1)
            if s.startswith("\\sortielibre"):
                libre_en_attente = True
            if s.startswith("\\suiteconsole"):
                suite_console = True
            if s.startswith("\\rattacher") and dernier_code is not None:
                rattachable = True
                i += 1
                continue
            me = re.match(r"\\begin\{corrige\}\{(\d+)\}", s)
            if me:
                exercice = int(me.group(1))
            if s and not s.startswith("%") and not s.startswith("\\titresortie") \
                    and not mc and not s.startswith("\\sortielibre"):
                rattachable = False
            i += 1
            continue
        env, reste = d.group(1), d.group(2)
        arg, _ = lire_accolades(reste)
        opts = options(arg) if (env == "code" and arg) else {}
        debut = i + 1
        j = debut
        fin = re.compile(r"^\s*\\end\{" + env + r"\}")
        while j < len(texte) and not fin.match(texte[j]):
            j += 1
        bloc = Bloc(env, opts, nettoyer(texte[debut:j]), fichier, i + 1, chapitre)
        bloc.exercice = exercice
        if env in ("code", "idleediteur"):
            if env == "code" and (opts.get("suite") or opts.get("variante")):
                bloc.precedent = dernier_code
            dernier_code, rattachable = bloc, True
        elif env in ("sortie", "erreur"):
            if cible_en_attente:
                bloc.cible = cible_en_attente
            elif libre_en_attente:
                bloc.libre = True
            elif rattachable and dernier_code is not None:
                dernier_code.executions.append(bloc)
            cible_en_attente, libre_en_attente = None, False
        elif env in ("console", "idleshell"):
            if suite_console:
                bloc.suiteconsole = precedent_console
            suite_console = False
            precedent_console = bloc
            rattachable = False
        blocs.append(bloc)
        i = j + 1
    return blocs


def code_complet(bloc):
    # variante : le bloc ne montre que des lignes modifiées (à partir de first=n)
    # du programme précédent ; on exécute le programme complet ainsi modifié
    if bloc.opts.get("variante") and bloc.precedent is not None:
        base = code_complet(bloc.precedent).rstrip("\n").split("\n")
        n = int(bloc.opts.get("first", 1))
        base[n - 1:n - 1 + len(bloc.lignes)] = bloc.lignes
        return "\n".join(base) + "\n"
    morceaux, b = [], bloc
    while b is not None:
        morceaux.insert(0, "\n".join(b.lignes))
        b = b.precedent
    return "\n".join(morceaux) + "\n"


def saisies_de(lignes):
    res = []
    for l in lignes:
        res += re.findall(r"«([^»]*)»", l)
    return res


def executer(code, nom, saisies):
    """Exécute le programme comme IDLE (Run Module) ; renvoie (code, lignes)."""
    tmp = Path(tempfile.mkdtemp(prefix="otpy-"))
    try:
        (tmp / nom).write_text(code, encoding="utf-8")
        env = dict(os.environ, OTPY_SAISIES=json.dumps(saisies),
                   PYTHONIOENCODING="utf-8", PYTHONHASHSEED="0")
        env.pop("PYTHONSTARTUP", None)
        p = subprocess.run([sys.executable, "-X", "utf8", str(OUTILS / "execution_idle.py"), nom],
                           cwd=tmp, capture_output=True, text=True, encoding="utf-8", timeout=30,
                           env=env, stdin=subprocess.DEVNULL)
        transcription = p.stdout + p.stderr
        for chemin in (str(tmp / nom), str(tmp / nom).replace("\\", "/")):
            transcription = transcription.replace(chemin, nom)
        return p.returncode, nettoyer(transcription.split("\n"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def instructions_console(lignes):
    instr, sorties_attendues = [], []
    for l in lignes:
        if l.startswith(">>>"):
            instr.append([l[4:] if l.startswith(">>> ") else l[3:]])
        elif l.startswith("...") and instr and not l.startswith("...("):
            instr[-1].append(l[4:] if l.startswith("... ") else l[3:])
    return instr


def rejouer_console(lignes, prefixe=None):
    lignes = list(lignes)
    if lignes and lignes[-1].strip() == ">>>":
        lignes = lignes[:-1]
    # bandeau de démarrage d'IDLE (avant le premier >>>) : non comparé
    entete = []
    while lignes and not lignes[0].startswith(">>>"):
        entete.append(lignes.pop(0))
    if entete:
        obtenu, attendu = rejouer_console(lignes, prefixe)
        return (None if obtenu is None else entete + obtenu), (attendu if obtenu is None else entete + attendu)
    prefixe = list(prefixe or [])
    if prefixe and prefixe[-1].strip() == ">>>":
        prefixe = prefixe[:-1]
    tout = prefixe + lignes
    donnees = {"instructions": instructions_console(tout), "saisies": saisies_de(tout)}
    p = subprocess.run([sys.executable, "-X", "utf8", str(OUTILS / "console_idle.py")],
                       input=json.dumps(donnees), capture_output=True, text=True,
                       encoding="utf-8", timeout=30)
    if p.returncode != 0:
        return None, p.stderr
    obtenu = nettoyer(p.stdout.split("\n"))
    if prefixe:
        n = len(nettoyer(rejouer_console(prefixe)[0] or []))
        obtenu = obtenu[n:]
    return obtenu, lignes


def chaine_console(bloc):
    lignes, b = [], bloc.suiteconsole
    while b is not None:
        lignes = b.lignes + lignes
        b = b.suiteconsole
    return lignes


def diff(attendu, obtenu):
    lignes = []
    for k in range(max(len(attendu), len(obtenu))):
        a = attendu[k] if k < len(attendu) else "<rien>"
        o = obtenu[k] if k < len(obtenu) else "<rien>"
        if a != o:
            lignes.append(f"      ligne {k + 1} :\n        livre  : {a!r}\n        python : {o!r}")
    return "\n".join(lignes[:6])


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    exporter = "--exporter" in sys.argv
    tome = RACINE / (args[0] if args else "tome-1")
    filtres = args[1:]
    fichiers = sorted((tome / "chapitres").glob("*.tex")) + sorted((tome / "projets").glob("*.tex")) \
        + sorted((tome / "bilans").glob("*.tex")) + sorted((tome / "annexes").glob("solutions-*.tex")) \
        + sorted((tome / "liminaires").glob("*.tex"))
    if filtres:
        fichiers = [f for f in fichiers if any(x in f.stem for x in filtres)]
    tous, erreurs, controles = [], [], 0
    for f in fichiers:
        tous += analyser(f)
    cibles = {b.cible: b for b in tous if b.cible}
    cibles_vues = set()
    for b in tous:
        if b.env not in ("code", "idleediteur"):
            continue
        o = b.opts
        for k, l in enumerate(b.lignes, 1):
            controles += 1
            if "\t" in l:
                erreurs.append(f"{b.lieu()} : tabulation ligne {k}")
            if len(l) > 79:
                erreurs.append(f"{b.lieu()} : ligne {k} trop longue ({len(l)} > 79)")
        if o.get("nocheck") or o.get("trous"):
            continue
        source = code_complet(b)
        nom = o.get("file") or "program.py"
        if not o.get("bug") and not b.executions:
            controles += 1
            try:
                compile(source, nom, "exec")
            except SyntaxError as e:
                erreurs.append(f"{b.lieu()} : erreur de syntaxe : {e}")
        runs = list(b.executions)
        if o.get("cible"):
            if o["cible"] not in cibles:
                erreurs.append(f"{b.lieu()} : cible inconnue {o['cible']}")
            else:
                runs.append(cibles[o["cible"]])
                cibles_vues.add(o["cible"])
        if o.get("norun"):
            continue
        for run in runs:
            controles += 1
            code_retour, obtenu = executer(source, nom, saisies_de(run.lignes))
            if run.env == "erreur" and code_retour == 0:
                erreurs.append(f"{b.lieu()} -> {run.lieu()} : une erreur était attendue")
            if run.env == "sortie" and code_retour != 0:
                erreurs.append(f"{b.lieu()} -> {run.lieu()} : le programme a échoué\n"
                               + "\n".join("        " + l for l in obtenu[-6:]))
                continue
            if o.get("aleatoire"):
                continue
            if obtenu != run.lignes:
                erreurs.append(f"{b.lieu()} -> {run.lieu()} : sortie différente\n{diff(run.lignes, obtenu)}")
    for cle, b in cibles.items():
        if cle not in cibles_vues:
            erreurs.append(f"{b.lieu()} : la sortie cible {cle} n'est produite par aucun programme")
    for b in tous:
        if b.env in ("sortie", "erreur") and not (b.cible or b.libre) and not any(
                b in c.executions for c in tous if c.env in ("code", "idleediteur")):
            erreurs.append(f"{b.lieu()} : sortie isolée (ajouter \\cible{{}} ou \\sortielibre)")
        if b.env in ("console", "idleshell"):
            controles += 1
            obtenu, attendu = rejouer_console(b.lignes, chaine_console(b))
            if obtenu is None:
                erreurs.append(f"{b.lieu()} : simulation impossible\n{attendu}")
            elif obtenu != attendu:
                erreurs.append(f"{b.lieu()} : console différente\n{diff(attendu, obtenu)}")
    # export des fichiers d'accompagnement
    if exporter:
        dossier = tome / "code"
        for sous in ("chapters", "solutions"):
            shutil.rmtree(dossier / sous, ignore_errors=True)
        compte = {}
        for b in tous:
            if b.env != "code" or b.opts.get("trous") or b.opts.get("mini") or b.opts.get("variante"):
                continue
            solution = b.fichier.stem.startswith("solutions")
            if b.chapitre == 0 or (not b.opts.get("file") and not (solution and b.exercice)):
                continue
            nom = b.opts.get("file") or f"exercise-{b.exercice:02d}.py"
            base = dossier / ("solutions" if solution else "chapters") / f"chapter-{b.chapitre:02d}"
            base.mkdir(parents=True, exist_ok=True)
            code = "\n".join(re.sub(r"\s*#\s*<\d+>\s*$", "", l) for l in code_complet(b).split("\n"))
            (base / nom).write_text(code.rstrip("\n") + "\n", encoding="utf-8")
            if not solution:
                compte.setdefault(b.chapitre, set()).add(nom)
        with open(dossier / "programmes.tex", "w", encoding="utf-8") as f:
            f.write("%% Écrit par outils/verifier_code.py --exporter : programmes par chapitre\n")
            for ch in sorted(compte):
                f.write(f"\\otNbProgrammes{{{ch}}}{{{len(compte[ch])}}}\n")
        print("Export :", sum(len(v) for v in compte.values()), "programmes de chapitres dans", dossier)
    nb_code = sum(1 for b in tous if b.env == "code")
    nb_cons = sum(1 for b in tous if b.env in ("console", "idleshell"))
    print(f"{len(fichiers)} fichiers · {nb_code} blocs de code · {nb_cons} consoles · {controles} contrôles")
    if erreurs:
        print(f"\n{len(erreurs)} PROBLÈME(S) :")
        for e in erreurs:
            print("  -", e)
        sys.exit(1)
    print("Tout est conforme.")


if __name__ == "__main__":
    main()
