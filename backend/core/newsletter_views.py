from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.conf import settings
from django.urls import reverse
from django.http import HttpResponse

from .services import ResponseService, EmailService
from .models import NewsletterSubscriber
import re

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@api_view(["POST"])
@permission_classes([AllowAny])
@authentication_classes([])
def newsletter_subscribe(request):
    """Inscription newsletter: sauvegarde + email de bienvenue avec lien de désinscription."""
    data = request.data or {}
    email = (data.get("email") or "").strip()
    first = (data.get("firstName") or "").strip()
    last = (data.get("lastName") or "").strip()

    if not email or not EMAIL_REGEX.match(email):
        return ResponseService.validation_error({"email": "Email invalide"})

    # IP de consentement
    ip = request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip() or request.META.get('REMOTE_ADDR')

    # Rechercher (insensible à la casse) puis créer si nécessaire
    sub = NewsletterSubscriber.objects.filter(email__iexact=email).first()
    if not sub:
        sub = NewsletterSubscriber.objects.create(
            email=email.lower(), first_name=first, last_name=last, consent_ip=ip, est_actif=True, source='website'
        )

    # Mise à jour éventuelle et réactivation
    changed = False
    if first and sub.first_name != first:
        sub.first_name = first; changed = True
    if last and sub.last_name != last:
        sub.last_name = last; changed = True
    if not sub.est_actif or sub.unsubscribed_at is not None:
        sub.reactivate(save=False); changed = True
    if sub.consent_ip != ip and ip:
        sub.consent_ip = ip; changed = True
    if changed:
        sub.save()

    # Lien de désinscription
    unsub_url = request.build_absolute_uri(reverse('core:newsletter_unsubscribe', args=[sub.unsubscribe_token]))

    try:
        EmailService.send_newsletter_welcome(sub, unsub_url)
    except Exception:
        pass

    return ResponseService.success(
        message="Inscription prise en compte. Un email de bienvenue vient d'être envoyé.",
        data={"email": sub.email},
        status_code=status.HTTP_200_OK
    )


@api_view(["GET"])
@permission_classes([AllowAny])
@authentication_classes([])
def newsletter_unsubscribe(request, token: str):
    """Désinscription via lien public affichant une page HTML simple."""
    try:
        sub = NewsletterSubscriber.objects.get(unsubscribe_token=token)
        if sub.est_actif:
            sub.mark_unsubscribed()
        success = True
    except NewsletterSubscriber.DoesNotExist:
        success = False

    frontend_url = getattr(settings, 'FRONTEND_URL', getattr(settings, 'FRONTEND_BASE_URL', 'https://www.optitab.net'))
    homepage = frontend_url.rstrip('/') + '/'
    message = ("Vous êtes désabonné de la newsletter OptiTAB." if success else "Lien de désabonnement invalide ou déjà utilisé.")

    html = f"""
    <!doctype html>
    <html lang=\"fr\">
      <head>
        <meta charset=\"utf-8\" />
        <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\" />
        <title>Newsletter OptiTAB</title>
        <style>
          body {{ background:#f3f4f6; font-family: Arial, sans-serif; color:#111827; }}
          .card {{ max-width:560px; margin:40px auto; background:#fff; border:1px solid #e5e7eb; border-radius:12px; padding:24px; }}
          .btn {{ display:inline-block; padding:10px 16px; background:#2a38b7; color:#fff; text-decoration:none; border-radius:8px; }}
          .muted {{ color:#6b7280; font-size:12px; }}
        </style>
      </head>
      <body>
        <div class=\"card\">
          <h1 style=\"margin-top:0\">Newsletter OptiTAB</h1>
          <p>{message}</p>
          <p><a class=\"btn\" href=\"{homepage}\">Retour au site</a></p>
          <p class=\"muted\">Si c'était une erreur, vous pourrez vous réabonner depuis notre site.</p>
        </div>
      </body>
    </html>
    """
    return HttpResponse(html)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def newsletter_subscribers_list(request):
    """Liste paginée des abonnés (admin only). Query params: q, active=true/false, limit, offset."""
    user = request.user
    if not (user.is_staff or user.is_superuser):
        return ResponseService.error("Accès interdit", status_code=status.HTTP_403_FORBIDDEN)

    q = (request.GET.get('q') or '').strip()
    active = request.GET.get('active', 'true').lower()
    limit = int(request.GET.get('limit', '100'))
    offset = int(request.GET.get('offset', '0'))

    qs = NewsletterSubscriber.objects.all().order_by('-date_creation')
    if active in ('true', '1', 'yes'): qs = qs.filter(est_actif=True)
    elif active in ('false', '0', 'no'): qs = qs.filter(est_actif=False)
    if q:
        qs = qs.filter(email__icontains=q)

    total = qs.count()
    items = list(qs[offset:offset+limit].values('email', 'first_name', 'last_name', 'est_actif', 'date_creation', 'unsubscribed_at'))
    return ResponseService.success(data={"total": total, "items": items})


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def newsletter_broadcast(request):
    """Envoie un email à tous les abonnés actifs (admin only).

    Body JSON: { subject: str, text?: str, html?: str, limit?: int, onlyInactive?: bool }
    """
    user = request.user
    if not (user.is_staff or user.is_superuser):
        return ResponseService.error("Accès interdit", status_code=status.HTTP_403_FORBIDDEN)

    data = request.data or {}
    subject = (data.get('subject') or '').strip()
    text = (data.get('text') or '').strip()
    html = (data.get('html') or '').strip()
    use_template = bool(data.get('useTemplate', True))
    limit = int(data.get('limit') or 0)
    only_inactive = bool(data.get('onlyInactive') or False)
    if not subject:
        return ResponseService.validation_error({"subject": "Sujet requis"})

    qs = NewsletterSubscriber.objects.all()
    qs = qs.filter(est_actif=not only_inactive)
    qs = qs.order_by('id')
    if limit:
        qs = qs[:limit]

    count = 0
    for sub in qs.iterator():
        unsub_url = request.build_absolute_uri(reverse('core:newsletter_unsubscribe', args=[sub.unsubscribe_token]))
        # Construire corps
        text_body = text + ("\n\nSe désabonner: " + unsub_url)
        # Eviter les backslashes dans les expressions d'f-strings: pré-calculer le HTML du texte
        text_html = (text or '').replace('\n', '<br/>')
        html_body = html or f"<div style='font-family:Arial,sans-serif;font-size:14px;color:#111827'>{text_html}<br/><br/><a href='{unsub_url}'>Se désabonner</a></div>"
        try:
            # Gabarit HTML par défaut si demandé
            if use_template:
                if html:
                    content_html = html
                else:
                    lines = (text or '').split('\n')
                    content_html = ''.join(f"<p style='margin:0 0 12px 0'>{line.strip()}</p>" for line in lines if line.strip())
                html_body = EmailService.render_newsletter_template(subject, content_html, unsub_url)

            from django.core.mail import EmailMultiAlternatives
            msg = EmailMultiAlternatives(subject=subject, body=text_body, from_email=settings.DEFAULT_FROM_EMAIL, to=[sub.email])
            msg.attach_alternative(html_body, 'text/html')
            msg.send(fail_silently=False)
            count += 1
        except Exception:
            # Continuer même si un email échoue
            continue

    return ResponseService.success(message=f"Email envoyé à {count} abonné(s)", data={"sent": count})
