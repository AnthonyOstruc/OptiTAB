"""Accès aux contenus pédagogiques (subscriptions/acces_contenu.py).

- Seule l'administration crée, modifie, supprime ou duplique un contenu.
- La liste ne transmet les corrigés, le texte des cours et les réponses des quiz
  qu'aux comptes qui y ont accès (abonnés, chapitre de découverte, contenu gratuit).
"""
from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from cours.models import Cours
from curriculum.models import Exercice, Matiere, MatiereContexte, Notion, Theme
from pays.models import Niveau, Pays
from quiz.models import Quiz
from subscriptions.models import SubscriptionPlan, UserSubscription

User = get_user_model()


class AccesContenuTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        pays = Pays.objects.create(nom="France", code_iso="FRA")
        cls.niveau = Niveau.objects.create(pays=pays, nom="Seconde", ordre=1)
        matiere = Matiere.objects.create(titre="Mathématiques", ordre=1)
        contexte = MatiereContexte.objects.create(matiere=matiere, niveau=cls.niveau)
        theme = Theme.objects.create(titre="Fonctions", matiere=matiere, contexte=contexte, ordre=1)
        cls.notion = Notion.objects.create(theme=theme, titre="Payante", ordre=1)
        cls.demo = Notion.objects.create(theme=theme, titre="Découverte", ordre=2)
        cls.niveau.demo_notion = cls.demo
        cls.niveau.save()

        cls.exercice = Exercice.objects.create(
            notion=cls.notion, titre="Ex payant", contenu="Énoncé", question="Q ?",
            reponse_correcte="RÉPONSE SECRÈTE", etapes="ÉTAPES SECRÈTES",
        )
        cls.exercice_gratuit = Exercice.objects.create(
            notion=cls.notion, titre="Ex gratuit", contenu="Énoncé", question="Q ?",
            reponse_correcte="réponse libre", etapes="étapes libres", access_scope="free",
        )
        cls.exercice_demo = Exercice.objects.create(
            notion=cls.demo, titre="Ex démo", contenu="Énoncé", question="Q ?",
            reponse_correcte="réponse démo", etapes="étapes démo",
        )
        Cours.objects.create(notion=cls.notion, titre="Cours payant", contenu="TEXTE DU COURS")
        Quiz.objects.create(notion=cls.notion, titre="Quiz", contenu="", questions_data=[{"q": 1, "bonne": "A"}], solution="SOLUTION")

        cls.gratuit = User.objects.create_user(email="gratuit@example.com", password="x", first_name="G", last_name="G", niveau_pays=cls.niveau)
        cls.abonne = User.objects.create_user(email="abonne@example.com", password="x", first_name="A", last_name="A", niveau_pays=cls.niveau)
        cls.admin = User.objects.create_user(email="admin@example.com", password="x", first_name="Ad", last_name="Ad", is_staff=True)
        plan = SubscriptionPlan.objects.create(
            name="Mensuel", plan_type="basic", plan_mode="subscription", billing_period="monthly",
            price=Decimal("7.99"), stripe_price_id="price_acces_contenu", features=[],
        )
        UserSubscription.objects.create(
            user=cls.abonne, plan=plan, status="active", stripe_subscription_id="sub_acces_contenu",
            current_period_start=timezone.now() - timedelta(days=1),
            current_period_end=timezone.now() + timedelta(days=29), niveau_pays=cls.niveau,
        )

    def _client(self, user):
        client = APIClient()
        client.credentials(HTTP_ACCEPT="application/json")
        client.force_authenticate(user=user)
        return client

    # --- Écriture réservée à l'administration -------------------------------

    def test_free_and_subscribed_accounts_cannot_change_content(self):
        for user in (self.gratuit, self.abonne):
            client = self._client(user)
            for methode, url in (
                ("delete", f"/api/notions/{self.notion.id}/"),
                ("patch", f"/api/notions/{self.notion.id}/"),
                ("post", f"/api/notions/{self.notion.id}/duplicate/"),
                ("delete", f"/api/exercices/{self.exercice.id}/"),
                ("patch", f"/api/exercices/{self.exercice.id}/"),
                ("post", "/api/themes/"),
                ("patch", f"/api/niveaux/{self.niveau.id}/"),
                ("delete", f"/api/cours/cours/{Cours.objects.get().id}/"),
                ("delete", f"/api/quiz/quiz/{Quiz.objects.get().id}/"),
            ):
                response = getattr(client, methode)(url, {"titre": "piraté"}, format="json")
                self.assertEqual(response.status_code, 403, f"{user.email} {methode} {url}")
        self.assertTrue(Notion.objects.filter(pk=self.notion.pk, titre="Payante").exists())
        self.assertTrue(Exercice.objects.filter(pk=self.exercice.pk).exists())

    def test_admin_can_change_content(self):
        client = self._client(self.admin)
        response = client.patch(f"/api/notions/{self.notion.id}/", {"titre": "Renommée"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Notion.objects.get(pk=self.notion.pk).titre, "Renommée")

    def test_anonymous_cannot_change_content(self):
        response = APIClient().delete(f"/api/notions/{self.notion.id}/")
        self.assertIn(response.status_code, (401, 403))

    # --- Corrigés réservés aux comptes qui y ont accès -----------------------

    def _exercices(self, user, notion):
        data = self._client(user).get("/api/exercices/", {"notion": notion.id}).json()
        return {item["titre"]: item for item in data}

    def test_free_account_does_not_receive_paid_solutions(self):
        items = self._exercices(self.gratuit, self.notion)
        payant = items["Ex payant"]
        self.assertEqual(payant["reponse_correcte"], "")
        self.assertEqual(payant["etapes"], "")
        self.assertTrue(payant["acces_limite"])
        self.assertEqual(payant["question"], "Q ?")  # l'énoncé reste visible
        self.assertEqual(items["Ex gratuit"]["reponse_correcte"], "réponse libre")

    def test_free_account_keeps_the_demo_chapter(self):
        item = self._exercices(self.gratuit, self.demo)["Ex démo"]
        self.assertEqual(item["reponse_correcte"], "réponse démo")
        self.assertNotIn("acces_limite", item)

    def test_subscriber_and_admin_receive_everything(self):
        for user in (self.abonne, self.admin):
            item = self._exercices(user, self.notion)["Ex payant"]
            self.assertEqual(item["reponse_correcte"], "RÉPONSE SECRÈTE")
            self.assertNotIn("acces_limite", item)

    def test_free_account_does_not_receive_course_text_or_quiz_answers(self):
        client = self._client(self.gratuit)
        cours = client.get("/api/cours/cours/", {"notion": self.notion.id}).json()[0]
        self.assertEqual(cours["contenu"], "")
        quiz = client.get("/api/quiz/quiz/", {"notion": self.notion.id}).json()[0]
        self.assertEqual(quiz["questions_data"], [])
        self.assertEqual(quiz["solution"], "")

    def test_admin_pagination_still_works(self):
        data = self._client(self.admin).get("/api/exercices/", {"limit": 1, "offset": 0}).json()
        self.assertEqual(data["count"], 3)
        self.assertEqual(len(data["results"]), 1)
