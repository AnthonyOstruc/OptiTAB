from __future__ import annotations

import os
from unittest import TestCase
from unittest.mock import patch

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

