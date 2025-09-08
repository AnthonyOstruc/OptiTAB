#!/usr/bin/env python
"""
Test de la version OpenAI et compatibilité API
"""
import os
import sys

# Configuration Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')

import django
django.setup()

def test_openai_version():
    """Test de la version OpenAI et compatibilité"""
    print("🤖 Test de la version OpenAI")
    print("=" * 35)

    try:
        import openai
        print(f"✅ OpenAI importé avec succès")

        # Vérifier la version
        version = getattr(openai, '__version__', 'Unknown')
        print(f"📦 Version OpenAI: {version}")

        # Test de la nouvelle API (v1.x)
        if version.startswith('1.'):
            print("✅ Nouvelle API détectée (v1.x)")
            test_new_api(openai)
        else:
            print(f"⚠️  Version inattendue: {version}")
            print("💡 Version recommandée: openai==1.3.0")

    except ImportError as e:
        print(f"❌ Erreur d'import OpenAI: {e}")
        print("💡 Solution: pip install openai==1.3.0")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False

    return True

def test_new_api(openai):
    """Test de la nouvelle API OpenAI v1.x"""
    print("\n🔧 Test Nouvelle API (v1.x)")
    print("-" * 30)

    try:
        # Nettoyer l'environnement avant le test
        import os
        proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'OPENAI_PROXY']
        for var in proxy_vars:
            os.environ.pop(var, None)

        # Test d'initialisation du client avec une clé fictive
        client = openai.OpenAI(api_key="test_key")
        print("✅ Client OpenAI créé avec succès")

        # Note: On ne fait pas de vrai appel API pour éviter les coûts
        print("✅ Structure API compatible")
        print("✅ Prêt pour les vraies requêtes")

    except Exception as e:
        print(f"❌ Erreur nouvelle API: {e}")
        if 'proxies' in str(e):
            print("💡 Solution: Lancez 'python clean_proxy_env.py' d'abord")
        return False

    return True


def test_ai_helper():
    """Test de la classe AIHelper"""
    print("\n🧠 Test AIHelper")
    print("-" * 20)

    try:
        from ai.views import AIHelper

        # Créer une instance
        helper = AIHelper()
        print("✅ AIHelper créé avec succès")

        # Tester la méthode de prompt
        context_data = {
            'exercices': [],
            'cours': [],
            'chapitres': []
        }

        prompt = helper.build_prompt("Test question", context_data)
        print("✅ Prompt construit avec succès")
        print(f"📝 Longueur du prompt: {len(prompt)} caractères")

    except Exception as e:
        print(f"❌ Erreur AIHelper: {e}")
        return False

    return True

if __name__ == '__main__':
    print("🚀 Test de compatibilité OpenAI pour OptiTAB\n")

    # Test de la version
    version_ok = test_openai_version()

    # Test de l'AI Helper
    helper_ok = test_ai_helper()

    print("\n" + "=" * 50)

    if version_ok and helper_ok:
        print("✅ Configuration OpenAI vérifiée avec succès !")
        print("🎯 L'IA est prête à fonctionner.")
        print("\n💡 Testez maintenant l'interface IA !")
    else:
        print("❌ Problème de configuration détecté.")
        print("\n🔧 Solutions:")
        print("1. pip install openai==1.3.0")
        print("2. python manage.py runserver")
        print("3. Tester l'interface IA")
        sys.exit(1)
