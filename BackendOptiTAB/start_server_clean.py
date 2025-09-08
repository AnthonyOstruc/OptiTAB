#!/usr/bin/env python
"""
Script de lancement du serveur avec nettoyage automatique de l'environnement
"""
import os
import sys
import subprocess

def main():
    """Lance le serveur Django après nettoyage"""
    print("🚀 Lancement du serveur OptiTAB avec environnement propre")
    print("=" * 60)

    # Nettoyer l'environnement
    print("🧹 Nettoyage de l'environnement...")
    exec(open('clean_proxy_env.py').read())

    print("\n🎯 Lancement du serveur Django...")
    print("-" * 40)

    try:
        # Lancer le serveur Django
        cmd = [sys.executable, 'manage.py', 'runserver']
        print(f"Commande: {' '.join(cmd)}")
        print("Serveur accessible sur: http://localhost:8000")
        print("\n💡 Appuyez sur Ctrl+C pour arrêter le serveur")
        print("=" * 60)

        subprocess.run(cmd, cwd=os.getcwd())

    except KeyboardInterrupt:
        print("\n\n👋 Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"\n❌ Erreur lors du lancement: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
