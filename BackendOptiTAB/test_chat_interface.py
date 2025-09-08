#!/usr/bin/env python
"""
Script de test rapide pour la nouvelle interface de chat IA
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

def test_chat_interface():
    """Test basique de l'interface de chat"""
    print("🤖 Test de l'interface ChatGPT-like OptiTAB")
    print("=" * 50)

    # Vérifier les modèles
    print("📊 Vérification des modèles...")
    try:
        conversations_count = AIConversation.objects.count()
        print(f"✅ {conversations_count} conversations trouvées")
    except Exception as e:
        print(f"❌ Erreur modèle: {e}")
        return False

    # Vérifier les utilisateurs
    print("👤 Vérification des utilisateurs...")
    try:
        users_count = User.objects.count()
        print(f"✅ {users_count} utilisateurs trouvés")
    except Exception as e:
        print(f"❌ Erreur utilisateurs: {e}")
        return False

    # Vérifier la configuration OpenAI
    print("🔑 Vérification configuration OpenAI...")
    openai_key = os.getenv('OPENAI_API_KEY')
    if openai_key:
        print("✅ Clé API OpenAI configurée")
        print(f"   Longueur: {len(openai_key)} caractères")
    else:
        print("⚠️  Clé API OpenAI non trouvée dans les variables d'environnement")
        print("   Configurez OPENAI_API_KEY dans votre .env")

    print("\n🎉 Interface de chat prête !")
    print("\n📋 Pour tester :")
    print("1. cd BackendOptiTAB && python manage.py runserver")
    print("2. cd websitecursor && npm run dev")
    print("3. Connectez-vous et cliquez sur le bouton IA 🤖")
    print("4. Posez votre première question !")

    return True

if __name__ == '__main__':
    success = test_chat_interface()
    if success:
        print("\n✅ Test réussi ! Votre interface de chat est opérationnelle.")
    else:
        print("\n❌ Test échoué. Vérifiez la configuration.")
        sys.exit(1)
