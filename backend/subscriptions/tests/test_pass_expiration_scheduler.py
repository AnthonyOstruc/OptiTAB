from __future__ import annotations

import os
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from django.conf import settings
from django.core.signals import request_started

from subscriptions import pass_expiration_scheduler as planificateur
from subscriptions.pass_expiration_scheduler import _should_start_scheduler


class PassExpirationSchedulerShouldStartTests(TestCase):
    def test_runserver_parent_process_does_not_start_without_run_main(self):
        with patch.dict(os.environ, {}, clear=True), patch(
            "subscriptions.pass_expiration_scheduler.os.sys.argv",
            ["manage.py", "runserver"],
        ):
            self.assertFalse(_should_start_scheduler())

    def test_runserver_child_process_starts_when_run_main_true(self):
        with patch.dict(os.environ, {"RUN_MAIN": "true"}, clear=True), patch(
            "subscriptions.pass_expiration_scheduler.os.sys.argv",
            ["manage.py", "runserver"],
        ):
            self.assertTrue(_should_start_scheduler())

    def test_runserver_no_reload_starts_without_run_main(self):
        with patch.dict(os.environ, {}, clear=True), patch(
            "subscriptions.pass_expiration_scheduler.os.sys.argv",
            ["manage.py", "runserver", "--noreload"],
        ):
            self.assertTrue(_should_start_scheduler())

    def test_disable_env_prevents_start(self):
        with patch.dict(
            os.environ,
            {"DISABLE_PASS_EXPIRATION_EMAILS_SCHEDULER": "1", "RUN_MAIN": "true"},
            clear=True,
        ), patch(
            "subscriptions.pass_expiration_scheduler.os.sys.argv",
            ["manage.py", "runserver"],
        ):
            self.assertFalse(_should_start_scheduler())


class DemarrageALaPremiereRequeteTests(TestCase):
    """La tâche de fond naît à la première requête servie, jamais à l'import du serveur
    (un fil lancé avant la création des processus de gunicorn peut les figer)."""

    def setUp(self):
        self.addCleanup(request_started.disconnect, dispatch_uid=planificateur._PREMIERE_REQUETE)
        autorise = patch.object(planificateur, "_should_start_scheduler", return_value=True)
        autorise.start()
        self.addCleanup(autorise.stop)

    def _requete(self):
        return request_started.send(sender=self.__class__, environ={})

    def test_rien_ne_demarre_au_chargement_du_serveur(self):
        with patch.object(planificateur, "start_pass_expiration_emails_scheduler") as demarrer:
            planificateur.demarrer_a_la_premiere_requete()
            demarrer.assert_not_called()

    def test_demarre_une_seule_fois_a_la_premiere_requete(self):
        with patch.object(planificateur, "start_pass_expiration_emails_scheduler") as demarrer:
            planificateur.demarrer_a_la_premiere_requete()
            self._requete()
            self._requete()
            demarrer.assert_called_once_with()

    def test_un_echec_du_demarrage_ne_fait_pas_echouer_la_requete(self):
        echec = patch.object(planificateur, "start_pass_expiration_emails_scheduler", side_effect=RuntimeError("panne"))
        with echec, patch.object(planificateur.logger, "exception") as journal, patch("builtins.print"):
            planificateur.demarrer_a_la_premiere_requete()
            self._requete()
            journal.assert_called_once()

    def test_desactivee_elle_ne_se_branche_pas(self):
        interdit = patch.object(planificateur, "_should_start_scheduler", return_value=False)
        with interdit, patch.object(planificateur, "start_pass_expiration_emails_scheduler") as demarrer:
            planificateur.demarrer_a_la_premiere_requete()
            self._requete()
            demarrer.assert_not_called()

    def test_les_portes_d_entree_du_serveur_ne_lancent_aucun_fil(self):
        for nom in ("wsgi.py", "asgi.py"):
            source = (Path(settings.BASE_DIR) / "backendAPI" / nom).read_text(encoding="utf-8")
            self.assertIn("demarrer_a_la_premiere_requete()", source, nom)
            self.assertNotIn("start_pass_expiration_emails_scheduler()", source, nom)


class ConnexionsBaseBorneesTests(TestCase):
    def test_une_connexion_a_la_base_ne_peut_pas_attendre_sans_fin(self):
        source = (Path(settings.BASE_DIR) / "backendAPI" / "settings.py").read_text(encoding="utf-8")
        self.assertEqual(source.count('.setdefault("OPTIONS", {}).update(_reseau_base)'), 2)
        for option in ('"connect_timeout"', '"keepalives": 1', '"keepalives_idle"', '"keepalives_interval"', '"keepalives_count"'):
            self.assertIn(option, source)
