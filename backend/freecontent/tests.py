from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from curriculum.models import Matiere, MatiereContexte, Notion, Theme
from pays.models import Niveau, Pays
from synthesis.models import SynthesisSheet


def _build_notion_tree():
    pays = Pays.objects.create(nom='France', code_iso='FRA')
    niveau = Niveau.objects.create(pays=pays, nom='Premiere', ordre=1)
    matiere = Matiere.objects.create(titre='Mathematiques', ordre=1)
    contexte = MatiereContexte.objects.create(matiere=matiere, niveau=niveau)
    theme = Theme.objects.create(
        titre='Fonctions',
        matiere=matiere,
        contexte=contexte,
        ordre=1,
    )
    notion = Notion.objects.create(theme=theme, titre='Fonctions usuelles', ordre=1)
    return notion


class FreeSummarySheetTypeTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.notion = _build_notion_tree()
        self.summary_sheet = SynthesisSheet.objects.create(
            notion=self.notion,
            titre='Resume fonctions',
            summary='Contenu synthese',
            access_scope=SynthesisSheet.ACCESS_SCOPE_FREE,
            sheet_type=SynthesisSheet.SHEET_TYPE_SUMMARY,
        )
        self.table_sheet = SynthesisSheet.objects.create(
            notion=self.notion,
            titre='Tableau derivees',
            summary='Contenu tableau',
            access_scope=SynthesisSheet.ACCESS_SCOPE_FREE,
            sheet_type=SynthesisSheet.SHEET_TYPE_TABLE,
        )

    def test_free_summary_list_excludes_table_type(self):
        response = self.client.get('/api/free/learning-resources/', {'type': 'summary'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        results = response.data.get('results', response.data)
        returned_ids = {item['id'] for item in results}

        self.assertIn(self.summary_sheet.id, returned_ids)
        self.assertNotIn(self.table_sheet.id, returned_ids)

    def test_free_summary_retrieve_slug_rejects_table_sheet(self):
        summary_response = self.client.get(
            f'/api/free/learning-resources/synthese-gratuite-{self.summary_sheet.id}/'
        )
        table_response = self.client.get(
            f'/api/free/learning-resources/synthese-gratuite-{self.table_sheet.id}/'
        )

        self.assertEqual(summary_response.status_code, status.HTTP_200_OK)
        self.assertEqual(table_response.status_code, status.HTTP_404_NOT_FOUND)
