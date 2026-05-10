import shutil
import tempfile
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from .elevenlabs import generate_speech_mp3, list_filtered_voices, list_shared_voices
from .models import ReelProject, ReelSlide
from .tts.base import TTSResult
from .tts.google import synthesize as synthesize_google_speech


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

        with patch('reel_studio.views.tts_generate_speech', side_effect=self.fake_tts_result) as mocked_tts:
            response = self.client.post(
                reverse('reel-project-generate-slide-speeches', args=[project.pk]),
                {
                    'provider': 'google',
                    'voice_id': 'fr-FR-Standard-F',
                    'google_speaking_rate': 1.1,
                    'google_pitch': -1.5,
                    'google_volume_gain_db': 2,
                    'google_effects_profile_id': 'headphone-class-device',
                },
                format='json',
            )

        self.assertEqual(response.status_code, 201)
        first_call_kwargs = mocked_tts.call_args_list[0].kwargs
        self.assertEqual(first_call_kwargs['google_speaking_rate'], 1.1)
        self.assertEqual(first_call_kwargs['google_pitch'], -1.5)
        self.assertEqual(first_call_kwargs['google_volume_gain_db'], 2)
        self.assertEqual(first_call_kwargs['google_effects_profile_id'], 'headphone-class-device')
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

    @override_settings(ELEVENLABS_API_KEY='test-key', ELEVENLABS_VOICE_ID='6FXyooAOTqUK8m2HWm32')
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
                            'preview_url': 'https://example.com/anna-preview.mp3',
                            'labels': {'language': 'fr', 'accent': 'parisian'},
                        },
                    ]
                }

        with patch('reel_studio.elevenlabs.requests.get', return_value=FakeResponse()):
            voices = list_filtered_voices(language='fr', accent='parisian', include_fallback=True)

        self.assertGreaterEqual(len(voices), 2)
        self.assertEqual(voices[0]['voice_id'], '6FXyooAOTqUK8m2HWm32')
        self.assertEqual(voices[0]['name'], 'Marine - Premium Conversational AI')
        self.assertEqual(voices[1]['voice_id'], 'aQROLel5sQbj1vuIVi6B')
        self.assertEqual(voices[1]['name'], 'Nicolas')
        anna_voice = next(voice for voice in voices if voice['voice_id'] == 'other-voice')
        self.assertEqual(anna_voice['preview_url'], 'https://example.com/anna-preview.mp3')

    @override_settings(ELEVENLABS_API_KEY='test-key')
    def test_shared_voice_library_filters_and_preview(self):
        class FakeResponse:
            status_code = 200
            reason = 'OK'

            @staticmethod
            def json():
                return {
                    'voices': [
                        {
                            'voice_id': 'library-voice',
                            'name': 'Nicolas - Narrator',
                            'category': 'professional',
                            'language': 'fr',
                            'accent': 'parisian',
                            'gender': 'male',
                            'age': 'middle_aged',
                            'description': 'French narrator',
                            'preview_url': 'https://example.com/library-preview.mp3',
                            'cloned_by_count': 42,
                        },
                    ],
                    'has_more': False,
                    'total_count': 1,
                }

        with patch('reel_studio.elevenlabs.requests.get', return_value=FakeResponse()) as mocked_get:
            payload = list_shared_voices(
                language='fr',
                accent='parisian',
                category='high_quality',
                gender='male',
                age='middle aged',
                search='Nicolas',
                featured=True,
                page_size=80,
            )

        request_kwargs = mocked_get.call_args.kwargs
        self.assertEqual(mocked_get.call_args.args[0], 'https://api.elevenlabs.io/v1/shared-voices')
        self.assertEqual(request_kwargs['params']['language'], 'fr')
        self.assertEqual(request_kwargs['params']['accent'], 'parisian')
        self.assertEqual(request_kwargs['params']['category'], 'high_quality')
        self.assertEqual(request_kwargs['params']['gender'], 'male')
        self.assertEqual(request_kwargs['params']['age'], 'middle_aged')
        self.assertEqual(request_kwargs['params']['search'], 'Nicolas')
        self.assertIs(request_kwargs['params']['featured'], True)
        self.assertEqual(request_kwargs['params']['page_size'], 80)
        self.assertEqual(payload['total_count'], 1)
        self.assertEqual(payload['voices'][0]['voice_id'], 'library-voice')
        self.assertEqual(payload['voices'][0]['preview_url'], 'https://example.com/library-preview.mp3')
        self.assertEqual(payload['voices'][0]['labels']['gender'], 'male')
        self.assertEqual(payload['filters']['age'], 'middle_aged')
        self.assertTrue(payload['filters']['featured'])

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

    def test_google_generation_uses_advanced_settings(self):
        class FakeResponse:
            status_code = 200
            reason = 'OK'

            @staticmethod
            def json():
                return {'audioContent': 'YXVkaW8='}

        with (
            patch('reel_studio.tts.google._get_access_token', return_value='token'),
            patch('reel_studio.tts.google.requests.post', return_value=FakeResponse()) as mocked_post,
        ):
            result = synthesize_google_speech(
                text='Bonjour',
                voice_id='fr-FR-Standard-F',
                speaking_rate=1.15,
                pitch=-1.5,
                volume_gain_db=2,
                effects_profile_id='headphone-class-device',
            )

        payload = mocked_post.call_args.kwargs['json']
        audio_config = payload['audioConfig']
        self.assertEqual(audio_config['audioEncoding'], 'MP3')
        self.assertEqual(audio_config['speakingRate'], 1.15)
        self.assertEqual(audio_config['pitch'], -1.5)
        self.assertEqual(audio_config['volumeGainDb'], 2)
        self.assertEqual(audio_config['effectsProfileId'], ['headphone-class-device'])
        self.assertEqual(result['audio_bytes'], b'audio')
