#!/usr/bin/env python
"""
Test de l'endpoint historique IA
"""
import os
import sys

# Configuration Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')

import django
django.setup()

from ai.models import AIConversation
from django.contrib.auth import get_user_model

User = get_user_model()

def test_ai_history_endpoint():
    """Test rapide de l'endpoint historique"""
    print("🔍 Test de l'endpoint historique IA")
    print("=" * 40)

    # Vérifier que l'endpoint existe
    from ai.views import get_conversation_history
    print("✅ Fonction get_conversation_history trouvée")

    # Vérifier le modèle
    try:
        conversations_count = AIConversation.objects.count()
        print(f"✅ {conversations_count} conversations dans la base")
    except Exception as e:
        print(f"❌ Erreur modèle: {e}")
        return False

    print("\n📋 L'endpoint devrait retourner:")
    print("- Status: 200")
    print("- Content-Type: application/json")
    print("- Body: [] (tableau vide si pas d'historique)")

    print("\n🚀 Testez maintenant:")
    print("1. Ouvrez la console du navigateur (F12)")
    print("2. Allez dans l'onglet Network")
    print("3. Ouvrez l'interface IA")
    print("4. Cherchez la requête vers '/api/ai/history/'")

    return True

if __name__ == '__main__':
    success = test_ai_history_endpoint()
    if success:
        print("\n✅ Test terminé - vérifiez les logs du navigateur")
    else:
        print("\n❌ Problème détecté")
        sys.exit(1)
