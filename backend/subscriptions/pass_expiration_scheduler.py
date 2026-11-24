from __future__ import annotations

import logging
import os
import threading
import time

from django.core.management import call_command
from django.db import close_old_connections, connection
from django.db.utils import OperationalError
from django.utils import timezone

logger = logging.getLogger(__name__)

_scheduler_thread: threading.Thread | None = None
_scheduler_lock = threading.Lock()


def _parse_int(value: str | None, *, default: int) -> int:
    try:
        return int(value) if value is not None else default
    except Exception:
        return default


def _should_start_scheduler() -> bool:
    # Allow explicit disable.
    if str(os.getenv("DISABLE_PASS_EXPIRATION_EMAILS_SCHEDULER", "")).strip().lower() in {"1", "true", "yes"}:
        return False

    # Avoid starting in the outer autoreloader process (dev server).
    # Django sets RUN_MAIN="true" in the reloaded child process.
    if "runserver" in os.sys.argv:
        if "--noreload" in os.sys.argv:
            return True
        return str(os.getenv("RUN_MAIN", "")).lower() == "true"

    # For gunicorn/WSGI, start in all workers (advisory lock ensures one runner).
    return True


def _try_acquire_db_lock(lock_key: int) -> bool:
    if connection.vendor != "postgresql":
        return True
    with connection.cursor() as cursor:
        cursor.execute("SELECT pg_try_advisory_lock(%s);", [lock_key])
        row = cursor.fetchone()
        return bool(row and row[0])


def _release_db_lock(lock_key: int) -> None:
    if connection.vendor != "postgresql":
        return
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT pg_advisory_unlock(%s);", [lock_key])
    except Exception:
        # Best-effort unlock; lock is released automatically if connection closes.
        pass


def _run_once(*, hours_ago: int) -> None:
    try:
        call_command("send_pass_expiration_emails", hours_ago=hours_ago, verbosity=0)
    except Exception as exc:
        logger.exception("Pass expiration scheduler: error running command: %s", exc)


SYNCHRO_STRIPE_INTERVALLE = 6 * 3600


def _synchroniser_stripe_si_besoin() -> None:
    """Toutes les 6 heures, en production : abonnements remis d'accord avec Stripe.

    Jamais avec la clé de test (le site local écrit dans la base réelle).
    """
    from django.core.cache import cache
    from stripe_config import STRIPE_RUNTIME_MODE

    forcer = str(os.getenv("STRIPE_SYNC_FORCE", "")).strip().lower() in {"1", "true", "yes"}
    if STRIPE_RUNTIME_MODE != "live" and not forcer:
        return
    if cache.get("optitab_synchro_stripe"):
        return
    cache.set("optitab_synchro_stripe", timezone.now().isoformat(), SYNCHRO_STRIPE_INTERVALLE)
    try:
        from subscriptions.synchronisation import synchroniser_abonnements

        bilan = synchroniser_abonnements()
        print(f"[synchro-stripe] {bilan}", flush=True)
    except Exception as exc:
        logger.exception("Synchronisation Stripe : erreur (%s)", exc)


def _scheduler_loop(*, lock_key: int, interval_seconds: int, hours_ago: int) -> None:
    while True:
        try:
            close_old_connections()
            acquired = False
            try:
                acquired = _try_acquire_db_lock(lock_key)
            except OperationalError as exc:
                logger.warning("Pass expiration scheduler: DB not ready (%s)", exc)
                print(f"[pass-expiration] DB not ready: {exc}", flush=True)
                acquired = False

            if acquired:
                try:
                    logger.info(
                        "Pass expiration scheduler: running (hours_ago=%s, at=%s)",
                        hours_ago,
                        timezone.now().isoformat(),
                    )
                    _run_once(hours_ago=hours_ago)
                    _synchroniser_stripe_si_besoin()
                finally:
                    _release_db_lock(lock_key)
        except Exception as exc:
            logger.exception("Pass expiration scheduler: unexpected error: %s", exc)

        time.sleep(max(30, interval_seconds))


_PREMIERE_REQUETE = "optitab-taches-de-fond"


def demarrer_a_la_premiere_requete() -> None:
    """Lance la tâche de fond quand ce processus sert sa première requête.

    Jamais à l'import du serveur : avec « gunicorn --preload », l'import a lieu dans
    le processus maître, avant la création des processus qui servent les requêtes.
    Un fil déjà au travail à cet instant (connexion à la base, appel à Stripe) peut
    laisser un verrou pris dans un processus fils, qui ne répond alors plus jamais
    (panne du 24/11/2026 : après un démarrage, une requête sur deux sans réponse).
    Ici, le fil naît toujours dans un processus qui sert des requêtes.
    """
    if not _should_start_scheduler():
        return
    from django.core.signals import request_started

    request_started.connect(_a_la_premiere_requete, weak=False, dispatch_uid=_PREMIERE_REQUETE)


def _a_la_premiere_requete(**_kwargs) -> None:
    from django.core.signals import request_started

    request_started.disconnect(dispatch_uid=_PREMIERE_REQUETE)
    try:
        start_pass_expiration_emails_scheduler()
    except Exception:  # une tâche de fond ne doit jamais faire échouer une requête
        logger.exception("Tâche de fond : démarrage impossible.")
        print("[pass-expiration] scheduler failed to start — check backend logs.", flush=True)


def start_pass_expiration_emails_scheduler() -> None:
    """Start a lightweight in-process scheduler for pass expiration emails.

    - Safe across multiple gunicorn workers/instances via Postgres advisory lock.
    - In dev runserver, starts only in the autoreloader child process.
    - Disable via `DISABLE_PASS_EXPIRATION_EMAILS_SCHEDULER=1`.
    """
    if not _should_start_scheduler():
        return

    global _scheduler_thread
    with _scheduler_lock:
        if _scheduler_thread and _scheduler_thread.is_alive():
            return

        lock_key = _parse_int(os.getenv("PASS_EXPIRATION_EMAILS_LOCK_KEY"), default=845_120_331)

        from django.conf import settings

        default_interval = 60 if getattr(settings, "DEBUG", False) else 3600
        interval_seconds = _parse_int(
            os.getenv("PASS_EXPIRATION_EMAILS_INTERVAL_SECONDS"),
            default=default_interval,
        )
        hours_ago = _parse_int(os.getenv("PASS_EXPIRATION_EMAILS_HOURS_AGO"), default=72)

        thread = threading.Thread(
            target=_scheduler_loop,
            name="pass-expiration-emails-scheduler",
            daemon=True,
            kwargs={
                "lock_key": lock_key,
                "interval_seconds": interval_seconds,
                "hours_ago": hours_ago,
            },
        )
        thread.start()
        _scheduler_thread = thread
        print(
            f"[pass-expiration] scheduler started: interval={interval_seconds}s hours_ago={hours_ago}",
            flush=True,
        )
        logger.info(
            "Pass expiration scheduler started (interval_seconds=%s, hours_ago=%s).",
            interval_seconds,
            hours_ago,
        )
