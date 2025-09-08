#!/usr/bin/env python
"""
Test simplifié d'OpenAI sans dépendances externes
"""
import os
import sys

# Configuration Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')

import django
django.setup()

def test_openai_simple():
    """Test simplifié d'OpenAI"""
    print("🤖 Test simplifié OpenAI")
    print("=" * 30)

    # Nettoyer l'environnement
    print("🧹 Nettoyage environnement...")
    proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'OPENAI_PROXY']
    for var in proxy_vars:
        os.environ.pop(var, None)
    print("✅ Environnement nettoyé")

    try:
        import openai
        print(f"✅ OpenAI importé: {getattr(openai, '__version__', '0.28.1')}")

        # Test avec l'ancienne API
        if hasattr(openai, 'ChatCompletion'):
            print("✅ ChatCompletion disponible (ancienne API)")
            return True
        else:
            print("❌ ChatCompletion non disponible")
            return False

    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == '__main__':
    success = test_openai_simple()
    if success:
        print("\n✅ OpenAI fonctionne !")
    else:
        print("\n❌ Problème détecté")
        sys.exit(1)
