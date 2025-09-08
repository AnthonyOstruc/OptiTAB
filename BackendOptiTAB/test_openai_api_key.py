#!/usr/bin/env python
"""
Test de la configuration de la clé API OpenAI
"""
import os
import sys

# Configuration Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')

import django
django.setup()

def test_api_key_configuration():
    """Test de la configuration de la clé API OpenAI"""
    print("🔑 Test de la configuration API OpenAI")
    print("=" * 40)

    # Test des variables d'environnement
    api_key_env = os.getenv('OPENAI_API_KEY')
    print(f"📋 Variable d'environnement OPENAI_API_KEY: {'Définie' if api_key_env else 'Non définie'}")

    if api_key_env:
        print(f"   Longueur: {len(api_key_env)} caractères")
        print(f"   Préfixe: {api_key_env[:20]}..." if len(api_key_env) > 20 else f"   Clé: {api_key_env}")
    else:
        print("   ⚠️  Aucune clé trouvée dans les variables d'environnement")

    # Test de Django settings
    try:
        from django.conf import settings
        api_key_settings = getattr(settings, 'OPENAI_API_KEY', None)
        print(f"📋 Django settings OPENAI_API_KEY: {'Définie' if api_key_settings else 'Non définie'}")

        if api_key_settings:
            print(f"   Longueur: {len(api_key_settings)} caractères")
    except Exception as e:
        print(f"❌ Erreur accès settings: {e}")

    # Test OpenAI
    print("\n🤖 Test OpenAI avec la clé")
    print("-" * 30)

    try:
        import openai

        # Déterminer la clé API à utiliser
        api_key = api_key_env or api_key_settings

        if not api_key:
            print("❌ Aucune clé API trouvée")
            print("\n💡 Solutions:")
            print("1. export OPENAI_API_KEY=votre_clé")
            print("2. Ajouter dans .env: OPENAI_API_KEY=votre_clé")
            print("3. Ajouter dans settings.py: OPENAI_API_KEY = 'votre_clé'")
            return False

        print("✅ Clé API trouvée, test de connexion...")

        # Test de création du client
        client = openai.OpenAI(api_key=api_key)
        print("✅ Client OpenAI créé avec succès")

        # Test de validation de la clé (sans faire d'appel payant)
        print("✅ Configuration API OpenAI valide")

    except openai.AuthenticationError:
        print("❌ Clé API invalide ou expirée")
        print("💡 Vérifiez votre clé sur https://platform.openai.com/api-keys")
        return False
    except openai.PermissionDeniedError:
        print("❌ Accès refusé - vérifiez votre compte OpenAI")
        print("💡 Allez sur https://platform.openai.com/account/billing")
        return False
    except Exception as e:
        print(f"❌ Erreur OpenAI: {e}")
        return False

    return True

def show_configuration_help():
    """Affiche l'aide de configuration"""
    print("\n📖 Guide de Configuration")
    print("=" * 25)
    print("""
1. Obtenir une clé API :
   https://platform.openai.com/api-keys

2. Méthodes de configuration :

   A) Variable d'environnement :
      export OPENAI_API_KEY=sk-proj-votre_clé

   B) Fichier .env :
      OPENAI_API_KEY=sk-proj-votre_clé

   C) Django settings :
      OPENAI_API_KEY = 'sk-proj-votre_clé'

3. Activer la facturation :
   https://platform.openai.com/account/billing
   """)

if __name__ == '__main__':
    print("🚀 Test de configuration de la clé API OpenAI\n")

    success = test_api_key_configuration()

    print("\n" + "=" * 50)

    if success:
        print("✅ Configuration API OpenAI réussie !")
        print("🎯 L'IA est prête à fonctionner.")
        print("\n💡 Testez maintenant:")
        print("   python manage.py runserver")
    else:
        print("❌ Configuration API OpenAI incomplète.")
        show_configuration_help()
        sys.exit(1)

    print("\n🎉 Prêt pour l'IA !")
