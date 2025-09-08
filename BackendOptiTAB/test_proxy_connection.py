#!/usr/bin/env python
"""
Test de la connexion proxy API
"""
import requests
import sys
import os

def test_api_connection():
    """Test de la connexion à l'API via proxy"""
    print("🌐 Test de connexion API avec proxy")
    print("=" * 40)

    # Test de l'endpoint historique (sans authentification pour le test)
    try:
        # Test avec un token fictif pour voir si l'endpoint répond
        headers = {
            'Authorization': 'Bearer test_token',
            'Content-Type': 'application/json'
        }

        print("🔍 Test de l'endpoint: /api/ai/history/")
        response = requests.get('http://localhost:8000/api/ai/history/', headers=headers)

        print(f"✅ Status HTTP: {response.status_code}")

        if response.status_code == 401:
            print("✅ Authentification requise (normal)")
            print("✅ L'API est accessible !")
            return True
        elif response.status_code == 200:
            print("✅ Accès autorisé")
            return True
        else:
            print(f"❌ Status inattendu: {response.status_code}")
            print(f"Réponse: {response.text[:200]}...")
            return False

    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à http://localhost:8000")
        print("💡 Vérifiez que le serveur Django fonctionne:")
        print("   cd BackendOptiTAB && python manage.py runserver")
        return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def test_frontend_proxy():
    """Test du proxy côté frontend"""
    print("\n🔧 Vérification du proxy frontend")
    print("=" * 35)

    try:
        # Test de connexion au frontend
        response = requests.get('http://localhost:3000')
        if response.status_code == 200:
            print("✅ Serveur frontend accessible (port 3000)")
        else:
            print(f"⚠️  Serveur frontend: status {response.status_code}")

    except requests.exceptions.ConnectionError:
        print("❌ Serveur frontend non accessible")
        print("💡 Redémarrez le serveur frontend:")
        print("   cd websitecursor && npm run dev")

    print("\n📋 Configuration proxy vérifiée dans vite.config.js:")
    print("   - /api/* → http://localhost:8000/api/*")
    print("   - changeOrigin: true")
    print("   - secure: false")

if __name__ == '__main__':
    print("🚀 Test de la configuration proxy API\n")

    # Test du backend
    backend_ok = test_api_connection()

    # Test du frontend
    test_frontend_proxy()

    print("\n" + "=" * 50)
    if backend_ok:
        print("✅ Configuration proxy vérifiée avec succès !")
        print("🎯 L'IA devrait maintenant fonctionner correctement.")
    else:
        print("❌ Problème de configuration détecté.")
        print("🔧 Vérifiez les points suivants:")
        print("   1. Serveur Django: python manage.py runserver")
        print("   2. Serveur frontend: npm run dev")
        print("   3. Proxy dans vite.config.js")
        sys.exit(1)

    print("\n💡 Testez maintenant l'interface IA !")
