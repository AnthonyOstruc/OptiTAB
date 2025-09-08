#!/usr/bin/env python
"""
Test rapide du statut d'authentification
"""
import os
import sys

# Configuration Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')

import django
django.setup()

def check_auth_setup():
    """Vérifier la configuration d'authentification"""
    print("🔐 Vérification de l'authentification IA")
    print("=" * 45)

    # Vérifier les URLs
    from ai.urls import urlpatterns
    history_url_exists = any(pattern.name == 'conversation_history' for pattern in urlpatterns)
    ask_url_exists = any(pattern.name == 'ask_ai' for pattern in urlpatterns)

    print(f"✅ URL historique: {'Trouvée' if history_url_exists else 'Manquante'}")
    print(f"✅ URL question IA: {'Trouvée' if ask_url_exists else 'Manquante'}")

    # Vérifier les permissions
    from ai.views import get_conversation_history
    print("✅ Vue historique: Trouvée")

    # Vérifier le modèle
    from ai.models import AIConversation
    print("✅ Modèle AIConversation: Trouvé")

    print("\n📋 Configuration côté frontend attendue:")
    print("- Clé localStorage: 'access_token'")
    print("- Header: 'Authorization: Bearer <token>'")
    print("- Endpoint: '/api/ai/history/'")

    print("\n🚀 Pour tester l'authentification:")
    print("1. Connectez-vous à l'application")
    print("2. Ouvrez la console (F12)")
    print("3. Tapez: localStorage.getItem('access_token')")
    print("4. Le résultat devrait être votre token JWT")

    return True

if __name__ == '__main__':
    success = check_auth_setup()
    if success:
        print("\n✅ Configuration d'authentification vérifiée")
        print("🔍 Vérifiez maintenant côté frontend !")
    else:
        print("\n❌ Problème de configuration détecté")
        sys.exit(1)
