"""
Services utilitaires réutilisables pour éviter la duplication de code
"""
from django.core.mail import send_mail
from django.conf import settings
from django.db import models
from rest_framework.response import Response
from rest_framework import status
import logging
import random

logger = logging.getLogger(__name__)


class EmailService:
    """Service centralisé pour l'envoi d'emails"""
    
    @staticmethod
    def send_verification_code(user, code):
        """Envoi du code de vérification par email"""
        try:
            send_mail(
                subject='Code de vérification OptiTAB',
                message=f'Bonjour {user.first_name},\n\nVotre code de vérification est : {code}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Code de vérification envoyé à {user.email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi email à {user.email}: {e}")
            return False
    
    @staticmethod
    def send_password_reset(user, reset_link):
        """Envoi du lien de réinitialisation de mot de passe"""
        try:
            send_mail(
                subject='Réinitialisation de votre mot de passe OptiTAB',
                message=f'Bonjour {user.first_name},\n\nCliquez sur ce lien pour réinitialiser votre mot de passe : {reset_link}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f"Lien de réinitialisation envoyé à {user.email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi lien réinitialisation à {user.email}: {e}")
            return False


class ValidationService:
    """Service de validation réutilisable"""
    
    @staticmethod
    def generate_verification_code():
        """Génère un code de vérification à 6 chiffres"""
        return str(random.randint(100000, 999999))
    
    @staticmethod
    def validate_password_match(password1, password2):
        """Valide que les deux mots de passe correspondent"""
        if password1 != password2:
            raise ValueError("Les deux mots de passe ne correspondent pas")
        return True


class ResponseService:
    """Service pour standardiser les réponses API"""
    
    @staticmethod
    def success(message="Opération réussie", data=None, status_code=status.HTTP_200_OK):
        """Réponse de succès standardisée"""
        response_data = {"message": message, "success": True}
        if data is not None:
            response_data["data"] = data
        return Response(response_data, status=status_code)
    
    @staticmethod
    def error(message="Une erreur s'est produite", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Réponse d'erreur standardisée"""
        response_data = {"message": message, "success": False}
        if errors is not None:
            response_data["errors"] = errors
        return Response(response_data, status=status_code)
    
    @staticmethod
    def validation_error(errors):
        """Réponse d'erreur de validation standardisée"""
        return ResponseService.error(
            message="Erreurs de validation", 
            errors=errors, 
            status_code=status.HTTP_400_BAD_REQUEST
        )


class QuerySetService:
    """Service pour optimiser les requêtes en base"""
    
    @staticmethod
    def get_user_queryset():
        """QuerySet optimisé pour les utilisateurs avec leurs relations"""
        from users.models import CustomUser
        return CustomUser.objects.select_related('pays', 'niveau_pays')
    
    @staticmethod
    def get_curriculum_queryset():
        """QuerySet optimisé pour le curriculum avec toutes les relations"""
        from curriculum.models import Matiere
        return Matiere.objects.select_related('niveau__pays').prefetch_related('themes__notions__chapitres__exercices')


class BaseQuerySet(models.QuerySet):
    """QuerySet de base avec méthodes communes"""
    
    def active(self):
        """Filtre les éléments actifs"""
        return self.filter(est_actif=True)
    
    def by_ordre(self):
        """Tri par ordre puis nom/titre"""
        if hasattr(self.model, 'titre'):
            return self.order_by('ordre', 'titre')
        elif hasattr(self.model, 'nom'):
            return self.order_by('ordre', 'nom')
        return self.order_by('ordre')


class BaseManager(models.Manager):
    """Manager de base avec méthodes communes"""
    
    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)
    
    def active(self):
        """Retourne seulement les éléments actifs"""
        return self.get_queryset().active()
    
    def ordered(self):
        """Retourne les éléments triés par ordre"""
        return self.get_queryset().by_ordre()
    
    def active_ordered(self):
        """Retourne les éléments actifs triés par ordre"""
        return self.active().by_ordre()
