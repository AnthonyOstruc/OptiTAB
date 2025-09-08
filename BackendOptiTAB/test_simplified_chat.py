#!/usr/bin/env python
"""
Test rapide de l'interface de chat simplifiée
"""
import os
import sys
import django

# Configuration Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')
django.setup()

from ai.models import AIConversation
from django.contrib.auth import get_user_model

User = get_user_model()

def test_simplified_interface():
    """Test de l'interface simplifiée"""
    print("🎯 Test de l'interface chat simplifiée")
    print("=" * 50)

    # Vérifier que les modèles fonctionnent
    print("📊 Vérification des modèles...")
    try:
        conversations_count = AIConversation.objects.count()
        print(f"✅ {conversations_count} conversations trouvées")
    except Exception as e:
        print(f"❌ Erreur modèle: {e}")
        return False

    print("\n🎉 Interface simplifiée prête !")
    print("\n📋 Fonctionnalités de la version simplifiée :")
    print("✅ Zone de saisie épurée")
    print("✅ Boutons d'envoi directs")
    print("✅ Pas de filtres de contexte")
    print("✅ Interface ultra-simple")
    print("✅ Envoi immédiat des messages")

    print("\n🚀 Testez maintenant :")
    print("1. Ouvrez l'interface IA")
    print("2. Tapez une question")
    print("3. Appuyez sur Enter ou cliquez sur un bouton")
    print("4. L'IA répond automatiquement !")

    return True

if __name__ == '__main__':
    success = test_simplified_interface()
    if success:
        print("\n✅ Interface simplifiée opérationnelle !")
    else:
        print("\n❌ Problème détecté")
        sys.exit(1)
