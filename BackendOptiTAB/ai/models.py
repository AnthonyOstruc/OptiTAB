from django.db import models
from django.contrib.auth import get_user_model
from core.models import BaseContent

User = get_user_model()

class AIConversation(BaseContent):
    """Conversation avec l'IA"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_conversations')
    message = models.TextField(verbose_name="Message de l'utilisateur")
    ai_response = models.TextField(verbose_name="Réponse de l'IA")
    contexte_matiere = models.ForeignKey('curriculum.MatiereContexte', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_conversations')
    contexte_chapitre = models.ForeignKey('curriculum.Chapitre', on_delete=models.SET_NULL, null=True, blank=True, related_name='ai_conversations')

    # Métadonnées
    tokens_used = models.PositiveIntegerField(default=0, verbose_name="Tokens utilisés")
    model_used = models.CharField(max_length=50, default='gpt-3.5-turbo', verbose_name="Modèle IA utilisé")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Conversation IA"
        verbose_name_plural = "Conversations IA"
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['contexte_matiere']),
            models.Index(fields=['contexte_chapitre']),
        ]

    def __str__(self):
        return f"IA - {self.user.username} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"