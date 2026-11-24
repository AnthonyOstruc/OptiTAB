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

# Tâche de fond (fin des pass, synchronisation Stripe) : lancée à la première requête
# servie, jamais ici — ce fichier est chargé par le processus maître de gunicorn, avant
# la création des processus qui servent les requêtes (voir demarrer_a_la_premiere_requete).
# Plusieurs processus peuvent la lancer : un verrou PostgreSQL n'en laisse tourner qu'un.
try:
    from subscriptions.pass_expiration_scheduler import demarrer_a_la_premiere_requete

    demarrer_a_la_premiere_requete()
except Exception:
    logging.getLogger(__name__).exception(
        "Impossible de démarrer le scheduler d'emails d'expiration de pass (ASGI)."
    )
    print(
        "[pass-expiration] scheduler failed to start (ASGI) — check backend logs.",
        flush=True,
    )
