import os
import openai
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
import logging
from curriculum.models import MatiereContexte, Exercice
from cours.models import Cours
from .models import AIConversation
from .serializers import AIQuerySerializer, AIConversationSerializer


logger = logging.getLogger(__name__)


class AIHelper:
    """Classe utilitaire pour gérer les interactions avec l'IA"""

    def __init__(self):
        openai.api_key = getattr(settings, 'OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
        if not openai.api_key:
            raise ValueError("OPENAI_API_KEY non configurée")

    def search_relevant_content(self, matiere_contexte=None, chapitre=None, query=""):
        """Recherche du contenu pertinent dans la base de données"""
        context_data = {
            'exercices': [],
            'cours': [],
            'chapitres': []
        }

        # Recherche par chapitre spécifique
        if chapitre:
            exercices = Exercice.objects.filter(chapitre=chapitre)[:5]  # Limiter à 5 exercices
            cours = Cours.objects.filter(chapitre=chapitre).first()

            context_data['exercices'] = [
                {
                    'titre': ex.titre,
                    'question': ex.question,
                    'reponse_correcte': ex.reponse_correcte,
                    'etapes': ex.etapes or ""
                } for ex in exercices
            ]

            if cours:
                context_data['cours'] = {
                    'titre': cours.chapitre.titre,
                    'contenu': cours.contenu if hasattr(cours, 'contenu') else "",
                    'video_url': cours.video_url or ""
                }

        # Recherche par matière/contexte
        elif matiere_contexte:
            chapitres = Chapitre.objects.filter(
                notion__theme__contexte=matiere_contexte
            ).select_related('notion__theme')[:3]  # Limiter à 3 chapitres

            for chap in chapitres:
                exercices = Exercice.objects.filter(chapitre=chap)[:3]
                context_data['exercices'].extend([
                    {
                        'chapitre': chap.titre,
                        'titre': ex.titre,
                        'question': ex.question,
                        'reponse_correcte': ex.reponse_correcte,
                        'etapes': ex.etapes or ""
                    } for ex in exercices
                ])

        return context_data

    def build_prompt(self, user_query, context_data):
        """Construit le prompt pour ChatGPT"""
        system_prompt = """Tu es un assistant pédagogique intelligent pour la plateforme OptiTAB.
Tu aides les élèves dans leurs apprentissages scolaires en te basant sur le contenu disponible dans la base de données.

INSTRUCTIONS IMPORTANTES:
1. Réponds toujours en français
2. Sois pédagogique et encourageant
3. Utilise le contenu fourni pour étayer tes réponses
4. Si tu n'as pas assez d'informations, dis-le clairement
5. Propose des exercices supplémentaires si pertinent
6. Explique les concepts de manière claire et progressive

CONTEXTE DISPONIBLE:
"""

        # Ajouter les exercices au prompt
        if context_data['exercices']:
            system_prompt += "\nEXERCICES DISPONIBLES:\n"
            for i, ex in enumerate(context_data['exercices'], 1):
                system_prompt += f"\n{i}. {ex['titre']}\n"
                system_prompt += f"   Question: {ex['question']}\n"
                system_prompt += f"   Solution: {ex['reponse_correcte']}\n"
                if ex.get('etapes'):
                    system_prompt += f"   Étapes: {ex['etapes']}\n"

        # Ajouter les cours au prompt
        if context_data['cours']:
            system_prompt += f"\nCOURS DISPONIBLE:\n{context_data['cours']['contenu']}\n"

        return system_prompt

    def get_ai_response(self, user_query, context_data, model='gpt-3.5-turbo'):
        """Obtient la réponse de l'IA"""
        system_prompt = self.build_prompt(user_query, context_data)

        try:
            # Nettoyer les variables d'environnement proxy problématiques
            import os
            proxy_vars = ['HTTP_PROXY', 'HTTPS_PROXY', 'http_proxy', 'https_proxy', 'OPENAI_PROXY']
            for var in proxy_vars:
                os.environ.pop(var, None)

            logger.debug("Variables proxy nettoyées")

            # Utilisation de l'ancienne API OpenAI v0.28.1 (compatible proxy)
            logger.debug("Utilisation de l'ancienne API OpenAI v0.28.1")

            # Configurer la clé API
            api_key = getattr(settings, 'OPENAI_API_KEY', os.getenv('OPENAI_API_KEY'))
            if not api_key:
                raise ValueError("OPENAI_API_KEY non configurée. Ajoutez-la dans vos variables d'environnement.")

            logger.debug("Clé API trouvée, configuration OpenAI...")
            openai.api_key = api_key

            response = openai.ChatCompletion.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_query}
                ],
                max_tokens=1000,
                temperature=0.7
            )

            ai_response = response.choices[0].message.content
            tokens_used = response.usage.total_tokens

            return ai_response, tokens_used

        except Exception as e:
            error_msg = str(e)
            logger.error(f"Erreur OpenAI: {error_msg}")

            # Gestion spécifique de l'erreur de quota
            if "exceeded your current quota" in error_msg.lower():
                return """🚨 Crédits OpenAI épuisés

Votre quota OpenAI est dépassé. Voici les solutions :

1️⃣ **Ajouter des crédits** :
   • Allez sur https://platform.openai.com/account/billing
   • Cliquez sur "Add to credit balance"
   • Ajoutez au minimum 5$

2️⃣ **Utiliser GPT-3.5-turbo** :
   • Plus économique que GPT-4
   • Suffisant pour l'éducation

3️⃣ **Attendre la remise à zéro** :
   • Les crédits gratuits se renouvellent le 1er du mois

💡 Conseil : Commencez par ajouter 5$ pour continuer immédiatement !

📊 Estimation des coûts :
• Question simple : ~0.001$
• Explication détaillée : ~0.004$
• GPT-3.5-turbo : 10x moins cher que GPT-4""", 0

            return f"Erreur lors de la génération de la réponse: {error_msg}", 0


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def ask_ai(request):
    """Endpoint pour poser une question à l'IA"""
    serializer = AIQuerySerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    try:
        ai_helper = AIHelper()
    except ValueError as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Récupérer le contexte
    matiere_contexte = None
    chapitre = None

    if serializer.validated_data.get('matiere_contexte_id'):
        try:
            matiere_contexte = MatiereContexte.objects.get(
                id=serializer.validated_data['matiere_contexte_id']
            )
        except MatiereContexte.DoesNotExist:
            return Response({'error': 'Contexte matière non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    if serializer.validated_data.get('chapitre_id'):
        try:
            chapitre = Chapitre.objects.get(id=serializer.validated_data['chapitre_id'])
        except Chapitre.DoesNotExist:
            return Response({'error': 'Chapitre non trouvé'}, status=status.HTTP_404_NOT_FOUND)

    # Rechercher le contenu pertinent
    context_data = ai_helper.search_relevant_content(
        matiere_contexte=matiere_contexte,
        chapitre=chapitre,
        query=serializer.validated_data['message']
    )

    # Obtenir la réponse de l'IA
    model = serializer.validated_data.get('model', 'gpt-3.5-turbo')
    ai_response, tokens_used = ai_helper.get_ai_response(
        serializer.validated_data['message'],
        context_data,
        model
    )

    # Sauvegarder la conversation
    conversation = AIConversation.objects.create(
        user=request.user,
        message=serializer.validated_data['message'],
        ai_response=ai_response,
        contexte_matiere=matiere_contexte,
        contexte_chapitre=chapitre,
        tokens_used=tokens_used,
        model_used=model
    )

    # Retourner la réponse
    response_serializer = AIConversationSerializer(conversation)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_conversation_history(request):
    """Récupère l'historique des conversations de l'utilisateur"""
    conversations = AIConversation.objects.filter(user=request.user)
    serializer = AIConversationSerializer(conversations, many=True)
    return Response(serializer.data)