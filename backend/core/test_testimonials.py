"""Tests des temoignages (captures WhatsApp / SMS de la page « lien en bio »).

Couvre en priorite le garde-fou RGPD : rien ne doit pouvoir etre publie
sans accord confirme, quelle que soit la voie d'ecriture utilisee.
"""
import shutil
import tempfile
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db.models.fields.files import FieldFile
from django.test import TestCase, override_settings
from rest_framework import status
from rest_framework.test import APIClient

from core.models import BioLandingSettings, Testimonial

MEDIA_ROOT = tempfile.mkdtemp()

# Sans cette bascule, les tests televersent sur le vrai bucket S3 : quand
# AWS_* est renseigne, `STORAGES['default']` pointe sur S3 et `MEDIA_ROOT`
# est purement ignore. On force le disque local le temps des tests.
LOCAL_STORAGE = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'django.contrib.staticfiles.storage.StaticFilesStorage'},
}


def isolated_media(cls):
    """Decorateur : media sur disque temporaire, jamais sur S3."""
    return override_settings(MEDIA_ROOT=MEDIA_ROOT, STORAGES=LOCAL_STORAGE)(cls)


def make_image(name='capture.png'):
    """Un PNG 1x1 valide, suffisant pour ImageField (Pillow le lit)."""
    png_bytes = (
        b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
        b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01'
        b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
    )
    return SimpleUploadedFile(name, png_bytes, content_type='image/png')


@isolated_media
class TestimonialModelTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_publication_sans_accord_autorisee(self):
        """L'accord est une trace interne : il ne conditionne plus la publication.

        Choix explicite du proprietaire du site. Le champ reste disponible
        dans l'admin Django pour garder une trace si besoin.
        """
        testimonial = Testimonial.objects.create(
            author="Maman d'élève",
            image=make_image(),
            consent_confirmed=False,
            is_published=True,
        )
        testimonial.refresh_from_db()
        self.assertTrue(testimonial.is_published)

    def test_mise_en_avant_impossible_si_non_publie(self):
        testimonial = Testimonial.objects.create(
            author="Papa d'élève",
            image=make_image(),
            consent_confirmed=True,
            is_published=False,
            is_featured=True,
        )
        testimonial.refresh_from_db()
        self.assertFalse(testimonial.is_featured)

    def test_un_seul_temoignage_mis_en_avant(self):
        first = Testimonial.objects.create(
            author='Élève',
            image=make_image(),
            consent_confirmed=True,
            is_published=True,
            is_featured=True,
        )
        second = Testimonial.objects.create(
            author='Étudiant',
            image=make_image(),
            consent_confirmed=True,
            is_published=True,
            is_featured=True,
        )

        first.refresh_from_db()
        second.refresh_from_db()
        self.assertFalse(first.is_featured)
        self.assertTrue(second.is_featured)


