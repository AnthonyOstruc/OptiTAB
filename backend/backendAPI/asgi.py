"""
ASGI config for backendAPI project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import logging
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backendAPI.settings')

application = get_asgi_application()

# Auto-run pass expiration emails (dev + prod) via an in-process scheduler.
# Safe across multiple workers/instances using a Postgres advisory lock.
try:
    from subscriptions.pass_expiration_scheduler import start_pass_expiration_emails_scheduler

    start_pass_expiration_emails_scheduler()
except Exception:
    logging.getLogger(__name__).exception(
        "Impossible de démarrer le scheduler d'emails d'expiration de pass (ASGI)."
    )
    print(
        "[pass-expiration] scheduler failed to start (ASGI) — check backend logs.",
        flush=True,
    )
