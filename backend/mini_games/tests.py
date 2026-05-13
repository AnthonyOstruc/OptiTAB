from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class MathRunAdminAccessTests(TestCase):
    def setUp(self):
        user_model = get_user_model()
        self.admin = user_model.objects.create_user(
            email='mathrun-admin@example.com',
            first_name='Math',
            last_name='Admin',
            password='test-password',
            is_active=True,
            is_staff=True,
        )
        self.student = user_model.objects.create_user(
            email='mathrun-student@example.com',
            first_name='Math',
            last_name='Student',
            password='test-password',
            is_active=True,
        )
        self.client = APIClient()

    def test_admin_can_submit_score_and_read_leaderboard(self):
        self.client.force_authenticate(self.admin)

        submit_response = self.client.post(
            reverse('mathrun-score'),
            {'score': 12, 'category': 'all'},
            format='json',
        )
        self.assertEqual(submit_response.status_code, 200)

        leaderboard_response = self.client.get(reverse('mathrun-leaderboard'))
        self.assertEqual(leaderboard_response.status_code, 200)
        self.assertEqual(leaderboard_response.data['leaderboard'][0]['score'], 12)

    def test_non_admin_cannot_access_math_run_api(self):
        self.client.force_authenticate(self.student)

        submit_response = self.client.post(
            reverse('mathrun-score'),
            {'score': 12, 'category': 'all'},
            format='json',
        )
        self.assertEqual(submit_response.status_code, 403)

        leaderboard_response = self.client.get(reverse('mathrun-leaderboard'))
        self.assertEqual(leaderboard_response.status_code, 403)

    def test_anonymous_cannot_access_math_run_api(self):
        submit_response = self.client.post(
            reverse('mathrun-score'),
            {'score': 12, 'category': 'all'},
            format='json',
        )
        self.assertEqual(submit_response.status_code, 401)

        leaderboard_response = self.client.get(reverse('mathrun-leaderboard'))
        self.assertEqual(leaderboard_response.status_code, 401)
