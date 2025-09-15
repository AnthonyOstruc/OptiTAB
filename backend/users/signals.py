from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    frontend_base = getattr(settings, 'FRONTEND_BASE_URL', getattr(settings, 'FRONTEND_URL', 'http://localhost:3000'))
    reset_url = f"{frontend_base.rstrip('/')}/password-reset?token={reset_password_token.key}"
    message = f"Bonjour,\n\nCliquez sur le lien suivant pour réinitialiser votre mot de passe :\n\n{reset_url}\n\nMerci."
    
    send_mail(
        subject="Réinitialisation de votre mot de passe - OptiTAB",
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reset_password_token.user.email],
        fail_silently=False,
    )
