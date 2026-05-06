import shutil
import tempfile
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from .elevenlabs import generate_speech_mp3, list_filtered_voices
from .models import ReelProject, ReelSlide
from .tts.base import TTSResult


class ReelStudioSpeechPersistenceTests(TestCase):
    def setUp(self):
        self.media_root = tempfile.mkdtemp()
        self.settings_override = override_settings(MEDIA_ROOT=self.media_root)
        self.settings_override.enable()
        self.addCleanup(self.settings_override.disable)
        self.addCleanup(lambda: shutil.rmtree(self.media_root, ignore_errors=True))

        user_model = get_user_model()
        self.user = user_model.objects.create_user(
            email='reel-admin@example.com',
            first_name='Reel',
            last_name='Admin',
            password='test-password',
            is_staff=True,
            is_active=True,
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    @staticmethod
    def fake_tts_result(*, text, provider='', voice_id='', model_id='', output_format='', **kwargs):
        return TTSResult(
            audio_bytes=f'audio:{text}'.encode('utf-8'),
            provider=provider or 'google',
            voice_id=voice_id or 'fr-FR-Standard-F',
            model_id=model_id or 'fr-FR-Standard-F',
            output_format=output_format or 'mp3',
            character_count=len(text),
            cached=False,
        )

    def test_generate_slide_speeches_persists_files_and_project_speech_state(self):
        project = ReelProject.objects.create(title='Reel test', slide_count=2)
        first_slide = ReelSlide.objects.create(
            reel_project=project,
            order=1,
            slide_type=ReelSlide.TYPE_HOOK,
            title='Hook',
            voice_script='Premier script voix.',
        )
        second_slide = ReelSlide.objects.create(
            reel_project=project,
            order=2,
            slide_type=ReelSlide.TYPE_RESULT,
            title='Resultat',
            voice_script='Deuxieme script voix.',
        )

        with patch('reel_studio.views.tts_generate_speech', side_effect=self.fake_tts_result):
            response = self.client.post(
                reverse('reel-project-generate-slide-speeches', args=[project.pk]),
                {'provider': 'google', 'voice_id': 'fr-FR-Standard-F'},
                format='json',
            )

        self.assertEqual(response.status_code, 201)
        first_slide.refresh_from_db()
        second_slide.refresh_from_db()
        project.refresh_from_db()

        self.assertTrue(first_slide.speech_audio.name)
        self.assertTrue(second_slide.speech_audio.name)
        self.assertEqual(first_slide.speech_status, ReelProject.SPEECH_STATUS_READY)
        self.assertEqual(second_slide.speech_status, ReelProject.SPEECH_STATUS_READY)
        self.assertEqual(project.speech_status, ReelProject.SPEECH_STATUS_READY)
        self.assertEqual(project.speech_text, 'Premier script voix.\n\nDeuxieme script voix.')
        self.assertEqual(project.speech_voice_id, 'fr-FR-Standard-F')
        self.assertFalse(project.speech_audio.name)

    def test_generate_single_slide_speech_returns_updated_project_state(self):
        project = ReelProject.objects.create(title='Reel solo', slide_count=1)
        slide = ReelSlide.objects.create(
            reel_project=project,
            order=1,
            slide_type=ReelSlide.TYPE_HOOK,
            title='Hook',
            voice_script='Script voix solo.',
        )

        with patch('reel_studio.views.tts_generate_speech', side_effect=self.fake_tts_result):
            response = self.client.post(
                reverse('reel-slide-generate-speech', args=[slide.pk]),
                {'provider': 'google', 'voice_id': 'fr-FR-Standard-F'},
                format='json',
            )

        self.assertEqual(response.status_code, 201)
        slide.refresh_from_db()
        project.refresh_from_db()

        self.assertTrue(slide.speech_audio.name)
        self.assertEqual(project.speech_status, ReelProject.SPEECH_STATUS_READY)
        self.assertEqual(project.speech_text, 'Script voix solo.')
        self.assertEqual(response.data['project']['speech_status'], ReelProject.SPEECH_STATUS_READY)

    def test_create_project_rejects_blank_title(self):
        response = self.client.post(
            reverse('reel-project-list-create'),
            {'title': '   ', 'slide_count': 0},
            format='json',
        )

        self.assertEqual(response.status_code, 400)
        self.assertIn('title', response.data)
        self.assertFalse(ReelProject.objects.filter(title='').exists())

    def test_save_template_preserves_generated_slide_speech_when_voice_text_is_unchanged(self):
        project = ReelProject.objects.create(title='Reel template', slide_count=1)
        slide = ReelSlide.objects.create(
            reel_project=project,
            order=1,
            slide_type=ReelSlide.TYPE_KATEX,
            title='Ancien titre',
            katex='x=1',
            voice_script='Voix deja generee.',
        )

        with patch('reel_studio.views.tts_generate_speech', side_effect=self.fake_tts_result):
            speech_response = self.client.post(
                reverse('reel-slide-generate-speech', args=[slide.pk]),
                {'provider': 'google', 'voice_id': 'fr-FR-Standard-F'},
                format='json',
            )

        self.assertEqual(speech_response.status_code, 201)
        slide.refresh_from_db()
        previous_audio_name = slide.speech_audio.name
        self.assertTrue(previous_audio_name)

        response = self.client.post(
            reverse('reel-project-save-template', args=[project.pk]),
            {
                'template_text': '\n'.join([
                    'SLIDE 1 | katex',
                    'TITLE: Nouveau titre',
                    'KATEX: x=2',
                    'VOICE: Voix deja generee.',
                    '---',
                    'INSTAGRAM_DESCRIPTION:',
                    'Description sauvegardee.',
                ])
            },
            format='json',
        )

        self.assertEqual(response.status_code, 200)
        slide.refresh_from_db()
        project.refresh_from_db()

        self.assertEqual(slide.title, 'Nouveau titre')
        self.assertEqual(slide.katex, 'x=2')
        self.assertEqual(slide.speech_audio.name, previous_audio_name)
        self.assertEqual(slide.speech_status, ReelProject.SPEECH_STATUS_READY)
        self.assertEqual(project.speech_status, ReelProject.SPEECH_STATUS_READY)
        self.assertEqual(project.instagram_caption, 'Description sauvegardee.')

    @override_settings(ELEVENLABS_API_KEY='test-key', ELEVENLABS_VOICE_ID='aQROLel5sQbj1vuIVi6B')
    def test_builtin_voices_are_first_elevenlabs_choices(self):
        class FakeResponse:
            status_code = 200
            reason = 'OK'

            @staticmethod
            def json():
                return {
                    'voices': [
                        {
                            'voice_id': 'other-voice',
                            'name': 'Anna B',
                            'category': 'professional',
                            'labels': {'language': 'fr', 'accent': 'parisian'},
                        },
                    ]
                }

        with patch('reel_studio.elevenlabs.requests.get', return_value=FakeResponse()):
            voices = list_filtered_voices(language='fr', accent='parisian', include_fallback=True)

        self.assertGreaterEqual(len(voices), 2)
        self.assertEqual(voices[0]['voice_id'], 'aQROLel5sQbj1vuIVi6B')
        self.assertEqual(voices[0]['name'], 'Nicolas')
        self.assertEqual(voices[1]['voice_id'], 'WQKwBV2Uzw1gSGr69N8I')
        self.assertEqual(voices[1]['name'], 'Mylene')

    @override_settings(
        ELEVENLABS_API_KEY='test-key',
        ELEVENLABS_VOICE_ID='voice-default',
        ELEVENLABS_MODEL_ID='eleven_multilingual_v2',
        ELEVENLABS_OUTPUT_FORMAT='mp3_44100_128',
    )
    def test_elevenlabs_generation_uses_advanced_settings(self):
        class FakeResponse:
            status_code = 200
            reason = 'OK'
            content = b'audio-bytes'

        with patch('reel_studio.elevenlabs.requests.post', return_value=FakeResponse()) as mocked_post:
            result = generate_speech_mp3(
                text='Bonjour',
                voice_id='voice-1',
                model_id='eleven_multilingual_v3',
                stability=0.64,
                similarity_boost=0.84,
                style=0.10,
                speed=1,
                use_speaker_boost=True,
                language_code='fr',
                apply_text_normalization='on',
            )

        payload = mocked_post.call_args.kwargs['json']
        self.assertEqual(payload['model_id'], 'eleven_v3')
        self.assertEqual(payload['language_code'], 'fr')
        self.assertEqual(payload['apply_text_normalization'], 'on')
        self.assertEqual(payload['voice_settings']['stability'], 0.64)
        self.assertEqual(payload['voice_settings']['similarity_boost'], 0.84)
        self.assertEqual(payload['voice_settings']['style'], 0.10)
        self.assertEqual(payload['voice_settings']['speed'], 1)
        self.assertIs(payload['voice_settings']['use_speaker_boost'], True)
        self.assertEqual(result['model_id'], 'eleven_v3')