@isolated_media
class TestimonialPublicApiTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()

    def test_seuls_les_temoignages_publies_sont_exposes(self):
        Testimonial.objects.create(
            author='Élève',
            role='Terminale',
            image=make_image(),
            consent_confirmed=True,
            is_published=True,
        )
        Testimonial.objects.create(
            author='Étudiant',
            role='Prépa MPSI',
            image=make_image(),
            consent_confirmed=True,
            is_published=False,
        )

        response = self.client.get('/api/testimonials/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        roles = [item['role'] for item in response.data]
        self.assertEqual(roles, ['Terminale'])

    def test_charge_utile_publique_sans_donnee_interne(self):
        Testimonial.objects.create(
            author="Maman d'élève",
            role='Terminale',
            image=make_image(),
            alt_text='Message WhatsApp',
            consent_confirmed=True,
            is_published=True,
        )

        response = self.client.get('/api/testimonials/')
        item = response.data[0]
        self.assertEqual(
            set(item.keys()),
            {'id', 'name', 'author', 'role', 'channel', 'src', 'alt', 'featured'},
        )
        # Aucun champ de moderation ne doit fuiter cote public.
        self.assertNotIn('consent_confirmed', item)
        self.assertNotIn('is_published', item)
        self.assertNotIn('name_consent', item)
        self.assertNotIn('display_name', item)


class BioLandingVisibilityTests(TestCase):
    """Mise en ligne de la page /avis, pilotee depuis le studio."""

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_user(
            email='studio@optitab.net',
            first_name='Studio',
            last_name='Admin',
            password='motdepasse-solide',
            is_staff=True,
        )

    def test_hors_ligne_par_defaut(self):
        """Rien ne doit partir en ligne sans action explicite."""
        response = self.client.get('/api/bio-landing/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['published'])

    def test_statut_lisible_sans_authentification(self):
        """La page publique doit pouvoir interroger le statut."""
        BioLandingSettings.load()
        response = self.client.get('/api/bio-landing/status/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_bascule_reservee_aux_admins(self):
        response = self.client.patch(
            '/api/admin/bio-landing/', {'published': True}, format='json'
        )
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertFalse(BioLandingSettings.load().is_published)

    def test_mise_en_ligne_et_retrait(self):
        self.client.force_authenticate(self.admin)

        online = self.client.patch(
            '/api/admin/bio-landing/', {'published': True}, format='json'
        )
        self.assertEqual(online.status_code, status.HTTP_200_OK)
        self.assertTrue(online.data['published'])
        self.assertTrue(self.client.get('/api/bio-landing/status/').data['published'])

        offline = self.client.patch(
            '/api/admin/bio-landing/', {'published': False}, format='json'
        )
        self.assertFalse(offline.data['published'])
        self.assertFalse(self.client.get('/api/bio-landing/status/').data['published'])

    def test_valeur_invalide_refusee(self):
        self.client.force_authenticate(self.admin)
        response = self.client.patch(
            '/api/admin/bio-landing/', {'published': 'peut-etre'}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_singleton_unique(self):
        """Aucun second enregistrement ne doit pouvoir apparaitre."""
        BioLandingSettings.load()
        BioLandingSettings(is_published=True).save()
        self.assertEqual(BioLandingSettings.objects.count(), 1)


@isolated_media
class TestimonialAdminApiTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def setUp(self):
        self.client = APIClient()
        # CustomUser utilise l'email comme identifiant et exige prenom + nom.
        self.admin = get_user_model().objects.create_user(
            email='admin@optitab.net',
            first_name='Studio',
            last_name='Admin',
            password='motdepasse-solide',
            is_staff=True,
        )

    def test_acces_refuse_sans_authentification(self):
        response = self.client.get('/api/admin/testimonials/')
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_creation_avec_upload(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            '/api/admin/testimonials/create/',
            {
                "author": "Maman d'élève",
                'role': 'Terminale',
                'channel': 'whatsapp',
                'image': make_image(),
                'consent_confirmed': 'true',
                'is_published': 'true',
            },
            format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['src'])
        self.assertTrue(Testimonial.objects.filter(author="Maman d'élève").exists())

    def test_creation_publiee_sans_accord(self):
        """L'API n'exige plus l'accord pour publier."""
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            '/api/admin/testimonials/create/',
            {
                'author': 'Élève',
                'role': 'Terminale',
                'image': make_image(),
                'consent_confirmed': 'false',
                'is_published': 'true',
            },
            format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['is_published'])

    def test_creation_refusee_sans_image(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            '/api/admin/testimonials/create/',
            {'author': 'Élève'},
            format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('image', response.data)

    def test_profil_libre_refuse(self):
        """Aucun nom ni prenom ne doit pouvoir entrer par l'API.

        Le studio propose une liste fermee, mais un appel direct doit etre
        rejete lui aussi : c'est la garantie que la page ne peut pas afficher
        de prenom, meme par erreur de manipulation.
        """
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            '/api/admin/testimonials/create/',
            {
                'author': 'Sandra M.',
                'image': make_image(),
                'consent_confirmed': 'true',
            },
            format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('author', response.data)
        self.assertEqual(Testimonial.objects.count(), 0)

    def test_prenom_refuse_sans_accord_nominatif(self):
        """Le prenom exige un accord distinct de celui de publication."""
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            '/api/admin/testimonials/create/',
            {
                'author': 'Élève',
                'display_name': 'Sandra M.',
                'name_consent': 'false',
                'image': make_image(),
                'consent_confirmed': 'true',
            },
            format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name_consent', response.data)

    def test_prenom_affiche_avec_accord_nominatif(self):
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            '/api/admin/testimonials/create/',
            {
                'author': "Maman d'élève",
                'role': 'Terminale',
                'display_name': 'Sandra M.',
                'name_consent': 'true',
                'image': make_image(),
                'consent_confirmed': 'true',
                'is_published': 'true',
            },
            format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        public = self.client.get('/api/testimonials/')
        self.assertEqual(public.data[0]['name'], 'Sandra M.')

    def test_retrait_accord_efface_le_prenom(self):
        """Retirer l'accord ne doit pas laisser le prenom en base."""
        testimonial = Testimonial.objects.create(
            author='Élève',
            display_name='Sandra M.',
            name_consent=True,
            image=make_image(),
            consent_confirmed=True,
            is_published=True,
        )
        self.assertEqual(testimonial.display_name, 'Sandra M.')

        testimonial.name_consent = False
        testimonial.save()
        testimonial.refresh_from_db()

        self.assertEqual(testimonial.display_name, '')
        self.assertEqual(testimonial.public_name, '')

    def test_prenom_absent_de_l_api_publique_sans_accord(self):
        """Meme si la colonne contenait un prenom, l'API ne l'expose pas."""
        testimonial = Testimonial.objects.create(
            author='Élève',
            role='Terminale',
            image=make_image(),
            consent_confirmed=True,
            is_published=True,
        )
        # Ecriture directe en base, sans passer par save() : cas limite.
        Testimonial.objects.filter(pk=testimonial.pk).update(
            display_name='Sandra M.', name_consent=False
        )

        response = self.client.get('/api/testimonials/')
        self.assertEqual(response.data[0]['name'], '')

    def test_profil_facultatif(self):
        """Un temoignage peut n'afficher que le niveau, sans aucun profil."""
        self.client.force_authenticate(self.admin)
        response = self.client.post(
            '/api/admin/testimonials/create/',
            {
                'role': 'Terminale',
                'image': make_image(),
                'consent_confirmed': 'true',
                'is_published': 'true',
            },
            format='multipart',
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['author'], '')

    def test_reordonnancement(self):
        self.client.force_authenticate(self.admin)
        a = Testimonial.objects.create(author='Élève', role='Seconde', image=make_image(), ordre=0)
        b = Testimonial.objects.create(author='Étudiant', role='BTS', image=make_image(), ordre=1)

        response = self.client.post(
            '/api/admin/testimonials/reorder/',
            {'order': [b.id, a.id]},
            format='json',
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        a.refresh_from_db()
        b.refresh_from_db()
        self.assertEqual(b.ordre, 0)
        self.assertEqual(a.ordre, 1)

    def test_suppression(self):
        self.client.force_authenticate(self.admin)
        testimonial = Testimonial.objects.create(author='Élève', role='À supprimer', image=make_image())

        # Accept explicite : sans lui, DRF sert la page HTML navigable et
        # renvoie 200 au lieu de 204. Axios envoie bien application/json.
        response = self.client.delete(
            f'/api/admin/testimonials/{testimonial.id}/',
            HTTP_ACCEPT='application/json',
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Testimonial.objects.filter(pk=testimonial.pk).exists())

    def test_suppression_aboutit_meme_si_le_stockage_refuse(self):
        """L'utilisateur IAM du bucket n'a pas toujours le droit s3:DeleteObject.

        Dans ce cas la ligne doit quand meme disparaitre, sinon l'admin se
        retrouve avec un temoignage impossible a retirer de la page.
        """
        self.client.force_authenticate(self.admin)
        testimonial = Testimonial.objects.create(author='Élève', role='Stockage KO', image=make_image())

        with patch.object(
            FieldFile, 'delete', side_effect=Exception('AccessDenied: s3:DeleteObject')
        ):
            response = self.client.delete(
                f'/api/admin/testimonials/{testimonial.id}/',
                HTTP_ACCEPT='application/json',
            )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Testimonial.objects.filter(pk=testimonial.pk).exists())
