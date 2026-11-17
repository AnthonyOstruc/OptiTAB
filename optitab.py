"""Lance le site OptiTAB en local en une seule commande.

    python optitab.py

- backend Django  : http://127.0.0.1:8000 (avec le venv de backend/)
- frontend Vite   : http://localhost:3000 (le navigateur s'ouvre tout seul)

Ctrl+C arrête les deux.
Attention : backend/.env pointe sur la base de PRODUCTION.
"""

import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

RACINE = Path(__file__).resolve().parent
BACKEND = RACINE / "backend"
FRONTEND = RACINE / "frontend"
WINDOWS = os.name == "nt"

PYTHON_VENV = BACKEND / "venv" / ("Scripts/python.exe" if WINDOWS else "bin/python")
NPM = "npm.cmd" if WINDOWS else "npm"


def port_occupe(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex(("127.0.0.1", port)) == 0


def arreter(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    if WINDOWS:
        # Arrête aussi les processus enfants (vite, autoreload de Django).
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(proc.pid)],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        proc.terminate()


def main() -> int:
    if not PYTHON_VENV.exists():
        print(f"Venv introuvable : {PYTHON_VENV}")
        return 1
    if not (FRONTEND / "node_modules").exists():
        print("node_modules absent : lancez d'abord  cd frontend ; npm install")
        return 1

    for port, nom in ((8000, "backend"), (3000, "frontend")):
        if port_occupe(port):
            print(f"Le port {port} ({nom}) est déjà utilisé : le site tourne peut-être déjà.")
            return 1

    print("Démarrage d'OptiTAB en local (Ctrl+C pour tout arrêter)…\n")
    backend = subprocess.Popen([str(PYTHON_VENV), "manage.py", "runserver", "127.0.0.1:8000"],
                               cwd=BACKEND)
    frontend = subprocess.Popen([NPM, "run", "dev"], cwd=FRONTEND)

    try:
        while True:
            for proc, nom in ((backend, "backend"), (frontend, "frontend")):
                if proc.poll() is not None:
                    print(f"\nLe {nom} s'est arrêté (code {proc.returncode}).")
                    return proc.returncode or 1
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nArrêt…")
        return 0
    finally:
        arreter(frontend)
        arreter(backend)
        print("OptiTAB local arrêté.")


if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.default_int_handler)
    sys.exit(main())
