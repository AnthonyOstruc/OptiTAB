from __future__ import annotations

from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from users.models import ParentChild


class CreateChildAccountViewTests(TestCase):
    def setUp(self):
        self.api_client = APIClient()

    def _create_user(self, *, tag: str, role: str = "student"):
        User = get_user_model()
        return User.objects.create_user(
            email=f"{tag}@example.com",
            first_name="Test",
            last_name="User",
            password="test-password",
            is_active=True,
            role=role,
        )

    def test_student_user_can_create_child_and_is_promoted_to_parent(self):
        parent_user = self._create_user(tag="creator-student", role="student")
        self.api_client.force_authenticate(user=parent_user)

        with patch(
            "core.services.EmailService.send_child_account_created",
            return_value=True,
        ):
            response = self.api_client.post(
                "/api/users/me/children/create/",
                data={
                    "email": "child-created@example.com",
                    "first_name": "Child",
                    "last_name": "Account",
                },
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        parent_user.refresh_from_db()
        self.assertEqual(parent_user.role, "parent")

        User = get_user_model()
        child = User.objects.get(email="child-created@example.com")
        self.assertEqual(child.role, "student")
        self.assertTrue(child.is_active)

        link = ParentChild.objects.get(parent=parent_user, child=child)
        self.assertEqual(link.status, ParentChild.STATUS_ACCEPTED)
        self.assertIsNotNone(link.responded_at)

    def test_parent_user_can_create_child_without_role_change(self):
        parent_user = self._create_user(tag="creator-parent", role="parent")
        self.api_client.force_authenticate(user=parent_user)

        with patch(
            "core.services.EmailService.send_child_account_created",
            return_value=True,
        ):
            response = self.api_client.post(
                "/api/users/me/children/create/",
                data={
                    "email": "child-parent-flow@example.com",
                    "first_name": "Child",
                    "last_name": "ParentFlow",
                },
                format="json",
            )

        self.assertEqual(response.status_code, 200)
        parent_user.refresh_from_db()
        self.assertEqual(parent_user.role, "parent")

    def test_returns_400_when_email_already_exists(self):
        parent_user = self._create_user(tag="creator-duplicate", role="student")
        existing_child = self._create_user(tag="existing-child", role="student")
        self.api_client.force_authenticate(user=parent_user)

        response = self.api_client.post(
            "/api/users/me/children/create/",
            data={
                "email": existing_child.email,
                "first_name": "Child",
                "last_name": "Duplicate",
            },
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn("existe déjà", str(response.data.get("message", "")))
