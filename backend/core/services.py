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
from django.utils import timezone

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
        def _append_version(url: str) -> str:
            version = os.getenv('EMAIL_LOGO_VERSION') or os.getenv('ASSET_VERSION')
            if not version and getattr(settings, 'DEBUG', False):
                import time as _t
                version = str(int(_t.time()))
            return f"{url}{'&' if '?' in url else '?'}v={version}" if version else url

        logo = getattr(settings, 'EMAIL_LOGO_URL', None)
        if logo and isinstance(logo, str) and logo.lower().startswith('http'):
            return _append_version(logo)
        # Fallback basé sur FRONTEND_URL
        frontend = getattr(settings, 'FRONTEND_URL', '') or getattr(settings, 'FRONTEND_BASE_URL', '')
        if isinstance(frontend, str) and frontend.lower().startswith('https://') and ('localhost' not in frontend and '127.0.0.1' not in frontend):
            return _append_version(frontend.rstrip('/') + '/Logo_bg.png')
        return _append_version('https://www.optitab.net/Logo_bg.png')

    @staticmethod
    def _get_stripe_mode_label():
        secret_key = (os.getenv('STRIPE_SECRET_KEY') or '').strip().lower()
        if secret_key.startswith('sk_live_'):
            return 'LIVE'
        if secret_key.startswith('sk_test_'):
            return 'TEST'
        return 'UNKNOWN'

    @staticmethod
    def _count_active_subscriptions_on_stripe():
        mode_label = EmailService._get_stripe_mode_label()
        try:
            import stripe

            stripe.api_key = os.environ.get('STRIPE_SECRET_KEY')
            count = 0

            for status_key in ('active', 'trialing'):
                subscription_page = stripe.Subscription.list(status=status_key, limit=100)
                if hasattr(subscription_page, 'auto_paging_iter'):
                    iterator = subscription_page.auto_paging_iter()
                else:
                    iterator = getattr(subscription_page, 'data', []) or []

                for subscription in iterator:
                    if isinstance(subscription, dict):
                        cancel_at_period_end = bool(subscription.get('cancel_at_period_end', False))
                    else:
                        cancel_at_period_end = bool(getattr(subscription, 'cancel_at_period_end', False))
                    if not cancel_at_period_end:
                        count += 1

            return {
                'count': count,
                'mode_label': mode_label,
                'error_message': None,
            }
        except Exception as exc:
            error_message = str(exc) or exc.__class__.__name__
            logger.warning(
                "Stripe count unavailable for admin emails (mode=%s): %s",
                mode_label,
                error_message,
            )
            return {
                'count': None,
                'mode_label': mode_label,
                'error_message': error_message,
            }

    @staticmethod
    def _format_active_subscribers_for_email(stats):
        count = (stats or {}).get('count')
        if count is None:
            return 'Indisponible'
        return str(count)
    
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
    def send_verification_link(user, verification_link):
        """Envoie un lien de vérification d'email."""
        first_name = (user.first_name or '').strip() or 'OptiTABien'
        plain_message = (
            f"Bonjour {first_name},\n\n"
            "Merci de confirmer votre adresse email OptiTAB.\n"
            "Cliquez sur le lien ci-dessous pour valider votre email :\n"
            f"{verification_link}\n\n"
            "Ce lien expire dans 24 heures.\n\n"
            "À très vite,\nL'équipe OptiTAB"
        )

        logo_url = EmailService._resolve_logo_url()
        html_message = f"""
            <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                <tr>
                  <td style="padding:24px 24px 0 24px;">
                    {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                    <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;">Confirmez votre email</h1>
                    <p style="margin:0;color:#4b5563;font-size:15px;line-height:1.6;">
                      Bonjour {first_name},<br/>
                      Merci de confirmer votre adresse email pour sécuriser votre compte.
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:24px;">
                    <a href="{verification_link}" style="display:inline-block;background:#4f46e5;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 24px;border-radius:10px;">
                      Confirmer mon email
                    </a>
                    <p style="margin:16px 0 0 0;color:#6b7280;font-size:13px;line-height:1.6;">
                      Ce lien est valable pendant 24 heures. Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :
                    </p>
                    <p style="margin:12px 0 0 0;color:#2563eb;font-size:13px;word-break:break-all;">
                      <a href="{verification_link}" style="color:#2563eb;text-decoration:none;">{verification_link}</a>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 24px;background:#f3f4f6;color:#6b7280;font-size:12px;">
                    L'équipe OptiTAB<br/>
                    <a href="mailto:contact@optitab.net" style="color:#4f46e5;text-decoration:none;">contact@optitab.net</a>
                  </td>
                </tr>
              </table>
            </div>
        """.strip()

        try:
            email_message = EmailMultiAlternatives(
                subject='Confirmez votre email OptiTAB',
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email_message.attach_alternative(html_message, "text/html")
            email_message.send(fail_silently=False)
            logger.info(f"Lien de vérification envoyé à {user.email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi lien de vérification à {user.email}: {e}")
            return False
    
    @staticmethod
    def send_email_change_link(user, new_email, verification_link):
        """Envoie un lien de confirmation pour changer d'adresse email."""
        display_name = (user.first_name or '').strip() or 'OptiTABien'
        plain_message = (
            f"Bonjour {display_name},\n\n"
            f"Vous avez demandé à remplacer votre adresse email OptiTAB par {new_email}.\n"
            "Cliquez sur le lien ci-dessous pour confirmer ce changement :\n"
            f"{verification_link}\n\n"
            "Ce lien expire dans 24 heures. Si vous n'êtes pas à l'origine de cette demande, ignorez cet email.\n\n"
            "À très vite,\nL'équipe OptiTAB"
        )
        logo_url = EmailService._resolve_logo_url()
        html_message = f"""
            <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                <tr>
                  <td style="padding:24px 24px 0 24px;">
                    {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                    <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;">Confirmez votre nouvelle adresse email</h1>
                    <p style="margin:0;color:#4b5563;font-size:15px;line-height:1.6;">
                      Bonjour {display_name},<br/>
                      Cliquez sur le bouton ci-dessous pour confirmer votre nouvelle adresse email.
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:24px;">
                    <a href="{verification_link}" style="display:inline-block;background:#6366f1;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 24px;border-radius:10px;">
                      Confirmer mon nouvel email
                    </a>
                    <p style="margin:16px 0 0 0;color:#6b7280;font-size:13px;line-height:1.6;">
                      Nouveau mail : <strong style="color:#111827;">{new_email}</strong><br/>
                      Si le bouton ne fonctionne pas, copiez-collez ce lien dans votre navigateur :
                    </p>
                    <p style="margin:12px 0 0 0;color:#2563eb;font-size:13px;word-break:break-all;">
                      <a href="{verification_link}" style="color:#2563eb;text-decoration:none;">{verification_link}</a>
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:16px 24px;background:#f3f4f6;color:#6b7280;font-size:12px;">
                    Si vous n'êtes pas à l'origine de cette demande, vous pouvez ignorer cet email.
                  </td>
                </tr>
              </table>
            </div>
        """.strip()

        try:
            email_message = EmailMultiAlternatives(
                subject='Confirmation de changement d\'email OptiTAB',
                body=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[new_email],
            )
            email_message.attach_alternative(html_message, "text/html")
            email_message.send(fail_silently=False)
            logger.info("Lien de changement d'email envoyé à %s", new_email)
            return True
        except Exception as e:
            logger.error("Erreur envoi lien de changement d'email à %s: %s", new_email, e)
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
    def send_invoice_receipt(user, payment_history, invoice_link):
        """Envoie un email contenant la facture Stripe."""
        first_name = (user.first_name or '').strip() or 'OptiTABien'
        date_str = timezone.localtime(payment_history.created_at).strftime('%d %B %Y')
        amount_str = f"{payment_history.amount:.2f} {payment_history.currency.upper()}"
        subject = 'Votre facture OptiTAB'

        text_body = (
            f"Bonjour {first_name},\n\n"
            f"Voici la facture correspondant à votre paiement du {date_str} "
            f"d'un montant de {amount_str}.\n\n"
            f"Téléchargez-la en suivant ce lien sécurisé :\n{invoice_link}\n\n"
            "Merci pour votre confiance.\nL'équipe OptiTAB"
        )

        html_body = f"""
            <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                <tr>
                  <td style="padding:24px;">
                    <h1 style="margin:0 0 12px 0;font-size:20px;color:#111827;">Votre facture est disponible</h1>
                    <p style="margin:0 0 16px 0;color:#4b5563;font-size:15px;line-height:1.6;">
                      Bonjour {first_name},<br/>
                      Voici la facture correspondant à votre paiement du {date_str} (montant {amount_str}).
                    </p>
                    <a href="{invoice_link}" style="display:inline-block;background:#22c55e;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 24px;border-radius:10px;">
                      Télécharger ma facture
                    </a>
                    <p style="margin:16px 0 0 0;color:#6b7280;font-size:13px;line-height:1.6;">
                      Si le bouton ne fonctionne pas, copiez ce lien dans votre navigateur :<br/>
                      <a href="{invoice_link}" style="color:#2563eb;text-decoration:none;">{invoice_link}</a>
                    </p>
                  </td>
                </tr>
              </table>
            </div>
        """

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_body, "text/html")
        email.send(fail_silently=False)

    @staticmethod
    def send_gift_subscription_notification(recipient, gifter, plan, niveau=None):
        """Envoie une notification à un élève lorsqu'un parent lui offre un abonnement."""
        try:
            first_name = (recipient.first_name or '').strip() or 'OptiTABien'
            gifter_name = (gifter.first_name or '').strip() or 'Quelqu\'un'
            plan_name = getattr(plan, 'name', None) or getattr(plan, 'titre', None) or 'OptiTAB Premium'
            niveau_name = ''
            if niveau:
                niveau_name = getattr(niveau, 'nom', '') or ''
                if hasattr(niveau, 'pays') and niveau.pays:
                    pays_name = getattr(niveau.pays, 'nom', '')
                    if pays_name:
                        niveau_name = f"{niveau_name} ({pays_name})"
            
            subject = '🎁 Vous avez reçu un abonnement OptiTAB !'
            
            text_body = (
                f"Bonjour {first_name},\n\n"
                f"Bonne nouvelle ! {gifter_name} vous a offert un abonnement {plan_name} sur OptiTAB.\n\n"
            )
            if niveau_name:
                text_body += f"Niveau : {niveau_name}\n\n"
            text_body += (
                "Votre accès premium est maintenant activé. "
                "Connectez-vous à votre compte pour profiter de tous les cours, exercices et fonctionnalités.\n\n"
                "À très vite sur OptiTAB !\n"
                "L'équipe OptiTAB"
            )
            
            logo_url = EmailService._resolve_logo_url()
            frontend_url = getattr(settings, 'FRONTEND_URL', '') or 'https://www.optitab.net'
            
            html_body = f"""
                <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                    <tr>
                      <td style="padding:24px 24px 0 24px;">
                        {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                        <div style="text-align:center;margin-bottom:20px;">
                          <span style="font-size:48px;">🎁</span>
                        </div>
                        <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;text-align:center;">Vous avez reçu un cadeau !</h1>
                        <p style="margin:0 0 16px 0;color:#4b5563;font-size:15px;line-height:1.6;text-align:center;">
                          {gifter_name} vous a offert un abonnement <strong>{plan_name}</strong>
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0 24px 24px 24px;">
                        <div style="background:linear-gradient(135deg,#eef2ff 0%,#e0e7ff 100%);border-radius:12px;padding:20px;margin-bottom:20px;">
                          <p style="margin:0;color:#312e81;font-size:15px;line-height:1.6;">
                            <strong>Votre accès premium est activé</strong><br/>
                            Profitez de tous les cours, exercices corrigés et fonctionnalités avancées.
                          </p>
                          {f'<p style="margin:12px 0 0 0;color:#4338ca;font-size:14px;"><strong>Niveau :</strong> {niveau_name}</p>' if niveau_name else ''}
                        </div>
                        <div style="text-align:center;">
                          <a href="{frontend_url}/dashboard" style="display:inline-block;background:#4f46e5;color:#ffffff;text-decoration:none;font-weight:600;padding:14px 28px;border-radius:10px;font-size:15px;">
                            Accéder à mon espace
                          </a>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:16px 24px;background:#f9fafb;border-top:1px solid #e5e7eb;">
                        <p style="margin:0;color:#6b7280;font-size:13px;line-height:1.6;text-align:center;">
                          Merci de faire confiance à OptiTAB pour réussir en maths !
                        </p>
                      </td>
                    </tr>
                  </table>
                </div>
            """
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[recipient.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)
            
            logger.info(f"Email cadeau abonnement envoyé à {recipient.email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi email cadeau abonnement à {recipient.email}: {e}")
            return False

    @staticmethod
    def send_gift_purchase_confirmation(payer, recipient, plan, niveau=None, is_pass=False, invoice_link=None):
        """Envoie une confirmation au payeur lorsqu'il offre un abonnement ou un pass."""
        try:
            payer_name = (getattr(payer, 'first_name', '') or '').strip() or 'OptiTABien'
            recipient_first = (getattr(recipient, 'first_name', '') or '').strip()
            recipient_last = (getattr(recipient, 'last_name', '') or '').strip()
            recipient_name = ' '.join([p for p in [recipient_first, recipient_last] if p]).strip()
            if not recipient_name:
                recipient_name = getattr(recipient, 'email', '') or 'votre enfant'

            plan_name = getattr(plan, 'name', None) or getattr(plan, 'titre', None) or 'OptiTAB Premium'
            kind_label = 'pass' if is_pass else 'abonnement'
            invoice_link = (invoice_link or '').strip() or None

            niveau_name = ''
            if niveau:
                niveau_name = getattr(niveau, 'nom', '') or ''
                if hasattr(niveau, 'pays') and niveau.pays:
                    pays_name = getattr(niveau.pays, 'nom', '')
                    if pays_name:
                        niveau_name = f"{niveau_name} ({pays_name})"

            subject = 'Confirmation de votre cadeau OptiTAB'
            text_body = (
                f"Bonjour {payer_name},\n\n"
                f"Votre {kind_label} {plan_name} a bien été offert à {recipient_name}.\n"
            )
            if niveau_name:
                text_body += f"Niveau : {niveau_name}\n"
            text_body += "\n"

            logo_url = EmailService._resolve_logo_url()
            frontend_url = getattr(settings, 'FRONTEND_URL', '') or 'https://www.optitab.net'
            frontend_base = frontend_url.rstrip('/')
            subscription_url = f"{frontend_base}/subscription"
            recipient_line = f"<strong>{recipient_name}</strong>" if recipient_name else "votre enfant"
            level_line = f'<p style="margin:6px 0 0 0;color:#4338ca;font-size:14px;"><strong>Niveau :</strong> {niveau_name}</p>' if niveau_name else ''

            if invoice_link:
                text_body += (
                    "\nVotre reçu / facture est disponible :\n"
                    f"{invoice_link}\n"
                )
            text_body += (
                f"\nEspace Abonnement : {subscription_url}\n\n"
                "Merci pour votre confiance,\n"
                "L'équipe OptiTAB"
            )

            receipt_block = ""
            if invoice_link:
                receipt_block = f"""
                        <div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin-bottom:20px;text-align:center;">
                          <p style="margin:0 0 12px 0;color:#111827;font-size:14px;line-height:1.6;">
                            <strong>Télécharger votre reçu</strong>
                          </p>
                          <a href="{invoice_link}" style="display:inline-block;background:#2563eb;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 24px;border-radius:10px;font-size:15px;">
                            Télécharger le reçu
                          </a>
                          <p style="margin:12px 0 0 0;color:#6b7280;font-size:12px;line-height:1.6;">
                            Si le bouton ne fonctionne pas :<br/>
                            <a href="{invoice_link}" style="color:#2563eb;text-decoration:none;word-break:break-all;">{invoice_link}</a>
                          </p>
                        </div>
                """

            html_body = f"""
                <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                    <tr>
                      <td style="padding:24px 24px 0 24px;">
                        {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                        <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;text-align:center;">Cadeau confirmé</h1>
                        <p style="margin:0 0 16px 0;color:#4b5563;font-size:15px;line-height:1.6;text-align:center;">
                          Vous avez offert un {kind_label} <strong>{plan_name}</strong> à {recipient_line}.
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0 24px 24px 24px;">
                        <div style="background:linear-gradient(135deg,#eef2ff 0%,#e0e7ff 100%);border-radius:12px;padding:20px;margin-bottom:20px;">
                          <p style="margin:0;color:#312e81;font-size:15px;line-height:1.6;">
                            Votre cadeau est bien pris en compte et l'accès est activé pour le bénéficiaire.
                          </p>
                          {level_line}
                        </div>
                        {receipt_block}
                        <div style="text-align:center;">
                          <a href="{subscription_url}" style="display:inline-block;background:#4f46e5;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 24px;border-radius:10px;font-size:15px;">
                            Voir mes abonnements
                          </a>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:16px 24px;background:#f9fafb;border-top:1px solid #e5e7eb;">
                        <p style="margin:0;color:#6b7280;font-size:13px;line-height:1.6;text-align:center;">
                          Merci de faire confiance à OptiTAB.
                        </p>
                      </td>
                    </tr>
                  </table>
                </div>
            """

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[payer.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)
            logger.info("Email confirmation cadeau envoyé à %s", payer.email)
            return True
        except Exception as e:
            logger.error("Erreur envoi email confirmation cadeau à %s: %s", getattr(payer, 'email', None), e)
            return False

    @staticmethod
    def send_quiz_grade_notification(user, quiz_title, note, commentaire='', notion_id=None):
        """Envoie une notification par email lorsqu'un quiz est noté"""
        from django.conf import settings
        first_name = (user.first_name or '').strip() or 'OptiTABien'
        note_formatted = f"{note:.2f}/20"
        subject = f'Votre quiz "{quiz_title}" a été corrigé'

        # Construire l'URL vers la correction (avec ouverture automatique de l'onglet Solution)
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        correction_url = f"{frontend_url}/quiz-notion/{notion_id}?tab=solution" if notion_id else None

        text_body = (
            f"Bonjour {first_name},\n\n"
            f"Votre quiz \"{quiz_title}\" a été corrigé.\n\n"
            f"Note obtenue : {note_formatted}\n"
        )
        
        if commentaire:
            text_body += f"\nCommentaire du professeur :\n{commentaire}\n"
        
        if correction_url:
            text_body += f"\nConsultez votre correction : {correction_url}\n"
        
        text_body += (
            "\nVous pouvez consulter vos résultats dans votre espace personnel.\n\n"
            "Bon courage pour la suite !\nL'équipe OptiTAB"
        )

        logo_url = EmailService._resolve_logo_url()
        commentaire_html = f"""
            <div style="background:#f3f4f6;padding:16px;border-radius:8px;margin:16px 0;">
              <p style="margin:0;color:#374151;font-size:14px;line-height:1.6;font-style:italic;">
                "{commentaire}"
              </p>
            </div>
        """ if commentaire else ""

        html_body = f"""
            <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                <tr>
                  <td style="padding:24px 24px 0 24px;">
                    {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                    <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;">Quiz corrigé ✅</h1>
                    <p style="margin:0;color:#4b5563;font-size:15px;line-height:1.6;">
                      Bonjour {first_name},<br/>
                      Votre quiz <strong>"{quiz_title}"</strong> a été corrigé.
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:24px;">
                    <div style="background:#f0fdf4;border:2px solid #86efac;padding:16px;border-radius:10px;text-align:center;margin-bottom:16px;">
                      <p style="margin:0;color:#166534;font-size:14px;font-weight:600;">Note obtenue</p>
                      <p style="margin:8px 0 0 0;color:#15803d;font-size:32px;font-weight:700;">{note_formatted}</p>
                    </div>
                    {commentaire_html}
                    {f'''<div style="margin:20px 0;text-align:center;">
                      <a href="{correction_url}" style="display:inline-block;background:#2563eb;color:#ffffff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;font-size:15px;">📖 Voir ma correction</a>
                    </div>''' if correction_url else ''}
                    <p style="margin:16px 0 0 0;color:#6b7280;font-size:14px;line-height:1.6;">
                      Vous pouvez consulter vos résultats détaillés dans votre espace personnel.
                    </p>
                    <p style="margin:16px 0 0 0;color:#6b7280;font-size:14px;line-height:1.6;">
                      Bon courage pour la suite !<br/>
                      L'équipe OptiTAB
                    </p>
                  </td>
                </tr>
              </table>
            </div>
        """

        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)
            logger.info(f"Email de notation de quiz envoyé à {user.email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi email de notation de quiz à {user.email}: {e}")
            return False

    @staticmethod
    def send_quiz_grade_notification_to_parent(parent, child, quiz_title, note, commentaire='', notion_id=None):
        """Envoie une notification par email au parent lorsqu'un quiz de son enfant est noté"""
        from django.conf import settings
        parent_name = (parent.first_name or '').strip() or 'Parent'
        child_name = (child.first_name or '').strip() or 'votre enfant'
        note_formatted = f"{note:.1f}/20"
        subject = f'Quiz corrigé pour {child_name} - "{quiz_title}"'

        # Construire l'URL vers la correction (le parent peut consulter via son dashboard)
        frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')
        correction_url = f"{frontend_url}/quiz-notion/{notion_id}?tab=solution" if notion_id else None

        text_body = (
            f"Bonjour {parent_name},\n\n"
            f"Le quiz \"{quiz_title}\" de {child_name} a été corrigé.\n\n"
            f"Note obtenue : {note_formatted}\n"
        )
        
        if commentaire:
            text_body += f"\nCommentaire du professeur :\n{commentaire}\n"
        
        if correction_url:
            text_body += f"\nLien vers le quiz : {correction_url}\n"
        
        text_body += (
            "\nVous pouvez consulter les résultats dans votre espace parent.\n\n"
            "L'équipe OptiTAB"
        )

        logo_url = EmailService._resolve_logo_url()
        commentaire_html = f"""
            <div style="background:#f3f4f6;padding:16px;border-radius:8px;margin:16px 0;">
              <p style="margin:0;color:#374151;font-size:14px;line-height:1.6;font-style:italic;">
                "{commentaire}"
              </p>
            </div>
        """ if commentaire else ""

        # Couleur de la note selon la valeur
        note_color = "#15803d" if note >= 10 else "#dc2626"
        note_bg = "#f0fdf4" if note >= 10 else "#fef2f2"
        note_border = "#86efac" if note >= 10 else "#fecaca"

        html_body = f"""
            <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
              <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                <tr>
                  <td style="padding:24px 24px 0 24px;">
                    {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                    <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;">📊 Résultat du quiz</h1>
                    <p style="margin:0;color:#4b5563;font-size:15px;line-height:1.6;">
                      Bonjour {parent_name},<br/>
                      Le quiz <strong>"{quiz_title}"</strong> de <strong>{child_name}</strong> a été corrigé.
                    </p>
                  </td>
                </tr>
                <tr>
                  <td style="padding:24px;">
                    <div style="background:{note_bg};border:2px solid {note_border};padding:16px;border-radius:10px;text-align:center;margin-bottom:16px;">
                      <p style="margin:0;color:#374151;font-size:14px;font-weight:600;">Note de {child_name}</p>
                      <p style="margin:8px 0 0 0;color:{note_color};font-size:32px;font-weight:700;">{note_formatted}</p>
                    </div>
                    {commentaire_html}
                    {f'''<div style="margin:20px 0;text-align:center;">
                      <a href="{correction_url}" style="display:inline-block;background:#2563eb;color:#ffffff;padding:12px 24px;border-radius:8px;text-decoration:none;font-weight:600;font-size:15px;">📖 Voir le quiz</a>
                    </div>''' if correction_url else ''}
                    <p style="margin:16px 0 0 0;color:#6b7280;font-size:14px;line-height:1.6;">
                      Vous pouvez suivre la progression de votre enfant dans votre espace parent.
                    </p>
                    <p style="margin:16px 0 0 0;color:#6b7280;font-size:14px;line-height:1.6;">
                      L'équipe OptiTAB
                    </p>
                  </td>
                </tr>
              </table>
            </div>
        """

        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[parent.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)
            logger.info(f"Email de notation de quiz envoyé au parent {parent.email} pour {child.email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi email de notation au parent {parent.email}: {e}")
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
            # Prépare le message en HTML (évite les backslashes dans les expressions d'f-strings)
            message_html = (message or '').strip().replace('\n', '<br/>')
            html_body = f"""
                <div>
                  {f'<p><img src="{logo_url}" alt="OptiTAB" style="height:64px;width:auto;display:block;-ms-interpolation-mode:bicubic"/></p>' if logo_url else ''}
                  <p><strong>Nouveau message depuis le formulaire de contact OptiTAB</strong></p>
                  {f'<p style="margin:6px 0 12px 0"><strong>Ticket:</strong> {ticket_id}</p>' if ticket_id else ''}
                  <p><strong>Nom:</strong> {first_name.strip()} {last_name.strip()}<br/>
                     <strong>Email:</strong> {email.strip()}</p>
                  <p><strong>Message:</strong><br/>{message_html}</p>
                  <hr style="border:none;border-top:1px solid #eee;margin:16px 0"/>
                  <table role="presentation" style="width:100%;max-width:520px;margin-top:16px">
                    <tr>
                      <td style="vertical-align:middle;padding-right:12px">
                        {f'<img src="{EmailService._resolve_logo_url()}" alt="OptiTAB" style="height:56px;width:auto;display:block"/>' if EmailService._resolve_logo_url() else ''}
                      </td>
                      <td style="vertical-align:middle;color:#6b7280;font-size:12px;line-height:1.5">
                        OptiTAB • Plateforme d'apprentissage<br/>
                        <a href="https://www.optitab.net" style="color:#6b7280;text-decoration:none">www.optitab.net</a> • contact@optitab.net
                      </td>
                    </tr>
                  </table>
                </div>
            """

            # Remise en forme professionnelle de l'email (gabarit carte)
            html_body = f"""
              <div style=\"background:#f3f4f6;padding:24px 0;\">
                <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:100%;\">
                  <tr>
                    <td align=\"center\">
                      <table role=\"presentation\" width=\"600\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:600px;max-width:100%;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;\">
                        <tr>
                          <td style=\"padding:24px 24px 0 24px;\">{f'<img src="{logo_url}" alt="OptiTAB" style="height:64px;width:auto;display:block"/>' if logo_url else ''}</td>
                        </tr>
                        <tr>
                          <td style=\"padding:16px 24px 0 24px;\">
                            <h1 style=\"margin:0 0 6px 0;font-size:20px;line-height:1.3;color:#111827;\">Nouveau message de contact</h1>
                            <p style=\"margin:0;color:#6b7280;font-size:14px;\">Reçu via le formulaire OptiTAB.</p>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"padding:16px 24px;\">
                            <table role=\"presentation\" width=\"100%\" style=\"font-size:14px;color:#111827;\">
                              <tr><td style=\"padding:6px 0;width:120px;color:#6b7280;\">Nom</td><td style=\"padding:6px 0;\">{first_name.strip()} {last_name.strip()}</td></tr>
                              <tr><td style=\"padding:6px 0;width:120px;color:#6b7280;\">Email</td><td style=\"padding:6px 0;\"><a href=\"mailto:{email.strip()}\" style=\"color:#4f46e5;text-decoration:none\">{email.strip()}</a></td></tr>
                              <tr><td style=\"padding:6px 0;width:120px;color:#6b7280;\">Sujet</td><td style=\"padding:6px 0;\">{subject.strip()}</td></tr>
                            </table>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"padding:0 24px 16px 24px;\">
                            <div style=\"background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:16px;\">
                              <div style=\"font-weight:600;margin:0 0 8px 0;color:#111827;\">Message</div>
                              <div style=\"white-space:pre-wrap;line-height:1.6;color:#111827;\">{message_html}</div>
                            </div>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"padding:0 24px 24px 24px;\">
                            <a href=\"mailto:{email.strip()}\" style=\"display:inline-block;background:#4f46e5;color:#ffffff;text-decoration:none;border-radius:8px;padding:10px 16px;font-weight:600;\">Répondre à {first_name.strip()}</a>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"border-top:1px solid #e5e7eb;padding:16px 24px;color:#6b7280;font-size:12px;\">
                            <table role=\"presentation\" width=\"100%\">
                              <tr>
                                <td style=\"vertical-align:middle\">{f'<img src="{logo_url}" alt="OptiTAB" style="height:48px;width:auto;display:block"/>' if logo_url else ''}</td>
                                <td style=\"vertical-align:middle;text-align:right\">
                                  <span style=\"color:#374151;font-weight:600\">OptiTAB</span> • Plateforme d'apprentissage<br/>
                                  <a href=\"https://www.optitab.net\" style=\"color:#6b7280;text-decoration:none\">www.optitab.net</a> • contact@optitab.net
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
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
                        OptiTAB • Plateforme d'apprentissage<br/>
                        <a href="https://www.optitab.net" style="color:#6b7280;text-decoration:none">www.optitab.net</a> • contact@optitab.net
                      </td>
                    </tr>
                  </table>
                </div>
            """

            from_email = settings.DEFAULT_FROM_EMAIL
            reply_to = [os.getenv("CONTACT_RECIPIENT", "contact@optitab.net")]

            # Remise en forme professionnelle (gabarit carte) pour la confirmation
            html_body = f"""
              <div style=\"background:#f3f4f6;padding:24px 0;\">
                <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:100%;\">
                  <tr>
                    <td align=\"center\">
                      <table role=\"presentation\" width=\"600\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:600px;max-width:100%;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;\">
                        <tr>
                          <td style=\"padding:24px 24px 0 24px;\">{f'<img src="{logo_url}" alt="OptiTAB" style="height:64px;width:auto;display:block"/>' if logo_url else ''}</td>
                        </tr>
                        <tr>
                          <td style=\"padding:16px 24px 0 24px;\">
                            <h1 style=\"margin:0 0 6px 0;font-size:20px;line-height:1.3;color:#111827;\">Nous avons bien reçu votre message</h1>
                            <p style=\"margin:0;color:#6b7280;font-size:14px;\">Sujet: <strong>{subject}</strong></p>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"padding:16px 24px;\">
                            <p style=\"margin:0 0 12px 0;color:#111827;\">Bonjour {display_name},</p>
                            <p style=\"margin:0 0 12px 0;color:#111827;\">Merci pour votre message. Notre équipe vous répondra sous <strong>24 heures</strong> (jours ouvrés).</p>
                            <p style=\"margin:0 0 16px 0;color:#6b7280;\">Pour urgence, écrivez-nous à <a href=\"mailto:contact@optitab.net\" style=\"color:#4f46e5;text-decoration:none\">contact@optitab.net</a> ou sur WhatsApp: <a href=\"https://wa.me/33764040251\" style=\"color:#4f46e5;text-decoration:none\">07 64 04 02 51</a>.</p>
                            <div style=\"background:#f9fafb;border:1px solid #e5e7eb;border-radius:10px;padding:16px;\">
                              <div style=\"font-weight:600;margin:0 0 8px 0;color:#111827;\">Copie de votre message</div>
                              <div style=\"white-space:pre-wrap;line-height:1.6;color:#111827;\">{original_html}</div>
                            </div>
                          </td>
                        </tr>
                        <tr>
                          <td style=\"border-top:1px solid #e5e7eb;padding:16px 24px;color:#6b7280;font-size:12px;\">
                            <table role=\"presentation\" width=\"100%\">
                              <tr>
                                <td style=\"vertical-align:middle\">{f'<img src="{logo_url}" alt="OptiTAB" style="height:48px;width:auto;display:block"/>' if logo_url else ''}</td>
                                <td style=\"vertical-align:middle;text-align:right\">
                                  <span style=\"color:#374151;font-weight:600\">OptiTAB</span> • Plateforme d'apprentissage<br/>
                                  <a href=\"https://www.optitab.net\" style=\"color:#6b7280;text-decoration:none\">www.optitab.net</a> • contact@optitab.net
                                </td>
                              </tr>
                            </table>
                          </td>
                        </tr>
                      </table>
                    </td>
                  </tr>
                </table>
              </div>
            """

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

    @staticmethod
    def send_newsletter_welcome(subscriber, unsubscribe_url: str) -> bool:
        """Envoie un email de bienvenue avec lien de désinscription.

        - `subscriber`: instance avec attributs `.email`, `.first_name`
        - `unsubscribe_url`: URL absolue de désinscription (GET)
        """
        try:
            to_email = getattr(subscriber, 'email', None) or ''
            if not to_email:
                return False
            display_name = (getattr(subscriber, 'first_name', '') or '').strip() or 'cher membre'
            logo_url = EmailService._resolve_logo_url()

            subject = 'Bienvenue dans la newsletter OptiTAB'
            text_body = (
                f"Bonjour {display_name},\n\n"
                "Merci pour votre inscription à la newsletter OptiTAB. "
                "Vous recevrez régulièrement des nouveautés, des conseils et des ressources pour progresser en maths.\n\n"
                f"Pour vous désabonner à tout moment, cliquez ici : {unsubscribe_url}\n\n"
                "Cordialement,\nL'équipe OptiTAB\nwww.optitab.net"
            )

            html_body = f"""
                <div style="background:#f3f4f6;padding:24px">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:600px;margin:auto;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden">
                    <tr>
                      <td style="padding:20px 24px 0 24px">{f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block"/>' if logo_url else ''}</td>
                    </tr>
                    <tr>
                      <td style="padding:6px 24px 0 24px">
                        <h1 style="margin:0 0 8px 0;font-size:20px;line-height:1.4;color:#111827">Bienvenue dans la newsletter OptiTAB</h1>
                        <p style="margin:0;color:#6b7280;font-size:14px">Ressources, nouveautés et conseils pour progresser en maths.</p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:16px 24px 8px 24px;color:#111827">
                        <p style="margin:0 0 12px 0">Bonjour {display_name},</p>
                        <p style="margin:0 0 12px 0">Merci pour votre inscription. Nous vous enverrons régulièrement des emails utiles et sans spam.</p>
                        <p style="margin:0 0 16px 0;color:#6b7280">Vous pouvez vous désabonner à tout moment en un clic.</p>
                        <p style="margin:0 0 24px 0">
                          <a href="{unsubscribe_url}" style="background:#2a38b7;color:#fff;text-decoration:none;padding:12px 18px;border-radius:8px;display:inline-block">Se désabonner</a>
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="border-top:1px solid #e5e7eb;padding:16px 24px;color:#6b7280;font-size:12px">
                        Cet email vous a été envoyé par OptiTAB. 
                        <a href="{unsubscribe_url}" style="color:#4f46e5;text-decoration:none">Se désabonner</a>
                      </td>
                    </tr>
                  </table>
                </div>
            """

            email_msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[to_email],
            )
            email_msg.attach_alternative(html_body, "text/html")
            email_msg.send(fail_silently=False)
            logger.info("Email newsletter de bienvenue envoyé à %s", to_email)
            return True
        except Exception as e:
            logger.error("Erreur envoi email newsletter: %s", e)
            return False

    @staticmethod
    def render_newsletter_template(subject: str, content_html: str, unsubscribe_url: str) -> str:
        """Construit un HTML d'email avec entête (logo) et pied de page (désabonnement).

        - subject: titre affiché en tête du contenu
        - content_html: contenu HTML déjà sûr
        - unsubscribe_url: lien de désabonnement à inclure
        """
        logo_url = EmailService._resolve_logo_url()
        safe_subject = (subject or '').strip() or 'Newsletter OptiTAB'
        body_html = content_html or ''
        return f"""
          <div style=\"background:#f3f4f6;padding:24px 0;\">
            <table role=\"presentation\" width=\"100%\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:100%;\">
              <tr>
                <td align=\"center\">
                  <table role=\"presentation\" width=\"600\" cellspacing=\"0\" cellpadding=\"0\" style=\"width:600px;max-width:100%;background:#ffffff;border:1px solid #e5e7eb;border-radius:12px;overflow:hidden;\">
                    <tr>
                      <td style=\"padding:20px 24px 0 24px;\">{f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block"/>' if logo_url else ''}</td>
                    </tr>
                    <tr>
                      <td style=\"padding:6px 24px 8px 24px;\">
                        <h1 style=\"margin:0 0 10px 0;font-size:20px;line-height:1.4;color:#111827\">{safe_subject}</h1>
                      </td>
                    </tr>
                    <tr>
                      <td style=\"padding:8px 24px 16px 24px;color:#111827;font-size:14px;line-height:1.6\">
                        {body_html}
                      </td>
                    </tr>
                    <tr>
                      <td style=\"border-top:1px solid #e5e7eb;padding:16px 24px;color:#6b7280;font-size:12px\">
                        Cet email vous a été envoyé par OptiTAB.
                        <a href=\"{unsubscribe_url}\" style=\"color:#4f46e5;text-decoration:none\">Se désabonner</a>
                      </td>
                    </tr>
                  </table>
                </td>
              </tr>
            </table>
          </div>
        """

    @staticmethod
    def send_subscription_confirmation(user, plan, niveau=None, invoice_link=None):
        """Envoie un email de confirmation d'abonnement au nouvel abonné.

        invoice_link (optionnel) : URL Stripe (PDF ou page) permettant de télécharger le reçu/la facture.
        """
        try:
            first_name = (user.first_name or '').strip() or 'OptiTABien'
            plan_name = getattr(plan, 'name', None) or 'OptiTAB Premium'
            billing_period = getattr(plan, 'billing_period', '')
            price = getattr(plan, 'price', None)
            invoice_link = (invoice_link or '').strip() or None
            
            # Formater la période de facturation
            period_labels = {
                'daily': 'par jour',
                'weekly': 'par semaine',
                'monthly': 'par mois',
                'yearly': 'par an',
            }
            period_label = period_labels.get(billing_period, '')
            price_str = f"{price:.2f}€ {period_label}" if price else ''
            
            niveau_name = ''
            if niveau:
                niveau_name = getattr(niveau, 'nom', '') or ''
                if hasattr(niveau, 'pays') and niveau.pays:
                    pays_name = getattr(niveau.pays, 'nom', '')
                    if pays_name:
                        niveau_name = f"{niveau_name} ({pays_name})"
            
            subject = '✅ Bienvenue sur OptiTAB Premium !'
            
            text_body = (
                f"Bonjour {first_name},\n\n"
                f"Merci pour votre abonnement {plan_name} sur OptiTAB !\n\n"
            )
            if price_str:
                text_body += f"Montant : {price_str}\n"
            if niveau_name:
                text_body += f"Niveau : {niveau_name}\n"
            
            logo_url = EmailService._resolve_logo_url()
            frontend_url = getattr(settings, 'FRONTEND_URL', '') or 'https://www.optitab.net'
            frontend_base = frontend_url.rstrip('/')
            subscription_url = f"{frontend_base}/subscription"

            text_body += (
                "\nVotre accès premium est maintenant activé. "
                "Connectez-vous à votre compte pour profiter de tous les cours, exercices et fonctionnalités.\n"
            )
            if invoice_link:
                text_body += (
                    "\nVotre reçu / facture est disponible :\n"
                    f"{invoice_link}\n"
                )
            text_body += (
                f"\nRetrouvez toutes vos factures dans votre espace Abonnement : {subscription_url}\n\n"
                "À très vite sur OptiTAB !\n"
                "L'équipe OptiTAB"
            )

            receipt_block = ""
            if invoice_link:
                receipt_block = f"""
                        <div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin-bottom:20px;">
                          <p style="margin:0 0 12px 0;color:#111827;font-size:15px;line-height:1.6;text-align:center;">
                            <strong>Votre reçu est disponible</strong>
                          </p>
                          <div style="text-align:center;margin-bottom:10px;">
                            <a href="{invoice_link}" style="display:inline-block;background:#2563eb;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 24px;border-radius:10px;font-size:15px;">
                              Télécharger mon reçu
                            </a>
                          </div>
                          <p style="margin:0;color:#6b7280;font-size:12px;line-height:1.6;text-align:center;">
                            Si le bouton ne fonctionne pas, copiez ce lien :<br/>
                            <a href="{invoice_link}" style="color:#2563eb;text-decoration:none;word-break:break-all;">{invoice_link}</a>
                          </p>
                        </div>
                """
            else:
                receipt_block = f"""
                        <div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin-bottom:20px;text-align:center;">
                          <p style="margin:0;color:#111827;font-size:14px;line-height:1.6;">
                            Vos factures seront disponibles dans votre espace Abonnement.
                          </p>
                          <p style="margin:10px 0 0 0;">
                            <a href="{subscription_url}" style="color:#2563eb;text-decoration:none;font-weight:600;">Accéder à mes factures</a>
                          </p>
                        </div>
                """
            
            html_body = f"""
                <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                    <tr>
                      <td style="padding:24px 24px 0 24px;">
                        {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                        <div style="text-align:center;margin-bottom:20px;">
                          <span style="font-size:48px;">🎉</span>
                        </div>
                        <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;text-align:center;">Bienvenue sur OptiTAB Premium !</h1>
                        <p style="margin:0 0 16px 0;color:#4b5563;font-size:15px;line-height:1.6;text-align:center;">
                          Merci pour votre confiance, {first_name} !
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0 24px 24px 24px;">
                        <div style="background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);border-radius:12px;padding:20px;margin-bottom:20px;">
                          <p style="margin:0;color:#166534;font-size:15px;line-height:1.6;">
                            <strong>Votre abonnement {plan_name} est activé</strong><br/>
                            Profitez de tous les cours, exercices corrigés et fonctionnalités avancées.
                          </p>
                          {f'<p style="margin:12px 0 0 0;color:#15803d;font-size:14px;"><strong>Montant :</strong> {price_str}</p>' if price_str else ''}
                          {f'<p style="margin:8px 0 0 0;color:#15803d;font-size:14px;"><strong>Niveau :</strong> {niveau_name}</p>' if niveau_name else ''}
                        </div>
                        {receipt_block}
                        <div style="text-align:center;">
                          <a href="{frontend_base}/dashboard" style="display:inline-block;background:#22c55e;color:#ffffff;text-decoration:none;font-weight:600;padding:14px 28px;border-radius:10px;font-size:15px;">
                            Accéder à mon espace
                          </a>
                        </div>
                        <p style="margin:14px 0 0 0;color:#6b7280;font-size:13px;line-height:1.6;text-align:center;">
                          Vos factures : <a href="{subscription_url}" style="color:#2563eb;text-decoration:none;font-weight:600;">espace Abonnement</a>
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:16px 24px;background:#f9fafb;border-top:1px solid #e5e7eb;">
                        <p style="margin:0;color:#6b7280;font-size:13px;line-height:1.6;text-align:center;">
                          Une question ? Contactez-nous à <a href="mailto:contact@optitab.net" style="color:#4f46e5;text-decoration:none;">contact@optitab.net</a>
                        </p>
                      </td>
                    </tr>
                  </table>
                </div>
            """
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)
            
            logger.info(f"Email de confirmation d'abonnement envoyé à {user.email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi email de confirmation d'abonnement à {user.email}: {e}")
            return False

    @staticmethod
    def send_subscription_cancellation_confirmation(user, plan, niveau=None, effective_end=None, is_scheduled=True, beneficiary=None):
        """Envoie un email de confirmation de résiliation à l'utilisateur.

        - is_scheduled=True : annulation programmée à la fin de période (cancel_at_period_end)
        - beneficiary : si achat cadeau, indique le bénéficiaire concerné (optionnel)
        """
        try:
            first_name = (user.first_name or '').strip() or 'OptiTABien'
            plan_name = getattr(plan, 'name', None) or 'OptiTAB Premium'

            niveau_name = ''
            if niveau:
                niveau_name = getattr(niveau, 'nom', '') or ''
                if hasattr(niveau, 'pays') and niveau.pays:
                    pays_name = getattr(niveau.pays, 'nom', '')
                    if pays_name:
                        niveau_name = f"{niveau_name} ({pays_name})"

            logo_url = EmailService._resolve_logo_url()
            frontend_url = getattr(settings, 'FRONTEND_URL', '') or 'https://www.optitab.net'
            frontend_base = frontend_url.rstrip('/')
            subscription_url = f"{frontend_base}/subscription"

            end_label = None
            if effective_end:
                try:
                    end_label = timezone.localtime(effective_end).strftime('%d %B %Y')
                except Exception:
                    end_label = str(effective_end)

            beneficiary_label = ''
            if beneficiary:
                beneficiary_label = getattr(beneficiary, 'full_name', '') or ''
                beneficiary_label = beneficiary_label.strip() or getattr(beneficiary, 'email', '') or ''

            subject = (
                "Résiliation programmée de votre abonnement OptiTAB"
                if is_scheduled
                else "Confirmation de résiliation de votre abonnement OptiTAB"
            )

            text_body = (
                f"Bonjour {first_name},\n\n"
                f"Nous confirmons la résiliation de votre abonnement {plan_name}.\n"
            )
            if beneficiary_label:
                text_body += f"\nBénéficiaire : {beneficiary_label}\n"
            if niveau_name:
                text_body += f"Niveau : {niveau_name}\n"

            if is_scheduled:
                text_body += "\nVotre abonnement ne sera pas renouvelé."
                if end_label:
                    text_body += f" Vous gardez l'accès jusqu'au {end_label}.\n"
                else:
                    text_body += " Vous gardez l'accès jusqu'à la fin de la période en cours.\n"
            else:
                text_body += "\nVotre abonnement est désormais résilié."
                if end_label:
                    text_body += f" Accès maintenu jusqu'au {end_label}.\n"
                else:
                    text_body += "\n"

            text_body += (
                f"\nRetrouvez votre statut et vos factures ici : {subscription_url}\n\n"
                "Une question ? Contactez-nous à contact@optitab.net\n\n"
                "L'équipe OptiTAB"
            )

            headline = "Résiliation programmée" if is_scheduled else "Abonnement résilié"
            status_chip = (
                '<span style="display:inline-block;background:#fee2e2;color:#991b1b;padding:6px 10px;border-radius:999px;font-size:12px;font-weight:700;">RÉSILIATION</span>'
                if not is_scheduled
                else '<span style="display:inline-block;background:#fff7ed;color:#9a3412;padding:6px 10px;border-radius:999px;font-size:12px;font-weight:700;">FIN PROGRAMMÉE</span>'
            )

            details_rows = ""
            if beneficiary_label:
                details_rows += f"""
                  <tr>
                    <td style="padding:6px 0;color:#6b7280;width:34%;">Bénéficiaire</td>
                    <td style="padding:6px 0;color:#111827;font-weight:600;">{beneficiary_label}</td>
                  </tr>
                """
            if niveau_name:
                details_rows += f"""
                  <tr>
                    <td style="padding:6px 0;color:#6b7280;">Niveau</td>
                    <td style="padding:6px 0;color:#111827;font-weight:600;">{niveau_name}</td>
                  </tr>
                """
            if end_label:
                details_rows += f"""
                  <tr>
                    <td style="padding:6px 0;color:#6b7280;">Fin d'accès</td>
                    <td style="padding:6px 0;color:#111827;font-weight:600;">{end_label}</td>
                  </tr>
                """

            html_body = f"""
              <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                  <tr>
                    <td style="padding:24px 24px 0 24px;">
                      {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                      {status_chip}
                      <h1 style="margin:12px 0 8px 0;font-size:22px;color:#111827;">{headline}</h1>
                      <p style="margin:0 0 14px 0;color:#4b5563;font-size:15px;line-height:1.6;">
                        Bonjour {first_name},<br/>
                        Nous confirmons la résiliation de votre abonnement <strong>{plan_name}</strong>.
                      </p>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:0 24px 24px 24px;">
                      <div style="background:#f9fafb;border:1px solid #e5e7eb;border-radius:12px;padding:16px;">
                        <table width="100%" cellspacing="0" cellpadding="0" style="font-size:14px;">
                          {details_rows}
                        </table>
                      </div>
                      <div style="text-align:center;margin-top:18px;">
                        <a href="{subscription_url}" style="display:inline-block;background:#111827;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 22px;border-radius:10px;">
                          Gérer mon abonnement
                        </a>
                      </div>
                      <p style="margin:16px 0 0 0;color:#6b7280;font-size:13px;line-height:1.6;text-align:center;">
                        Besoin d'aide ? <a href="mailto:contact@optitab.net" style="color:#4f46e5;text-decoration:none;">contact@optitab.net</a>
                      </p>
                    </td>
                  </tr>
                </table>
              </div>
            """

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)
            logger.info("Email de résiliation envoyé à %s", user.email)
            return True
        except Exception as e:
            logger.error("Erreur envoi email de résiliation à %s: %s", getattr(user, 'email', ''), e)
            return False

    @staticmethod
    def send_new_subscription_notification_to_admin(user, plan, niveau=None, is_gift=False, payer=None):
        """Envoie une notification à contact@optitab.net lorsqu'un nouvel abonnement est souscrit."""
        try:
            from subscriptions.models import UserSubscription, AccessPass
            
            admin_email = 'contact@optitab.net'
            user_email = user.email or 'Email inconnu'
            user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or 'Utilisateur'
            plan_name = getattr(plan, 'name', None) or 'Plan inconnu'
            billing_period = getattr(plan, 'billing_period', '')
            price = getattr(plan, 'price', None)
            plan_mode = getattr(plan, 'plan_mode', 'subscription')
            
            # Détecter si c'est un réabonnement (l'utilisateur avait un abonnement annulé pour ce niveau)
            is_resubscription = False
            if niveau:
                is_resubscription = UserSubscription.objects.filter(
                    user=user, 
                    niveau_pays=niveau,
                    status='canceled'
                ).exists()
            
            stripe_stats = EmailService._count_active_subscriptions_on_stripe()
            stripe_active_subscribers_label = EmailService._format_active_subscribers_for_email(stripe_stats)
            stripe_mode_label = stripe_stats.get('mode_label', 'UNKNOWN')
            stripe_error_message = stripe_stats.get('error_message')
            if stripe_error_message:
                logger.warning(
                    "send_new_subscription_notification_to_admin: Stripe stats unavailable (mode=%s): %s",
                    stripe_mode_label,
                    stripe_error_message,
                )
            
            # Compter les passes actifs (pas sur Stripe, juste local)
            now = timezone.now()
            active_passes = AccessPass.objects.filter(ends_at__gt=now, is_revoked=False).count()
            
            # Formater la période de facturation
            period_labels = {
                'daily': 'Journalier',
                'weekly': 'Hebdomadaire',
                'monthly': 'Mensuel',
                'yearly': 'Annuel',
            }
            period_label = period_labels.get(billing_period, billing_period)
            price_str = f"{price:.2f}€" if price else 'N/A'
            
            niveau_name = ''
            if niveau:
                niveau_name = getattr(niveau, 'nom', '') or ''
                if hasattr(niveau, 'pays') and niveau.pays:
                    pays_name = getattr(niveau.pays, 'nom', '')
                    if pays_name:
                        niveau_name = f"{niveau_name} ({pays_name})"
            
            # Type d'abonnement
            type_label = 'Pass unique' if plan_mode == 'one_time' else 'Abonnement récurrent'
            
            # Info cadeau
            gift_info = ''
            payer_name = ''
            payer_email = ''
            if is_gift and payer:
                payer_name = f"{payer.first_name or ''} {payer.last_name or ''}".strip() or 'Parent'
                payer_email = payer.email or 'Email inconnu'
                gift_info = f"\n🎁 CADEAU offert par : {payer_name} ({payer_email})"
            
            # Sujet et titre selon nouveau/réabonnement
            if is_resubscription:
                subject = f"🔄 Réabonnement : {user_name} - {plan_name}"
                title_emoji = "🔄"
                title_text = "Réabonnement"
                intro_text = "Un utilisateur s'est réabonné sur OptiTAB !"
            else:
                subject = f"🆕 Nouvel abonnement : {user_name} - {plan_name}"
                title_emoji = "🆕"
                title_text = "Nouvelle Souscription"
                intro_text = "Nouvelle souscription sur OptiTAB !"
            
            text_body = (
                f"{intro_text}\n\n"
                f"👤 Utilisateur : {user_name}\n"
                f"📧 Email : {user_email}\n"
                f"📦 Plan : {plan_name}\n"
                f"💰 Prix : {price_str}\n"
                f"📅 Période : {period_label}\n"
                f"🔄 Type : {type_label}\n"
            )
            if niveau_name:
                text_body += f"📚 Niveau : {niveau_name}\n"
            text_body += f"\n📊 Abonnements actifs Stripe : {stripe_active_subscribers_label}\n"
            text_body += f"🔌 Mode Stripe : {stripe_mode_label}\n"
            if stripe_error_message:
                text_body += f"⚠️ Erreur Stripe : {stripe_error_message}\n"
            text_body += f"🎫 Passes actifs : {active_passes}\n"
            if gift_info:
                text_body += gift_info
            
            # Couleur du header selon nouveau/réabonnement
            header_gradient = "linear-gradient(135deg,#22c55e 0%,#16a34a 100%)" if is_resubscription else "linear-gradient(135deg,#4f46e5 0%,#7c3aed 100%)"
            
            html_body = f"""
                <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                    <tr>
                      <td style="padding:24px;background:{header_gradient};">
                        <h1 style="margin:0;font-size:20px;color:#ffffff;text-align:center;">{title_emoji} {title_text}</h1>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:24px;">
                        <table width="100%" cellspacing="0" cellpadding="8" style="font-size:14px;color:#374151;">
                          <tr>
                            <td style="width:40%;font-weight:600;color:#6b7280;">👤 Utilisateur</td>
                            <td>{user_name}</td>
                          </tr>
                          <tr style="background:#f9fafb;">
                            <td style="font-weight:600;color:#6b7280;">📧 Email</td>
                            <td><a href="mailto:{user_email}" style="color:#4f46e5;">{user_email}</a></td>
                          </tr>
                          <tr>
                            <td style="font-weight:600;color:#6b7280;">📦 Plan</td>
                            <td><strong>{plan_name}</strong></td>
                          </tr>
                          <tr style="background:#f9fafb;">
                            <td style="font-weight:600;color:#6b7280;">💰 Prix</td>
                            <td style="color:#22c55e;font-weight:600;">{price_str}</td>
                          </tr>
                          <tr>
                            <td style="font-weight:600;color:#6b7280;">📅 Période</td>
                            <td>{period_label}</td>
                          </tr>
                          <tr style="background:#f9fafb;">
                            <td style="font-weight:600;color:#6b7280;">🔄 Type</td>
                            <td>{type_label}</td>
                          </tr>
                          {f'<tr><td style="font-weight:600;color:#6b7280;">📚 Niveau</td><td>{niveau_name}</td></tr>' if niveau_name else ''}
                          <tr style="background:#f9fafb;">
                            <td style="font-weight:600;color:#6b7280;">📊 Abonnements actifs Stripe</td>
                            <td><strong>{stripe_active_subscribers_label}</strong></td>
                          </tr>
                          <tr>
                            <td style="font-weight:600;color:#6b7280;">🔌 Mode Stripe</td>
                            <td><strong>{stripe_mode_label}</strong></td>
                          </tr>
                          <tr style="background:#f9fafb;">
                            <td style="font-weight:600;color:#6b7280;">🎫 Passes actifs</td>
                            <td><strong>{active_passes}</strong></td>
                          </tr>
                          {f'<tr><td style="font-weight:600;color:#9a3412;">⚠️ Erreur Stripe</td><td style="color:#9a3412;">{stripe_error_message}</td></tr>' if stripe_error_message else ''}
                        </table>
                        {f'''<div style="margin-top:16px;padding:12px;background:#fef3c7;border-radius:8px;border-left:4px solid #f59e0b;">
                          <p style="margin:0;color:#92400e;font-size:14px;">
                            <strong>🎁 Cadeau</strong><br/>
                            Offert par : {payer_name} ({payer_email})
                          </p>
                        </div>''' if is_gift and payer else ''}
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:16px 24px;background:#f3f4f6;text-align:center;">
                        <p style="margin:0;color:#6b7280;font-size:12px;">
                          Notification automatique OptiTAB
                        </p>
                      </td>
                    </tr>
                  </table>
                </div>
            """
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)
            
            logger.info(f"Notification de {'réabonnement' if is_resubscription else 'nouvel abonnement'} envoyée à {admin_email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi notification admin pour nouvel abonnement: {e}")
            return False

    @staticmethod
    def send_reactivation_notification_to_admin(user, subscription=None):
        """Envoie une notification à contact@optitab.net lorsqu'un abonnement est réactivé."""
        try:
            from subscriptions.models import AccessPass
            
            admin_email = 'contact@optitab.net'
            user_email = user.email or 'Email inconnu'
            user_name = f"{user.first_name or ''} {user.last_name or ''}".strip() or 'Utilisateur'
            
            # Récupérer les infos de l'abonnement
            plan_name = 'Plan inconnu'
            niveau_name = ''
            price_str = 'N/A'
            period_label = ''
            
            if subscription:
                if subscription.plan:
                    plan_name = subscription.plan.name or 'Plan inconnu'
                    price = subscription.plan.price
                    price_str = f"{price:.2f}€" if price else 'N/A'
                    billing_period = subscription.plan.billing_period or ''
                    period_labels = {
                        'daily': 'Journalier',
                        'weekly': 'Hebdomadaire',
                        'monthly': 'Mensuel',
                        'yearly': 'Annuel',
                    }
                    period_label = period_labels.get(billing_period, billing_period)
                
                if subscription.niveau_pays:
                    niveau_name = subscription.niveau_pays.nom or ''
                    if hasattr(subscription.niveau_pays, 'pays') and subscription.niveau_pays.pays:
                        pays_name = getattr(subscription.niveau_pays.pays, 'nom', '')
                        if pays_name:
                            niveau_name = f"{niveau_name} ({pays_name})"
            
            stripe_stats = EmailService._count_active_subscriptions_on_stripe()
            stripe_active_subscribers_label = EmailService._format_active_subscribers_for_email(stripe_stats)
            stripe_mode_label = stripe_stats.get('mode_label', 'UNKNOWN')
            stripe_error_message = stripe_stats.get('error_message')
            if stripe_error_message:
                logger.warning(
                    "send_reactivation_notification_to_admin: Stripe stats unavailable (mode=%s): %s",
                    stripe_mode_label,
                    stripe_error_message,
                )

            # Compter les passes actifs (local uniquement)
            now = timezone.now()
            active_passes = AccessPass.objects.filter(ends_at__gt=now, is_revoked=False).count()
            
            subject = f"🔄 Réactivation : {user_name} - {plan_name}"
            
            text_body = (
                f"Un utilisateur a réactivé son abonnement sur OptiTAB !\n\n"
                f"👤 Utilisateur : {user_name}\n"
                f"📧 Email : {user_email}\n"
                f"📦 Plan : {plan_name}\n"
                f"💰 Prix : {price_str}\n"
                f"📅 Période : {period_label}\n"
            )
            if niveau_name:
                text_body += f"📚 Niveau : {niveau_name}\n"
            text_body += f"\n📊 Abonnements actifs Stripe : {stripe_active_subscribers_label}\n"
            text_body += f"🔌 Mode Stripe : {stripe_mode_label}\n"
            if stripe_error_message:
                text_body += f"⚠️ Erreur Stripe : {stripe_error_message}\n"
            text_body += f"🎫 Passes actifs : {active_passes}\n"
            
            html_body = f"""
                <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                    <tr>
                      <td style="padding:24px;background:linear-gradient(135deg,#22c55e 0%,#16a34a 100%);">
                        <h1 style="margin:0;font-size:20px;color:#ffffff;text-align:center;">🔄 Réactivation d'abonnement</h1>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:24px;">
                        <p style="margin:0 0 16px 0;color:#166534;font-size:15px;font-weight:600;">
                          Un utilisateur a annulé sa résiliation et continue son abonnement !
                        </p>
                        <table width="100%" cellspacing="0" cellpadding="8" style="font-size:14px;color:#374151;">
                          <tr>
                            <td style="width:40%;font-weight:600;color:#6b7280;">👤 Utilisateur</td>
                            <td>{user_name}</td>
                          </tr>
                          <tr style="background:#f9fafb;">
                            <td style="font-weight:600;color:#6b7280;">📧 Email</td>
                            <td><a href="mailto:{user_email}" style="color:#4f46e5;">{user_email}</a></td>
                          </tr>
                          <tr>
                            <td style="font-weight:600;color:#6b7280;">📦 Plan</td>
                            <td><strong>{plan_name}</strong></td>
                          </tr>
                          <tr style="background:#f9fafb;">
                            <td style="font-weight:600;color:#6b7280;">💰 Prix</td>
                            <td style="color:#22c55e;font-weight:600;">{price_str}</td>
                          </tr>
                          {f'<tr><td style="font-weight:600;color:#6b7280;">📅 Période</td><td>{period_label}</td></tr>' if period_label else ''}
                          {f'<tr style="background:#f9fafb;"><td style="font-weight:600;color:#6b7280;">📚 Niveau</td><td>{niveau_name}</td></tr>' if niveau_name else ''}
                        </table>
                        <div style="margin-top:16px;padding:16px;background:#f0fdf4;border-radius:8px;border:1px solid #bbf7d0;">
                          <p style="margin:0;font-weight:700;color:#166534;font-size:15px;">📊 Statistiques Stripe</p>
                          <p style="margin:8px 0 0 0;color:#166534;font-size:14px;">
                            Abonnements actifs : <strong>{stripe_active_subscribers_label}</strong><br/>
                            Mode Stripe : <strong>{stripe_mode_label}</strong><br/>
                            Passes actifs : <strong>{active_passes}</strong>
                          </p>
                          {f'<p style="margin:10px 0 0 0;color:#9a3412;font-size:13px;">Erreur Stripe : {stripe_error_message}</p>' if stripe_error_message else ''}
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:16px 24px;background:#f3f4f6;text-align:center;">
                        <p style="margin:0;color:#6b7280;font-size:12px;">
                          Notification automatique OptiTAB
                        </p>
                      </td>
                    </tr>
                  </table>
                </div>
            """
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)
            
            logger.info(f"Notification de réactivation envoyée à {admin_email}")
            return True
        except Exception as e:
            logger.error(f"Erreur envoi notification admin pour réactivation: {e}")
            return False

    @staticmethod
    def send_subscription_cancellation_notification_to_admin(user, plan, niveau=None, effective_end=None, is_scheduled=True, beneficiary=None):
        """Envoie une notification à contact@optitab.net lorsqu'un abonnement est résilié/programmé."""
        try:
            from subscriptions.models import AccessPass
            
            admin_email = 'contact@optitab.net'
            user_email = getattr(user, 'email', None) or 'Email inconnu'
            user_name = f"{getattr(user, 'first_name', '') or ''} {getattr(user, 'last_name', '') or ''}".strip() or 'Utilisateur'
            plan_name = getattr(plan, 'name', None) or 'Plan inconnu'

            stripe_stats = EmailService._count_active_subscriptions_on_stripe()
            stripe_active_subscribers_label = EmailService._format_active_subscribers_for_email(stripe_stats)
            stripe_mode_label = stripe_stats.get('mode_label', 'UNKNOWN')
            stripe_error_message = stripe_stats.get('error_message')
            if stripe_error_message:
                logger.warning(
                    "send_subscription_cancellation_notification_to_admin: Stripe stats unavailable (mode=%s): %s",
                    stripe_mode_label,
                    stripe_error_message,
                )

            # Compter les passes actifs (local uniquement)
            now = timezone.now()
            active_passes = AccessPass.objects.filter(ends_at__gt=now, is_revoked=False).count()

            niveau_name = ''
            if niveau:
                niveau_name = getattr(niveau, 'nom', '') or ''
                if hasattr(niveau, 'pays') and niveau.pays:
                    pays_name = getattr(niveau.pays, 'nom', '')
                    if pays_name:
                        niveau_name = f"{niveau_name} ({pays_name})"

            end_label = None
            if effective_end:
                try:
                    end_label = timezone.localtime(effective_end).strftime('%d %B %Y')
                except Exception:
                    end_label = str(effective_end)

            beneficiary_label = ''
            if beneficiary:
                beneficiary_name = f"{getattr(beneficiary, 'first_name', '') or ''} {getattr(beneficiary, 'last_name', '') or ''}".strip()
                beneficiary_email = getattr(beneficiary, 'email', '') or ''
                if beneficiary_name:
                    beneficiary_label = f"{beneficiary_name} ({beneficiary_email})"
                else:
                    beneficiary_label = beneficiary_email

            type_label = 'Annulation programmée (fin de période)' if is_scheduled else 'Annulation immédiate'
            
            # Indication si c'est un parent qui résilie pour son enfant
            is_gift_cancellation = beneficiary is not None
            if is_gift_cancellation:
                subject = f"❌ Désabonnement (parent→enfant) : {user_name} - {plan_name}"
            else:
                subject = f"❌ Désabonnement : {user_name} - {plan_name}"

            text_body = (
                "Un utilisateur vient de résilier son abonnement.\n\n"
                f"👤 Utilisateur : {user_name}\n"
                f"📧 Email : {user_email}\n"
                f"📦 Plan : {plan_name}\n"
                f"🧾 Type : {type_label}\n"
            )
            if beneficiary_label:
                text_body += f"🎁 Bénéficiaire (enfant) : {beneficiary_label}\n"
            if niveau_name:
                text_body += f"📚 Niveau : {niveau_name}\n"
            if end_label:
                text_body += f"🗓 Fin d'accès : {end_label}\n"

            text_body += f"\n📊 Abonnements actifs Stripe : {stripe_active_subscribers_label}\n"
            text_body += f"🔌 Mode Stripe : {stripe_mode_label}\n"
            if stripe_error_message:
                text_body += f"⚠️ Erreur Stripe : {stripe_error_message}\n"
            text_body += f"🎫 Passes actifs : {active_passes}\n"

            html_body = f"""
              <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                  <tr>
                    <td style="padding:24px;background:linear-gradient(135deg,#ef4444 0%,#f97316 100%);">
                      <h1 style="margin:0;font-size:20px;color:#ffffff;text-align:center;">❌ Désabonnement{' (parent→enfant)' if is_gift_cancellation else ''}</h1>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:24px;">
                      <table width="100%" cellspacing="0" cellpadding="8" style="font-size:14px;color:#374151;">
                        <tr>
                          <td style="width:40%;font-weight:600;color:#6b7280;">👤 Utilisateur (payeur)</td>
                          <td>{user_name}</td>
                        </tr>
                        <tr style="background:#f9fafb;">
                          <td style="font-weight:600;color:#6b7280;">📧 Email</td>
                          <td><a href="mailto:{user_email}" style="color:#4f46e5;">{user_email}</a></td>
                        </tr>
                        <tr>
                          <td style="font-weight:600;color:#6b7280;">📦 Plan</td>
                          <td><strong>{plan_name}</strong></td>
                        </tr>
                        <tr style="background:#f9fafb;">
                          <td style="font-weight:600;color:#6b7280;">🧾 Type</td>
                          <td>{type_label}</td>
                        </tr>
                        {f'<tr><td style="font-weight:600;color:#6b7280;">🎁 Bénéficiaire (enfant)</td><td>{beneficiary_label}</td></tr>' if beneficiary_label else ''}
                        {f'<tr style="background:#f9fafb;"><td style="font-weight:600;color:#6b7280;">📚 Niveau</td><td>{niveau_name}</td></tr>' if niveau_name else ''}
                        {f"<tr><td style='font-weight:600;color:#6b7280;'>🗓 Fin d'accès</td><td>{end_label}</td></tr>" if end_label else ''}
                      </table>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:16px 24px;background:#f3f4f6;text-align:center;">
                      <p style="margin:0;color:#6b7280;font-size:12px;">
                        Notification automatique OptiTAB
                      </p>
                      <p style="margin:8px 0 0;color:#374151;font-size:14px;font-weight:600;">
                        📊 Abonnements actifs Stripe : {stripe_active_subscribers_label}
                      </p>
                      <p style="margin:4px 0 0;color:#374151;font-size:14px;font-weight:600;">
                        🔌 Mode Stripe : {stripe_mode_label}
                      </p>
                      <p style="margin:4px 0 0;color:#374151;font-size:14px;font-weight:600;">
                        🎫 Passes actifs : {active_passes}
                      </p>
                      {f'<p style="margin:6px 0 0;color:#9a3412;font-size:12px;">⚠️ Erreur Stripe : {stripe_error_message}</p>' if stripe_error_message else ''}
                    </td>
                  </tr>
                </table>
              </div>
            """

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)

            logger.info("Notification de désabonnement envoyée à %s", admin_email)
            return True
        except Exception as e:
            logger.error("Erreur envoi notification admin désabonnement: %s", e)
            return False

    @staticmethod
    def send_child_account_created(child_user, temp_password, parent_user):
        """Envoie un email à l'enfant avec ses identifiants de connexion."""
        try:
            child_email = getattr(child_user, 'email', None)
            if not child_email:
                logger.warning("send_child_account_created: pas d'email enfant")
                return False

            child_first_name = getattr(child_user, 'first_name', '') or 'là'
            parent_name = f"{getattr(parent_user, 'first_name', '') or ''} {getattr(parent_user, 'last_name', '') or ''}".strip()
            if not parent_name:
                parent_name = getattr(parent_user, 'email', 'ton parent')

            login_url = f"{settings.FRONTEND_URL}/login"
            subject = "🎉 Ton compte OptiTAB a été créé !"
            logo_url = EmailService._resolve_logo_url()

            text_body = f"""
Bonjour {child_first_name} !

{parent_name} t'a créé un compte sur OptiTAB pour t'aider dans tes révisions.

Voici tes identifiants de connexion :

📧 Email : {child_email}
🔑 Mot de passe : {temp_password}

👉 Connecte-toi ici : {login_url}

⚠️ Important : Nous te recommandons de changer ton mot de passe après ta première connexion pour plus de sécurité.

À bientôt sur OptiTAB !
L'équipe OptiTAB
Contact : contact@optitab.net
"""

            html_body = f"""
              <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                  <tr>
                    <td style="padding:24px;text-align:center;">
                      {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin:0 auto 16px;"/>' if logo_url else ''}
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:0 24px 24px;">
                      <div style="background:linear-gradient(135deg,#22c55e 0%,#16a34a 100%);border-radius:12px;padding:20px;text-align:center;margin-bottom:24px;">
                        <h1 style="margin:0;font-size:22px;color:#ffffff;">🎉 Bienvenue sur OptiTAB !</h1>
                      </div>
                      
                      <p style="margin:0 0 16px;font-size:16px;color:#374151;">
                        Bonjour <strong>{child_first_name}</strong> !
                      </p>
                      <p style="margin:0 0 20px;font-size:14px;color:#6b7280;">
                        {parent_name} t'a créé un compte sur OptiTAB pour t'aider dans tes révisions.
                      </p>
                      
                      <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:12px;padding:20px;margin:20px 0;">
                        <h3 style="margin:0 0 12px;font-size:14px;color:#166534;">Tes identifiants de connexion :</h3>
                        <table width="100%" cellspacing="0" cellpadding="8" style="font-size:14px;">
                          <tr>
                            <td style="color:#6b7280;width:100px;">📧 Email</td>
                            <td style="color:#111827;font-weight:600;">{child_email}</td>
                          </tr>
                          <tr>
                            <td style="color:#6b7280;">🔑 Mot de passe</td>
                            <td style="color:#111827;font-weight:600;font-family:monospace;background:#fef3c7;padding:4px 8px;border-radius:4px;">{temp_password}</td>
                          </tr>
                        </table>
                      </div>

                      <div style="text-align:center;margin:24px 0;">
                        <a href="{login_url}" style="display:inline-block;background:linear-gradient(135deg,#3b82f6 0%,#2563eb 100%);color:#ffffff;text-decoration:none;padding:14px 32px;border-radius:8px;font-weight:600;font-size:16px;">
                          Se connecter
                        </a>
                      </div>

                      <div style="background:#fef3c7;border-radius:8px;padding:12px;border-left:4px solid #f59e0b;">
                        <p style="margin:0;color:#92400e;font-size:13px;">
                          ⚠️ <strong>Recommandation :</strong> Change ton mot de passe après ta première connexion pour plus de sécurité.
                        </p>
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:20px 24px;background:#f3f4f6;text-align:center;border-top:1px solid #e5e7eb;">
                      <p style="margin:0 0 8px;color:#374151;font-size:13px;font-weight:500;">
                        L'équipe OptiTAB
                      </p>
                      <p style="margin:0;color:#6b7280;font-size:12px;">
                        Une question ? Écrivez-nous à 
                        <a href="mailto:contact@optitab.net" style="color:#3b82f6;text-decoration:none;">contact@optitab.net</a>
                      </p>
                    </td>
                  </tr>
                </table>
              </div>
            """

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[child_email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)

            logger.info("Email de création de compte enfant envoyé à %s", child_email)
            return True
        except Exception as e:
            logger.error("Erreur envoi email création compte enfant: %s", e)
            return False

    @staticmethod
    def send_pass_expiration_notification(user, access_pass, niveau=None):
        """Envoie un email de notification lorsqu'un pass expire."""
        try:
            first_name = (user.first_name or '').strip() or 'OptiTABien'
            plan_name = getattr(access_pass.plan, 'name', None) or 'Pass OptiTAB'
            ends_at = access_pass.ends_at
            ends_at_str = ends_at.strftime('%d %B %Y à %H:%M') if ends_at else ''
            
            niveau_name = ''
            if niveau:
                niveau_name = getattr(niveau, 'nom', '') or ''
                if hasattr(niveau, 'pays') and niveau.pays:
                    pays_name = getattr(niveau.pays, 'nom', '')
                    if pays_name:
                        niveau_name = f"{niveau_name} ({pays_name})"
            
            subject = '⏰ Votre pass OptiTAB a expiré'
            logo_url = EmailService._resolve_logo_url()
            frontend_url = getattr(settings, 'FRONTEND_URL', '') or 'https://www.optitab.net'
            frontend_base = frontend_url.rstrip('/')
            pricing_url = f"{frontend_base}/pricing"

            text_body = (
                f"Bonjour {first_name},\n\n"
                f"Votre {plan_name} sur OptiTAB a expiré le {ends_at_str}.\n\n"
            )
            if niveau_name:
                text_body += f"Niveau : {niveau_name}\n\n"
            text_body += (
                "Pour continuer à accéder à tous les cours, exercices et fonctionnalités premium, "
                "vous pouvez renouveler votre pass ou souscrire un abonnement.\n\n"
                f"Consultez nos offres : {pricing_url}\n\n"
                "À bientôt sur OptiTAB !\n"
                "L'équipe OptiTAB"
            )

            html_body = f"""
                <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                    <tr>
                      <td style="padding:24px 24px 0 24px;">
                        {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                        <div style="text-align:center;margin-bottom:20px;">
                          <span style="font-size:48px;">⏰</span>
                        </div>
                        <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;text-align:center;">Votre pass a expiré</h1>
                        <p style="margin:0 0 16px 0;color:#4b5563;font-size:15px;line-height:1.6;text-align:center;">
                          Bonjour {first_name},
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0 24px 24px 24px;">
                        <div style="background:#fef2f2;border:1px solid #fecaca;border-radius:12px;padding:20px;margin-bottom:20px;">
                          <p style="margin:0;color:#991b1b;font-size:15px;line-height:1.6;">
                            <strong>Votre {plan_name} a expiré</strong><br/>
                            Date d'expiration : {ends_at_str}
                          </p>
                          {f'<p style="margin:12px 0 0 0;color:#b91c1c;font-size:14px;"><strong>Niveau :</strong> {niveau_name}</p>' if niveau_name else ''}
                        </div>
                        <p style="margin:0 0 20px 0;color:#4b5563;font-size:14px;line-height:1.6;text-align:center;">
                          Pour continuer à accéder à tous les cours premium, exercices corrigés et fonctionnalités avancées, renouvelez votre pass ou souscrivez à un abonnement.
                        </p>
                        <div style="text-align:center;">
                          <a href="{pricing_url}" style="display:inline-block;background:#4f46e5;color:#ffffff;text-decoration:none;font-weight:600;padding:14px 28px;border-radius:10px;font-size:15px;">
                            Voir nos offres
                          </a>
                        </div>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:16px 24px;background:#f9fafb;border-top:1px solid #e5e7eb;">
                        <p style="margin:0;color:#6b7280;font-size:13px;line-height:1.6;text-align:center;">
                          Une question ? Contactez-nous à <a href="mailto:contact@optitab.net" style="color:#4f46e5;text-decoration:none;">contact@optitab.net</a>
                        </p>
                      </td>
                    </tr>
                  </table>
                </div>
            """

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)

            logger.info("Email d'expiration de pass envoyé à %s", user.email)
            return True
        except Exception as e:
            logger.error("Erreur envoi email expiration pass: %s", e)
            return False

    @staticmethod
    def send_pass_expiration_notification_to_admin(user, access_pass, niveau=None):
        """Envoie une notification admin lorsqu'un pass expire (suivi business)."""
        try:
            from subscriptions.models import AccessPass

            admin_email = 'contact@optitab.net'
            user_email = getattr(user, 'email', None) or 'Email inconnu'
            user_name = f"{getattr(user, 'first_name', '') or ''} {getattr(user, 'last_name', '') or ''}".strip() or 'Utilisateur'

            plan_name = getattr(getattr(access_pass, 'plan', None), 'name', None) or 'Pass OptiTAB'
            payment_intent = getattr(access_pass, 'stripe_payment_intent_id', None) or ''

            ends_at = getattr(access_pass, 'ends_at', None)
            try:
                ends_at_label = timezone.localtime(ends_at).strftime('%d %B %Y à %H:%M') if ends_at else '—'
            except Exception:
                ends_at_label = str(ends_at) if ends_at else '—'

            niveau_name = ''
            if niveau:
                niveau_name = getattr(niveau, 'nom', '') or ''
                if hasattr(niveau, 'pays') and niveau.pays:
                    pays_name = getattr(niveau.pays, 'nom', '')
                    if pays_name:
                        niveau_name = f"{niveau_name} ({pays_name})"

            now = timezone.now()
            active_passes = AccessPass.objects.filter(ends_at__gt=now, is_revoked=False).count()
            stripe_stats = EmailService._count_active_subscriptions_on_stripe()
            stripe_active_subscribers_label = EmailService._format_active_subscribers_for_email(stripe_stats)
            stripe_mode_label = stripe_stats.get('mode_label', 'UNKNOWN')
            stripe_error_message = stripe_stats.get('error_message')
            if stripe_error_message:
                logger.warning(
                    "send_pass_expiration_notification_to_admin: Stripe stats unavailable (mode=%s): %s",
                    stripe_mode_label,
                    stripe_error_message,
                )

            subject = f"⏰ Pass expiré : {user_name} - {plan_name}"

            text_body = (
                "Un pass vient d'expirer sur OptiTAB.\n\n"
                f"👤 Utilisateur : {user_name}\n"
                f"📧 Email : {user_email}\n"
                f"🎫 Pass : {plan_name}\n"
                f"🗓 Expiré le : {ends_at_label}\n"
            )
            if niveau_name:
                text_body += f"📚 Niveau : {niveau_name}\n"
            if payment_intent:
                text_body += f"🧾 PaymentIntent : {payment_intent}\n"
            text_body += (
                f"\n📊 Abonnements actifs Stripe : {stripe_active_subscribers_label}\n"
                f"🔌 Mode Stripe : {stripe_mode_label}\n"
                f"🎫 Nombre de passes actifs : {active_passes}\n"
            )
            if stripe_error_message:
                text_body += f"⚠️ Erreur Stripe : {stripe_error_message}\n"

            html_body = f"""
              <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                  <tr>
                    <td style="padding:24px;background:linear-gradient(135deg,#ef4444 0%,#f59e0b 100%);">
                      <h1 style="margin:0;font-size:20px;color:#ffffff;text-align:center;">⏰ Pass expiré</h1>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:24px;">
                      <table width="100%" cellspacing="0" cellpadding="8" style="font-size:14px;color:#374151;">
                        <tr>
                          <td style="width:40%;font-weight:600;color:#6b7280;">👤 Utilisateur</td>
                          <td>{user_name}</td>
                        </tr>
                        <tr style="background:#f9fafb;">
                          <td style="font-weight:600;color:#6b7280;">📧 Email</td>
                          <td><a href="mailto:{user_email}" style="color:#4f46e5;">{user_email}</a></td>
                        </tr>
                        <tr>
                          <td style="font-weight:600;color:#6b7280;">🎫 Pass</td>
                          <td><strong>{plan_name}</strong></td>
                        </tr>
                        <tr style="background:#f9fafb;">
                          <td style="font-weight:600;color:#6b7280;">🗓 Expiré le</td>
                          <td>{ends_at_label}</td>
                        </tr>
                        {f'<tr><td style="font-weight:600;color:#6b7280;">📚 Niveau</td><td>{niveau_name}</td></tr>' if niveau_name else ''}
                        {f'<tr style="background:#f9fafb;"><td style="font-weight:600;color:#6b7280;">🧾 PaymentIntent</td><td style="font-family:monospace;">{payment_intent}</td></tr>' if payment_intent else ''}
                      </table>
                      <div style="margin-top:16px;padding:16px;background:#f3f4f6;border-radius:10px;border:1px solid #e5e7eb;">
                        <p style="margin:0 0 8px 0;color:#111827;font-weight:700;">📊 Accès actifs</p>
                        <p style="margin:0;color:#374151;">
                          Abonnements actifs Stripe : <strong>{stripe_active_subscribers_label}</strong><br/>
                          Mode Stripe : <strong>{stripe_mode_label}</strong><br/>
                          Passes actifs : <strong>{active_passes}</strong>
                        </p>
                        {f'<p style="margin:8px 0 0 0;color:#9a3412;font-size:12px;">Erreur Stripe : {stripe_error_message}</p>' if stripe_error_message else ''}
                      </div>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:16px 24px;background:#f9fafb;border-top:1px solid #e5e7eb;text-align:center;">
                      <p style="margin:0;color:#6b7280;font-size:12px;">Notification automatique OptiTAB</p>
                    </td>
                  </tr>
                </table>
              </div>
            """

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[admin_email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)

            logger.info("Notification admin expiration pass envoyée à %s", admin_email)
            return True
        except Exception as e:
            logger.error("Erreur envoi notification admin expiration pass: %s", e)
            return False

    @staticmethod
    def send_subscription_renewal_notification(user, plan, niveau=None, invoice_link=None, payment_history=None):
        """Envoie un email de notification lorsqu'un abonnement est renouvelé avec le lien vers la facture."""
        try:
            first_name = (user.first_name or '').strip() or 'OptiTABien'
            plan_name = getattr(plan, 'name', None) or 'OptiTAB Premium'
            billing_period = getattr(plan, 'billing_period', '')
            price = getattr(plan, 'price', None)
            invoice_link = (invoice_link or '').strip() or None
            
            # Formater la période de facturation
            period_labels = {
                'daily': 'par jour',
                'weekly': 'par semaine',
                'monthly': 'par mois',
                'yearly': 'par an',
            }
            period_label = period_labels.get(billing_period, '')
            price_str = f"{price:.2f}€ {period_label}" if price else ''
            
            # Date du paiement
            date_str = ''
            amount_str = ''
            if payment_history:
                date_str = timezone.localtime(payment_history.created_at).strftime('%d %B %Y')
                amount_str = f"{payment_history.amount:.2f}€"
            
            niveau_name = ''
            if niveau:
                niveau_name = getattr(niveau, 'nom', '') or ''
                if hasattr(niveau, 'pays') and niveau.pays:
                    pays_name = getattr(niveau.pays, 'nom', '')
                    if pays_name:
                        niveau_name = f"{niveau_name} ({pays_name})"
            
            subject = '🔄 Votre abonnement OptiTAB a été renouvelé'
            logo_url = EmailService._resolve_logo_url()
            frontend_url = getattr(settings, 'FRONTEND_URL', '') or 'https://www.optitab.net'
            frontend_base = frontend_url.rstrip('/')
            subscription_url = f"{frontend_base}/subscription"

            text_body = (
                f"Bonjour {first_name},\n\n"
                f"Votre abonnement {plan_name} sur OptiTAB a été renouvelé avec succès"
            )
            if date_str:
                text_body += f" le {date_str}"
            text_body += ".\n\n"
            if amount_str:
                text_body += f"Montant prélevé : {amount_str}\n"
            if niveau_name:
                text_body += f"Niveau : {niveau_name}\n"
            
            text_body += "\nVotre accès premium reste activé. Continuez à profiter de tous les cours et exercices.\n"
            
            if invoice_link:
                text_body += (
                    "\nVotre facture est disponible :\n"
                    f"{invoice_link}\n"
                )
            text_body += (
                f"\nRetrouvez toutes vos factures dans votre espace Abonnement : {subscription_url}\n\n"
                "À très vite sur OptiTAB !\n"
                "L'équipe OptiTAB"
            )

            receipt_block = ""
            if invoice_link:
                receipt_block = f"""
                        <div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin-bottom:20px;">
                          <p style="margin:0 0 12px 0;color:#111827;font-size:15px;line-height:1.6;text-align:center;">
                            <strong>Votre facture est disponible</strong>
                          </p>
                          <div style="text-align:center;margin-bottom:10px;">
                            <a href="{invoice_link}" style="display:inline-block;background:#2563eb;color:#ffffff;text-decoration:none;font-weight:600;padding:12px 24px;border-radius:10px;font-size:15px;">
                              Télécharger ma facture
                            </a>
                          </div>
                          <p style="margin:0;color:#6b7280;font-size:12px;line-height:1.6;text-align:center;">
                            Si le bouton ne fonctionne pas, copiez ce lien :<br/>
                            <a href="{invoice_link}" style="color:#2563eb;text-decoration:none;word-break:break-all;">{invoice_link}</a>
                          </p>
                        </div>
                """
            else:
                receipt_block = f"""
                        <div style="background:#f8fafc;border:1px solid #e5e7eb;border-radius:12px;padding:16px;margin-bottom:20px;text-align:center;">
                          <p style="margin:0;color:#111827;font-size:14px;line-height:1.6;">
                            Vos factures sont disponibles dans votre espace Abonnement.
                          </p>
                          <p style="margin:10px 0 0 0;">
                            <a href="{subscription_url}" style="color:#2563eb;text-decoration:none;font-weight:600;">Accéder à mes factures</a>
                          </p>
                        </div>
                """

            html_body = f"""
                <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                    <tr>
                      <td style="padding:24px 24px 0 24px;">
                        {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                        <div style="text-align:center;margin-bottom:20px;">
                          <span style="font-size:48px;">🔄</span>
                        </div>
                        <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;text-align:center;">Votre abonnement a été renouvelé</h1>
                        <p style="margin:0 0 16px 0;color:#4b5563;font-size:15px;line-height:1.6;text-align:center;">
                          Bonjour {first_name},
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:0 24px 24px 24px;">
                        <div style="background:linear-gradient(135deg,#f0fdf4 0%,#dcfce7 100%);border-radius:12px;padding:20px;margin-bottom:20px;">
                          <p style="margin:0;color:#166534;font-size:15px;line-height:1.6;">
                            <strong>Votre abonnement {plan_name} a été renouvelé avec succès</strong><br/>
                            Continuez à profiter de tous les cours et exercices premium.
                          </p>
                          {f'<p style="margin:12px 0 0 0;color:#15803d;font-size:14px;"><strong>Montant prélevé :</strong> {amount_str}</p>' if amount_str else ''}
                          {f'<p style="margin:8px 0 0 0;color:#15803d;font-size:14px;"><strong>Niveau :</strong> {niveau_name}</p>' if niveau_name else ''}
                        </div>
                        {receipt_block}
                        <div style="text-align:center;">
                          <a href="{frontend_base}/dashboard" style="display:inline-block;background:#22c55e;color:#ffffff;text-decoration:none;font-weight:600;padding:14px 28px;border-radius:10px;font-size:15px;">
                            Accéder à mon espace
                          </a>
                        </div>
                        <p style="margin:14px 0 0 0;color:#6b7280;font-size:13px;line-height:1.6;text-align:center;">
                          Vos factures : <a href="{subscription_url}" style="color:#2563eb;text-decoration:none;font-weight:600;">espace Abonnement</a>
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:16px 24px;background:#f9fafb;border-top:1px solid #e5e7eb;">
                        <p style="margin:0;color:#6b7280;font-size:13px;line-height:1.6;text-align:center;">
                          Une question ? Contactez-nous à <a href="mailto:contact@optitab.net" style="color:#4f46e5;text-decoration:none;">contact@optitab.net</a>
                        </p>
                      </td>
                    </tr>
                  </table>
                </div>
            """

            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)

            logger.info("Email de renouvellement d'abonnement envoyé à %s", user.email)
            return True
        except Exception as e:
            logger.error("Erreur envoi email renouvellement: %s", e)
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
