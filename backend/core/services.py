"""
Services utilitaires réutilisables pour éviter la duplication de code
"""
from django.core.mail import send_mail, EmailMultiAlternatives
import os
from django.conf import settings
from django.db import models
from rest_framework.response import Response
from rest_framework import status
import logging
import random
from email.mime.image import MIMEImage
from pathlib import Path
import os

logger = logging.getLogger(__name__)


class EmailService:
    """Service centralisé pour l'envoi d'emails"""
    
    @staticmethod
    def _resolve_logo_url():
        """Retourne une URL https publique du logo si disponible.

        Priorité:
        1) EMAIL_LOGO_URL
        2) FRONTEND_URL + '/Logo_Fr.png' si FRONTEND_URL est https et non localhost
        """
        logo = getattr(settings, 'EMAIL_LOGO_URL', None)
        if logo and isinstance(logo, str) and logo.lower().startswith('http'):
            return logo
        # Fallback basé sur FRONTEND_URL
        frontend = getattr(settings, 'FRONTEND_URL', '') or getattr(settings, 'FRONTEND_BASE_URL', '')
        if isinstance(frontend, str) and frontend.lower().startswith('https://') and ('localhost' not in frontend and '127.0.0.1' not in frontend):
            return frontend.rstrip('/') + '/Logo_bg.png'
        return 'https://www.optitab.net/Logo_bg.png'
    
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

    @staticmethod
    def send_contact_message(first_name: str, last_name: str, email: str, subject: str, message: str, ticket_id: str | None = None) -> bool:
        """Envoie un message du formulaire de contact vers la boîte de réception OptiTAB.

        Utilise Reply-To pour permettre la réponse directe à l'expéditeur.
        """
        try:
            to_email = os.getenv("CONTACT_RECIPIENT", "contact@optitab.net")
            # Sujet standardisé avec préfixe
            subject_prefix = os.getenv("CONTACT_SUBJECT_PREFIX", "[Contact OptiTAB]")
            ticket_part = f" [Ticket {ticket_id}]" if ticket_id else ""
            final_subject = f"{subject_prefix}{ticket_part} {subject.strip()}".strip()

            # Corps texte brut
            text_body = (
                f"Nouveau message depuis le formulaire de contact OptiTAB\n\n"
                f"Nom: {first_name.strip()} {last_name.strip()}\n"
                f"Email: {email.strip()}\n\n"
                f"Ticket: {ticket_id}\n\n" if ticket_id else ""
                f"Message:\n{message.strip()}\n"
            )

            # Variante HTML simple (avec logo si défini)
            logo_url = EmailService._resolve_logo_url()
            html_body = f"""
                <div>
                  {f'<p><img src="{logo_url}" alt="OptiTAB" style="height:64px;width:auto;display:block;-ms-interpolation-mode:bicubic"/></p>' if logo_url else ''}
                  <p><strong>Nouveau message depuis le formulaire de contact OptiTAB</strong></p>
                  {f'<p style="margin:6px 0 12px 0"><strong>Ticket:</strong> {ticket_id}</p>' if ticket_id else ''}
                  <p><strong>Nom:</strong> {first_name.strip()} {last_name.strip()}<br/>
                     <strong>Email:</strong> {email.strip()}</p>
                  <p><strong>Message:</strong><br/>{message.strip().replace('\n', '<br/>')}</p>
                  <hr style="border:none;border-top:1px solid #eee;margin:16px 0"/>
                  <table role="presentation" style="width:100%;max-width:520px;margin-top:16px">
                    <tr>
                      <td style="vertical-align:middle;padding-right:12px">
                        {f'<img src="{EmailService._resolve_logo_url()}" alt="OptiTAB" style="height:56px;width:auto;display:block"/>' if EmailService._resolve_logo_url() else ''}
                      </td>
                      <td style="vertical-align:middle;color:#6b7280;font-size:12px;line-height:1.5">
                        OptiTAB • Plateforme d\'apprentissage<br/>
                        <a href="https://www.optitab.net" style="color:#6b7280;text-decoration:none">www.optitab.net</a> • contact@optitab.net
                      </td>
                    </tr>
                  </table>
                </div>
            """

            email_msg = EmailMultiAlternatives(
                subject=final_subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email],
                reply_to=[email.strip()] if email else None,
            )
            email_msg.attach_alternative(html_body, "text/html")
            email_msg.send(fail_silently=False)
            logger.info("Message de contact envoyé à %s", to_email)
            return True
        except Exception as e:
            logger.error("Erreur lors de l'envoi du message de contact: %s", e)
            return False

    @staticmethod
    def send_contact_confirmation(to_email: str, first_name: str, subject: str, original_message: str = "", ticket_id: str | None = None) -> bool:
        """Envoie un email de confirmation à l'expéditeur du formulaire.

        Indique que le message a été reçu et que la réponse interviendra sous 24h.
        """
        try:
            display_name = (first_name or "").strip() or ""
            base_subject = os.getenv("CONTACT_CONFIRMATION_SUBJECT", "Nous avons bien reçu votre message - OptiTAB")
            ticket_part = f" [Ticket {ticket_id}]" if ticket_id else ""
            final_subject = f"{base_subject}{ticket_part}"

            text_body = (
                f"Bonjour {display_name},\n\n"
                f"Merci pour votre message. Nous l'avons bien reçu concernant \"{subject}\".\n"
                + (f"Numéro de ticket: {ticket_id}\n" if ticket_id else "") +
                f"Notre équipe vous répondra sous 24 heures (jours ouvrés).\n\n"
                f"Pour toute urgence, vous pouvez nous écrire à contact@optitab.net ou \n"
                f"nous joindre sur WhatsApp au 07 64 04 02 51.\n\n"
                f"Copie de votre message:\n{(original_message or '').strip()}\n\n"
                f"Cordialement,\nL'équipe OptiTAB\nhttps://www.optitab.net\n"
            )

            logo_url = EmailService._resolve_logo_url()
            original_html = (original_message or '').strip().replace('\n', '<br/>')
            html_body = f"""
                <div style="font-family:Arial,Helvetica,sans-serif;font-size:14px;color:#111">
                  {f'<p><img src="{logo_url}" alt="OptiTAB" style="height:64px;width:auto;display:block;-ms-interpolation-mode:bicubic"/></p>' if logo_url else ''}
                  <p>Bonjour {display_name},</p>
                  <p>Merci pour votre message. Nous l'avons bien reçu concernant <strong>{subject}</strong>.<br/>
                     Notre équipe vous répondra sous <strong>24 heures</strong> (jours ouvrés).</p>
                  {f'<p style="margin:6px 0 12px 0"><strong>Numéro de ticket:</strong> {ticket_id}</p>' if ticket_id else ''}
                  <p>Pour toute urgence, écrivez-nous à <a href="mailto:contact@optitab.net">contact@optitab.net</a>
                     ou contactez-nous sur WhatsApp au <a href="https://wa.me/33764040251" target="_blank">07 64 04 02 51</a>.</p>
                  <hr style="border:none;border-top:1px solid #eee;margin:16px 0"/>
                  <p style="margin:0 0 8px 0"><strong>Copie de votre message :</strong></p>
                  <p style="white-space:pre-wrap;margin:0">{original_html}</p>
                  <hr style="border:none;border-top:1px solid #eee;margin:16px 0"/>
                  <p style="color:#555">Cordialement,<br/>L'équipe OptiTAB<br/>
                     <a href="https://www.optitab.net">www.optitab.net</a></p>
                  <table role="presentation" style="width:100%;max-width:520px;margin-top:16px">
                    <tr>
                      <td style="vertical-align:middle;padding-right:12px">
                        {f'<img src="{EmailService._resolve_logo_url()}" alt="OptiTAB" style="height:56px;width:auto;display:block"/>' if EmailService._resolve_logo_url() else ''}
                      </td>
                      <td style="vertical-align:middle;color:#6b7280;font-size:12px;line-height:1.5">
                        OptiTAB • Plateforme d\'apprentissage<br/>
                        <a href="https://www.optitab.net" style="color:#6b7280;text-decoration:none">www.optitab.net</a> • contact@optitab.net
                      </td>
                    </tr>
                  </table>
                </div>
            """

            from_email = settings.DEFAULT_FROM_EMAIL
            reply_to = [os.getenv("CONTACT_RECIPIENT", "contact@optitab.net")]

            email_msg = EmailMultiAlternatives(
                subject=final_subject,
                body=text_body,
                from_email=from_email,
                to=[to_email],
                reply_to=reply_to,
            )
            email_msg.attach_alternative(html_body, "text/html")
            email_msg.send(fail_silently=False)
            logger.info("Email de confirmation envoyé à %s", to_email)
            return True
        except Exception as e:
            logger.error("Erreur lors de l'envoi de l'email de confirmation: %s", e)
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
        # Chapitres supprimés → précharger directement via Notion
        return (
            Matiere.objects
            .select_related('niveau__pays')
            .prefetch_related(
                'themes__notions__exercices',
                'themes__notions__cours',
                'themes__notions__quiz',
            )
        )


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
