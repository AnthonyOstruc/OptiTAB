from __future__ import annotations

from unittest import TestCase

from subscriptions.helpers import _build_pass_description


class PassDescriptionTests(TestCase):
    def test_keeps_single_pass_prefix_when_plan_already_starts_with_pass(self):
        description = _build_pass_description("Pass Annuel", level_label="1ere - France")
        self.assertEqual(description, "Pass Annuel - 1ere - France")

    def test_adds_pass_prefix_when_missing(self):
        description = _build_pass_description("Annuel", level_label="Terminale - France")
        self.assertEqual(description, "Pass Annuel - Terminale - France")

    def test_handles_empty_plan_name(self):
        description = _build_pass_description("", level_label="Terminale - France")
        self.assertEqual(description, "Pass - Terminale - France")

    def test_handles_empty_level_label(self):
        description = _build_pass_description("Pass 1 jour")
        self.assertEqual(description, "Pass 1 jour")
