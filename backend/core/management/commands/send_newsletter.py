import os
import time
from typing import Optional

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.urls import reverse

from core.models import NewsletterSubscriber


def build_unsubscribe_url(token: str, backend_base: str) -> str:
    base = (backend_base or '').strip().rstrip('/')
    if not base:
        base = 'http://localhost:8000' if getattr(settings, 'DEBUG', False) else 'https://optitab-backend.onrender.com'
    path = reverse('core:newsletter_unsubscribe', args=[str(token)])
    return f"{base}{path}"


class Command(BaseCommand):
    help = "Envoie un email à tous les abonnés newsletter (un email par abonné avec lien de désabonnement)."

    def add_arguments(self, parser):
        parser.add_argument('--subject', required=True, help='Sujet de l’email à envoyer')
        parser.add_argument('--text', default='', help='Corps texte brut (fallback)')
        parser.add_argument('--html', default='', help='Corps HTML inline (optionnel)')
        parser.add_argument('--html-file', default='', help='Chemin vers un fichier HTML à utiliser comme corps (optionnel)')
        parser.add_argument('--from-email', default=getattr(settings, 'DEFAULT_FROM_EMAIL', None), help='Expéditeur (FROM)')
        parser.add_argument('--only-inactive', action='store_true', help='Cibler les désabonnés (pour campagne de réactivation)')
        parser.add_argument('--limit', type=int, default=0, help='Limiter le nombre d’envois (debug)')
        parser.add_argument('--offset', type=int, default=0, help='Décaler le curseur de départ')
        parser.add_argument('--batch-size', type=int, default=100, help='Taille de lot avant d’attendre')
        parser.add_argument('--sleep', type=float, default=0.0, help='Pause (secondes) entre emails')
        parser.add_argument('--backend-base', default='', help='Base URL publique du backend pour le lien de désabonnement')
        parser.add_argument('--dry-run', action='store_true', help='N’envoie rien, affiche seulement')

    def handle(self, *args, **options):
        subject = options['subject']
        from_email = options['from_email'] or getattr(settings, 'DEFAULT_FROM_EMAIL', None)
        if not from_email:
            raise CommandError('DEFAULT_FROM_EMAIL non configuré et --from-email non fourni')

        html = options['html']
        html_file = options['html_file']
        text = options['text']
        if html_file:
            if not os.path.exists(html_file):
                raise CommandError(f"Fichier HTML introuvable: {html_file}")
            with open(html_file, 'r', encoding='utf-8') as f:
                html = f.read()

        queryset = NewsletterSubscriber.objects.all()
        if options['only_inactive']:
            queryset = queryset.filter(est_actif=False)
        else:
            queryset = queryset.filter(est_actif=True)

        offset = options['offset']
        limit = options['limit']
        if offset:
            queryset = queryset[offset:]
        if limit:
            queryset = queryset[:limit]

        total = queryset.count()
        self.stdout.write(self.style.WARNING(f"Envoi newsletter: {total} destinataires"))

        sent = 0
        for idx, sub in enumerate(queryset.iterator()):
            unsub_url = build_unsubscribe_url(sub.unsubscribe_token, options['backend_base'])

            # Construire corps final (ajout lien désabonnement)
            text_body = (text or '').strip()
            text_body += ("\n\nSe désabonner: " + unsub_url)

            html_body = html or ''
            if html_body:
                footer = f'<div style="margin-top:16px;color:#6b7280;font-size:12px">'
                footer += f'Cet email vous a été envoyé par OptiTAB. '
                footer += f'<a href="{unsub_url}" style="color:#4f46e5;text-decoration:none">Se désabonner</a>'
                footer += '</div>'
                html_body = f"{html_body}{footer}"
            else:
                # Si pas de HTML fourni, créer un HTML simple depuis le texte
                safe_text = (text or '').replace('\n', '<br/>')
                html_body = f"<div style='font-family:Arial,sans-serif;font-size:14px;color:#111827'>{safe_text}<br/><br/>"
                html_body += f"<a href='{unsub_url}' style='color:#4f46e5;text-decoration:none'>Se désabonner</a></div>"

            preview = f"[#{idx+1}/{total}] -> {sub.email}"
            if options['dry_run']:
                self.stdout.write(preview)
            else:
                msg = EmailMultiAlternatives(subject=subject, body=text_body, from_email=from_email, to=[sub.email])
                msg.attach_alternative(html_body, 'text/html')
                msg.send(fail_silently=False)
                sent += 1

                # Throttle
                if options['sleep']:
                    time.sleep(float(options['sleep']))
                if sent % options['batch_size'] == 0:
                    self.stdout.write(self.style.SUCCESS(f"{sent} emails envoyés..."))

        if options['dry_run']:
            self.stdout.write(self.style.WARNING(f"Dry-run terminé. {total} destinataires listés."))
        else:
            self.stdout.write(self.style.SUCCESS(f"Terminé. {sent} email(s) envoyé(s)."))

