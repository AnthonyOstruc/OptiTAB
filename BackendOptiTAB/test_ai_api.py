#!/usr/bin/env python
"""
Script de test pour l'API IA OptiTAB
"""
import os
import django
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch, MagicMock

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')
django.setup()

from ai.models import AIConversation
from curriculum.models import MatiereContexte, Chapitre, Exercice

User = get_user_model()


class AIAPITestCase(APITestCase):
    """Tests pour l'API IA"""

    def setUp(self):
        """Configuration initiale des tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_authenticate(user=self.user)

    @patch('ai.views.AIHelper.get_ai_response')
    def test_ask_ai_success(self, mock_get_ai_response):
        """Test d'une requête IA réussie"""
        # Mock de la réponse OpenAI
        mock_get_ai_response.return_value = ("Ceci est une réponse de test", 150)

        payload = {
            'message': 'Explique-moi les équations du second degré',
            'model': 'gpt-3.5-turbo'
        }

        response = self.client.post('/api/ai/ask/', payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('ai_response', response.data)
        self.assertIn('message', response.data)

        # Vérifier que la conversation a été sauvegardée
        conversation = AIConversation.objects.filter(user=self.user).first()
        self.assertIsNotNone(conversation)
        self.assertEqual(conversation.message, payload['message'])
        self.assertEqual(conversation.ai_response, "Ceci est une réponse de test")

    def test_ask_ai_unauthenticated(self):
        """Test d'une requête IA sans authentification"""
        self.client.force_authenticate(user=None)

        payload = {
            'message': 'Test message'
        }

        response = self.client.post('/api/ai/ask/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ask_ai_missing_message(self):
        """Test d'une requête IA sans message"""
        payload = {}

        response = self.client.post('/api/ai/ask/', payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_conversation_history(self):
        """Test de récupération de l'historique des conversations"""
        # Créer quelques conversations de test
        AIConversation.objects.create(
            user=self.user,
            message='Question 1',
            ai_response='Réponse 1'
        )
        AIConversation.objects.create(
            user=self.user,
            message='Question 2',
            ai_response='Réponse 2'
        )

        response = self.client.get('/api/ai/history/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['message'], 'Question 2')  # Plus récente en premier


def run_tests():
    """Fonction pour exécuter les tests"""
    import unittest

    # Créer une suite de tests
    suite = unittest.TestLoader().loadTestsFromTestCase(AIAPITestCase)

    # Exécuter les tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    return result.wasSuccessful()


if __name__ == '__main__':
    print("🚀 Démarrage des tests API IA OptiTAB...")
    success = run_tests()

    if success:
        print("✅ Tous les tests sont passés !")
    else:
        print("❌ Certains tests ont échoué")

    print("\n📝 Note: Assurez-vous d'avoir configuré OPENAI_API_KEY dans vos variables d'environnement")
    print("🔧 pour les tests réels avec l'API OpenAI.")
