from __future__ import annotations

from io import StringIO
from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone

from subscriptions.models import AccessPass, SubscriptionPlan, UserSubscription


class PassExpirationEmailCommandTests(TestCase):
    def _create_user(self, *, tag: str):
        User = get_user_model()
        return User.objects.create_user(
            email=f"{tag}@example.com",
            first_name="Test",
            last_name="User",
            password="test-password",
            is_active=True,
        )

    def _create_pass_plan(self, *, tag: str):
        return SubscriptionPlan.objects.create(
            name="Pass test",
            plan_type="basic",
            plan_mode="one_time",
            billing_period="daily",
            price=Decimal("1.00"),
            stripe_price_id=f"price_{tag}",
            features=[],
            access_days=1,
            is_active=True,
        )

    def _create_subscription_plan(self, *, tag: str):
        return SubscriptionPlan.objects.create(
            name="Mensuel",
            plan_type="basic",
            plan_mode="subscription",
            billing_period="monthly",
            price=Decimal("4.99"),
            stripe_price_id=f"price_sub_{tag}",
            features=[],
            is_active=True,
        )

    def test_send_once_when_pass_expires(self):
        user = self._create_user(tag="pass-expire-send")
        plan = self._create_pass_plan(tag="pass-expire-send")
        access_pass = AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=timezone.now() - timedelta(days=2),
            ends_at=timezone.now() - timedelta(hours=1),
            stripe_payment_intent_id="pi_pass_expire_send",
            expiration_email_sent=False,
            is_revoked=False,
        )

        with patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification",
            return_value=True,
        ) as send_email, patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification_to_admin",
            return_value=True,
        ) as send_admin_email:
            call_command("send_pass_expiration_emails", hours_ago=24, verbosity=0)

        access_pass.refresh_from_db()
        self.assertTrue(access_pass.expiration_email_sent)
        send_email.assert_called_once()
        send_admin_email.assert_called_once()

    def test_idempotent_no_second_email(self):
        user = self._create_user(tag="pass-expire-idempotent")
        plan = self._create_pass_plan(tag="pass-expire-idempotent")
        access_pass = AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=timezone.now() - timedelta(days=2),
            ends_at=timezone.now() - timedelta(hours=1),
            stripe_payment_intent_id="pi_pass_expire_idempotent",
            expiration_email_sent=False,
            is_revoked=False,
        )

        with patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification",
            return_value=True,
        ) as send_email, patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification_to_admin",
            return_value=True,
        ) as send_admin_email:
            call_command("send_pass_expiration_emails", hours_ago=24, verbosity=0)
            call_command("send_pass_expiration_emails", hours_ago=24, verbosity=0)

        access_pass.refresh_from_db()
        self.assertTrue(access_pass.expiration_email_sent)
        self.assertEqual(send_email.call_count, 1)
        self.assertEqual(send_admin_email.call_count, 1)

    def test_skip_if_user_has_active_subscription_marks_processed(self):
        user = self._create_user(tag="pass-expire-skip-sub")
        pass_plan = self._create_pass_plan(tag="pass-expire-skip-sub")
        sub_plan = self._create_subscription_plan(tag="pass-expire-skip-sub")
        UserSubscription.objects.create(
            user=user,
            plan=sub_plan,
            status="active",
            current_period_end=timezone.now() + timedelta(days=30),
        )

        access_pass = AccessPass.objects.create(
            user=user,
            plan=pass_plan,
            starts_at=timezone.now() - timedelta(days=2),
            ends_at=timezone.now() - timedelta(hours=1),
            stripe_payment_intent_id="pi_pass_expire_skip_sub",
            expiration_email_sent=False,
            is_revoked=False,
        )

        with patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification",
            return_value=True,
        ) as send_email, patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification_to_admin",
            return_value=True,
        ) as send_admin_email:
            call_command("send_pass_expiration_emails", hours_ago=24, verbosity=0)

        access_pass.refresh_from_db()
        self.assertTrue(access_pass.expiration_email_sent)
        send_email.assert_not_called()
        send_admin_email.assert_not_called()

    def test_skip_if_other_active_pass_exists_marks_processed(self):
        user = self._create_user(tag="pass-expire-skip-other-pass")
        plan = self._create_pass_plan(tag="pass-expire-skip-other-pass")

        expired_pass = AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=timezone.now() - timedelta(days=2),
            ends_at=timezone.now() - timedelta(hours=1),
            stripe_payment_intent_id="pi_pass_expire_skip_other_expired",
            expiration_email_sent=False,
            is_revoked=False,
        )
        AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=timezone.now(),
            ends_at=timezone.now() + timedelta(days=1),
            stripe_payment_intent_id="pi_pass_expire_skip_other_active",
            expiration_email_sent=False,
            is_revoked=False,
        )

        with patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification",
            return_value=True,
        ) as send_email, patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification_to_admin",
            return_value=True,
        ) as send_admin_email:
            call_command("send_pass_expiration_emails", hours_ago=24, verbosity=0)

        expired_pass.refresh_from_db()
        self.assertTrue(expired_pass.expiration_email_sent)
        send_email.assert_not_called()
        send_admin_email.assert_not_called()

    def test_revoked_pass_is_ignored(self):
        user = self._create_user(tag="pass-expire-revoked")
        plan = self._create_pass_plan(tag="pass-expire-revoked")
        revoked_pass = AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=timezone.now() - timedelta(days=2),
            ends_at=timezone.now() - timedelta(hours=1),
            stripe_payment_intent_id="pi_pass_expire_revoked",
            expiration_email_sent=False,
            is_revoked=True,
        )

        with patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification",
            return_value=True,
        ) as send_email, patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification_to_admin",
            return_value=True,
        ) as send_admin_email:
            call_command("send_pass_expiration_emails", hours_ago=24, verbosity=0)

        revoked_pass.refresh_from_db()
        self.assertFalse(revoked_pass.expiration_email_sent)
        send_email.assert_not_called()
        send_admin_email.assert_not_called()

    def test_command_is_silent_in_normal_mode(self):
        user = self._create_user(tag="pass-expire-silent")
        plan = self._create_pass_plan(tag="pass-expire-silent")
        AccessPass.objects.create(
            user=user,
            plan=plan,
            starts_at=timezone.now() - timedelta(days=2),
            ends_at=timezone.now() - timedelta(hours=1),
            stripe_payment_intent_id="pi_pass_expire_silent",
            expiration_email_sent=False,
            is_revoked=False,
        )
        output = StringIO()

        with patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification",
            return_value=True,
        ), patch(
            "subscriptions.management.commands.send_pass_expiration_emails.EmailService.send_pass_expiration_notification_to_admin",
            return_value=True,
        ):
            call_command(
                "send_pass_expiration_emails",
                hours_ago=24,
                verbosity=0,
                stdout=output,
            )

        self.assertEqual(output.getvalue().strip(), "")
