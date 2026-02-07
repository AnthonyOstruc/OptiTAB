"""
WSGI config for backendAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import logging
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')

application = get_wsgi_application()

# Auto-run pass expiration emails (dev + prod) via an in-process scheduler.
# Safe across multiple workers/instances using a Postgres advisory lock.
try:
    from subscriptions.pass_expiration_scheduler import start_pass_expiration_emails_scheduler

    start_pass_expiration_emails_scheduler()
except Exception:
    logging.getLogger(__name__).exception(
        "Impossible de démarrer le scheduler d'emails d'expiration de pass."
    )
    print(
        "[pass-expiration] scheduler failed to start (WSGI) — check backend logs.",
        flush=True,
    )
