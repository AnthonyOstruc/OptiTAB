from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from curriculum.models import Matiere, MatiereContexte, Notion, Theme
from pays.models import Niveau, Pays
from synthesis.models import SynthesisSheet


def _build_notion_tree():
    pays = Pays.objects.create(nom='France', code_iso='FRA')
    niveau = Niveau.objects.create(pays=pays, nom='Terminale', ordre=1)
    matiere = Matiere.objects.create(titre='Mathematiques', ordre=1)
    contexte = MatiereContexte.objects.create(matiere=matiere, niveau=niveau)
    theme = Theme.objects.create(
        titre='Analyse',
        matiere=matiere,
        contexte=contexte,
        ordre=1,
    )
    notion = Notion.objects.create(theme=theme, titre='Derivation', ordre=1)
    return notion


class SynthesisSheetTypeTests(TestCase):
    def setUp(self):
        self.notion = _build_notion_tree()
        user_model = get_user_model()
        self.admin = user_model.objects.create_user(
            email='admin@example.com',
            first_name='Admin',
            last_name='User',
            password='password123',
            is_staff=True,
            is_active=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.admin)

    def test_create_without_sheet_type_defaults_to_summary(self):
        response = self.client.post(
            '/api/sheets/',
            {
                'notion': self.notion.id,
                'titre': 'Fiche derivee',
                'summary': 'Contenu test',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created = SynthesisSheet.objects.get(notion=self.notion, titre='Fiche derivee')
        self.assertEqual(created.sheet_type, SynthesisSheet.SHEET_TYPE_SUMMARY)

    def test_api_filter_by_sheet_type(self):
        summary = SynthesisSheet.objects.create(
            notion=self.notion,
            titre='Limites',
            summary='Sheet summary',
            sheet_type=SynthesisSheet.SHEET_TYPE_SUMMARY,
        )
        table = SynthesisSheet.objects.create(
            notion=self.notion,
            titre='Limites',
            summary='Sheet table',
            sheet_type=SynthesisSheet.SHEET_TYPE_TABLE,
        )

        summary_response = self.client.get('/api/sheets/', {'sheet_type': 'summary'})
        table_response = self.client.get('/api/sheets/', {'sheet_type': 'table'})

        self.assertEqual(summary_response.status_code, status.HTTP_200_OK)
        self.assertEqual(table_response.status_code, status.HTTP_200_OK)

        summary_ids = {item['id'] for item in summary_response.data}
        table_ids = {item['id'] for item in table_response.data}

        self.assertIn(summary.id, summary_ids)
        self.assertNotIn(table.id, summary_ids)
        self.assertIn(table.id, table_ids)
        self.assertNotIn(summary.id, table_ids)

    def test_uniqueness_allows_same_title_for_different_types(self):
        SynthesisSheet.objects.create(
            notion=self.notion,
            titre='Puissances',
            summary='Version synthese',
            sheet_type=SynthesisSheet.SHEET_TYPE_SUMMARY,
        )
        SynthesisSheet.objects.create(
            notion=self.notion,
            titre='Puissances',
            summary='Version tableau',
            sheet_type=SynthesisSheet.SHEET_TYPE_TABLE,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                SynthesisSheet.objects.create(
                    notion=self.notion,
                    titre='Puissances',
                    summary='Version synthese bis',
                    sheet_type=SynthesisSheet.SHEET_TYPE_SUMMARY,
                )

    def test_duplicate_keeps_sheet_type(self):
        original = SynthesisSheet.objects.create(
            notion=self.notion,
            titre='Integrales',
            summary='Version tableau',
            sheet_type=SynthesisSheet.SHEET_TYPE_TABLE,
        )

        response = self.client.post(f'/api/sheets/{original.id}/duplicate/')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['sheet_type'], SynthesisSheet.SHEET_TYPE_TABLE)

        duplicate = SynthesisSheet.objects.get(pk=response.data['id'])
        self.assertEqual(duplicate.sheet_type, SynthesisSheet.SHEET_TYPE_TABLE)
        self.assertNotEqual(duplicate.id, original.id)


class SynthesisSheetAccessTests(TestCase):
    def setUp(self):
        self.notion = _build_notion_tree()
        self.sheet = SynthesisSheet.objects.create(
            notion=self.notion,
            titre='Fiche accessible en liste',
            summary='Contenu',
            sheet_type=SynthesisSheet.SHEET_TYPE_SUMMARY,
        )
        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            email='student@example.com',
            first_name='Student',
            last_name='User',
            password='password123',
            is_active=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_list_is_accessible_for_authenticated_non_subscriber(self):
        response = self.client.get('/api/sheets/', {'matiere': self.notion.theme.matiere_id, 'sheet_type': 'summary'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = {item['id'] for item in response.data}
        self.assertIn(self.sheet.id, returned_ids)

    def test_retrieve_still_requires_active_subscription_or_pass(self):
        response = self.client.get(f'/api/sheets/{self.sheet.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
