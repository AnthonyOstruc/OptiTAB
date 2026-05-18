from rest_framework import serializers

from .models import ReelProject, ReelSlide


class ReelSlideSerializer(serializers.ModelSerializer):
    speech_audio_url = serializers.SerializerMethodField()
    generated_image_url = serializers.SerializerMethodField()

    def get_speech_audio_url(self, obj):
        return self._file_url(obj.speech_audio)

    def get_generated_image_url(self, obj):
        return self._file_url(obj.generated_image)

    def _file_url(self, file_field):
        if not file_field:
            return None
        try:
            url = file_field.url
        except ValueError:
            return None

        request = self.context.get('request') if hasattr(self, 'context') else None
        if request and url and not str(url).startswith(('http://', 'https://')):
            return request.build_absolute_uri(url)
        return url

    def validate_title_scale(self, value):
        return self._validate_scale(value)

    def validate_screen_text_scale(self, value):
        return self._validate_scale(value)

    def validate_katex_scale(self, value):
        return self._validate_scale(value)

    def validate_katex_inline_offset_percent(self, value):
        if value < -40 or value > 40:
            raise serializers.ValidationError('Le decalage doit etre compris entre -40% et 40%.')
        return value

    def validate_katex_inline_vertical_offset_em(self, value):
        if value < -1 or value > 1:
            raise serializers.ValidationError('Le decalage vertical doit etre compris entre -1em et 1em.')
        return value

    def validate_katex_inline_separator(self, value):
        safe_value = str(value or '').strip()
        allowed = {
            ReelSlide.INLINE_SEPARATOR_SEMICOLON,
            ReelSlide.INLINE_SEPARATOR_ARROW,
            ReelSlide.INLINE_SEPARATOR_NONE,
        }
        if safe_value not in allowed:
            raise serializers.ValidationError('Separateur de ligne invalide.')
        return safe_value

    def validate_katex_cumulative_gap_em(self, value):
        if value < 0 or value > 1.5:
            raise serializers.ValidationError('Le vide entre lignes doit etre compris entre 0 et 1.5em.')
        return value

    @staticmethod
    def _validate_scale(value):
        if value < 0.5 or value > 2:
            raise serializers.ValidationError('La taille doit être comprise entre 50% et 200%.')
        return value

    class Meta:
        model = ReelSlide
        fields = [
            'id',
            'reel_project',
            'order',
            'slide_type',
            'title',
            'screen_text',
            'katex',
            'voice_script',
            'title_scale',
            'screen_text_scale',
            'katex_scale',
            'katex_inline_with_previous',
            'katex_inline_separator',
            'katex_inline_offset_percent',
            'katex_inline_vertical_offset_em',
            'katex_cumulative_gap_em',
            'katex_reset_cumulative',
            'katex_reset_keep_previous_line',
            'katex_reveal_with_speech',
            'katex_drop_previous_line',
            'duration_seconds',
            'layout_status',
            'layout_notes',
            'annotations',
            'generated_image',
            'generated_image_url',
            'generated_image_prompt',
            'generated_image_model_id',
            'generated_image_generated_at',
            'speech_text',
            'speech_audio',
            'speech_audio_url',
            'speech_voice_id',
            'speech_model_id',
            'speech_output_format',
            'speech_status',
            'speech_error',
            'speech_generated_at',
            'speech_word_timings',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'generated_image',
            'generated_image_url',
            'generated_image_prompt',
            'generated_image_model_id',
            'generated_image_generated_at',
            'speech_text',
            'speech_audio',
            'speech_audio_url',
            'speech_voice_id',
            'speech_model_id',
            'speech_output_format',
            'speech_status',
            'speech_error',
            'speech_generated_at',
            'speech_word_timings',
            'created_at',
            'updated_at',
        ]


class ReelProjectSerializer(serializers.ModelSerializer):
    speech_audio_url = serializers.SerializerMethodField()
    video_file_url = serializers.SerializerMethodField()

    def validate_title(self, value):
        safe_title = str(value or '').strip()
        if not safe_title:
            raise serializers.ValidationError('Le titre du reel est obligatoire.')
        return safe_title

    def _clean_pronunciation_list(self, items):
        allowed_languages = {'fr', 'en', 'es', 'de', 'it', 'pt'}
        cleaned = []
        seen_words = set()
        for item in items:
            if not isinstance(item, dict):
                raise serializers.ValidationError('Chaque entree de prononciation doit etre un objet.')
            word = str(item.get('word') or '').strip()
            pronunciation = str(item.get('pronunciation') or '').strip()
            if not word or not pronunciation:
                continue
            if len(word) > 80 or len(pronunciation) > 160:
                raise serializers.ValidationError('Mot ou prononciation trop long.')
            language = str(item.get('language') or 'fr').strip().lower()
            if language not in allowed_languages:
                language = 'fr'
            key = word.lower()
            if key in seen_words:
                continue
            seen_words.add(key)
            cleaned.append({'word': word, 'pronunciation': pronunciation, 'language': language})
        return cleaned

    def validate_pronunciation_overrides(self, value):
        if value in (None, ''):
            return []
        if not isinstance(value, list):
            raise serializers.ValidationError('Les surcharges de prononciation doivent etre une liste.')
        return self._clean_pronunciation_list(value)

    def validate_pronunciation_overrides_by_voice(self, value):
        if value in (None, '', {}):
            return {}
        if not isinstance(value, dict):
            raise serializers.ValidationError('Les surcharges par voix doivent etre un objet.')
        cleaned = {}
        for voice_id, overrides in value.items():
            voice_key = str(voice_id or '').strip()
            if not voice_key or len(voice_key) > 128:
                continue
            if not isinstance(overrides, list):
                continue
            voice_cleaned = self._clean_pronunciation_list(overrides)
            if voice_cleaned:
                cleaned[voice_key] = voice_cleaned
        return cleaned

    def get_speech_audio_url(self, obj):
        if not obj.speech_audio:
            return None
        try:
            url = obj.speech_audio.url
        except ValueError:
            return None

        request = self.context.get('request') if hasattr(self, 'context') else None
        if request and url and not str(url).startswith(('http://', 'https://')):
            return request.build_absolute_uri(url)
        return url

    def get_video_file_url(self, obj):
        if not obj.video_file:
            return None
        try:
            url = obj.video_file.url
        except ValueError:
            return None

        request = self.context.get('request') if hasattr(self, 'context') else None
        if request and url and not str(url).startswith(('http://', 'https://')):
            return request.build_absolute_uri(url)
        return url

    class Meta:
        model = ReelProject
        fields = [
            'id',
            'title',
            'theme',
            'level',
            'format_type',
            'instagram_caption',
            'target_duration_seconds',
            'slide_count',
            'status',
            'speech_audio',
            'speech_audio_url',
            'speech_voice_id',
            'speech_model_id',
            'speech_output_format',
            'speech_status',
            'speech_error',
            'speech_generated_at',
            'video_file',
            'video_file_url',
            'video_status',
            'video_error',
            'video_generated_at',
            'video_width',
            'video_height',
            'video_fps',
            'pronunciation_overrides',
            'pronunciation_overrides_by_voice',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'speech_audio',
            'speech_audio_url',
            'speech_voice_id',
            'speech_model_id',
            'speech_output_format',
            'speech_status',
            'speech_error',
            'speech_generated_at',
            'video_file',
            'video_file_url',
            'video_status',
            'video_error',
            'video_generated_at',
            'video_width',
            'video_height',
            'video_fps',
            'created_at',
            'updated_at',
        ]


class ReelProjectDetailSerializer(ReelProjectSerializer):
    slides = ReelSlideSerializer(many=True, read_only=True)

    class Meta(ReelProjectSerializer.Meta):
        fields = ReelProjectSerializer.Meta.fields + ['slides']


class ReelTemplateGenerateSerializer(serializers.Serializer):
    template_text = serializers.CharField()
    max_chars_per_line = serializers.IntegerField(min_value=12, max_value=120, default=38, required=False)
    include_hook = serializers.BooleanField(default=None, required=False, allow_null=True)
    include_cta = serializers.BooleanField(default=None, required=False, allow_null=True)
    hook_text = serializers.CharField(max_length=255, allow_blank=True, required=False, default='')
    cta_text = serializers.CharField(max_length=255, allow_blank=True, required=False, default='')


class ReelGeminiCarouselGenerateSerializer(serializers.Serializer):
    prompt = serializers.CharField(max_length=30000)
    model_id = serializers.CharField(max_length=128, allow_blank=True, required=False, default='')
    max_chars_per_line = serializers.IntegerField(min_value=12, max_value=120, default=38, required=False)
    generate_images = serializers.BooleanField(required=False, default=True)
    slide_image_strategy = serializers.ChoiceField(
        choices=['hook_cta', 'hook', 'cta', 'all', 'none', 'custom'],
        required=False,
        default='hook_cta',
    )
    slide_image_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1),
        required=False,
        default=list,
    )
    carousel_type = serializers.ChoiceField(
        choices=['marketing', 'quiz', 'tips', 'avantapres', 'story', 'notion'],
        required=False,
        default='marketing',
    )
    use_site_references = serializers.BooleanField(required=False, default=True)


class ReelSpeechGenerateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=12000, allow_blank=True, required=False, default='')
    voice_id = serializers.CharField(max_length=128, allow_blank=True, required=False, default='')
    model_id = serializers.CharField(max_length=128, allow_blank=True, required=False, default='')
    output_format = serializers.CharField(max_length=64, allow_blank=True, required=False, default='')
    provider = serializers.CharField(max_length=32, allow_blank=True, required=False, default='')
    stability = serializers.FloatField(min_value=0, max_value=1, required=False, allow_null=True)
    similarity_boost = serializers.FloatField(min_value=0, max_value=1, required=False, allow_null=True)
    style = serializers.FloatField(min_value=0, max_value=1, required=False, allow_null=True)
    speed = serializers.FloatField(min_value=0.5, max_value=2, required=False, allow_null=True)
    use_speaker_boost = serializers.BooleanField(required=False, allow_null=True)
    language_code = serializers.CharField(max_length=16, allow_blank=True, required=False, default='')
    apply_text_normalization = serializers.ChoiceField(
        choices=['auto', 'on', 'off'],
        allow_blank=True,
        required=False,
        default='',
    )
    google_speaking_rate = serializers.FloatField(min_value=0.25, max_value=4, required=False, allow_null=True)
    google_pitch = serializers.FloatField(min_value=-20, max_value=20, required=False, allow_null=True)
    google_volume_gain_db = serializers.FloatField(min_value=-96, max_value=16, required=False, allow_null=True)
    google_effects_profile_id = serializers.CharField(max_length=96, allow_blank=True, required=False, default='')


class ReelTTSTestSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=600, allow_blank=False)
    provider = serializers.CharField(max_length=32, allow_blank=True, required=False, default='')
    voice_id = serializers.CharField(max_length=128, allow_blank=True, required=False, default='')
    model_id = serializers.CharField(max_length=128, allow_blank=True, required=False, default='')
    stability = serializers.FloatField(min_value=0, max_value=1, required=False, allow_null=True)
    similarity_boost = serializers.FloatField(min_value=0, max_value=1, required=False, allow_null=True)
    style = serializers.FloatField(min_value=0, max_value=1, required=False, allow_null=True)
    speed = serializers.FloatField(min_value=0.5, max_value=2, required=False, allow_null=True)
    use_speaker_boost = serializers.BooleanField(required=False, allow_null=True)
    language_code = serializers.CharField(max_length=16, allow_blank=True, required=False, default='')
    apply_text_normalization = serializers.ChoiceField(
        choices=['auto', 'on', 'off'],
        allow_blank=True,
        required=False,
        default='',
    )
    google_speaking_rate = serializers.FloatField(min_value=0.25, max_value=4, required=False, allow_null=True)
    google_pitch = serializers.FloatField(min_value=-20, max_value=20, required=False, allow_null=True)
    google_volume_gain_db = serializers.FloatField(min_value=-96, max_value=16, required=False, allow_null=True)
    google_effects_profile_id = serializers.CharField(max_length=96, allow_blank=True, required=False, default='')


class ReelVideoFrameSerializer(serializers.Serializer):
    slide_id = serializers.IntegerField(min_value=1)
    image = serializers.CharField()
    duration_seconds = serializers.FloatField(min_value=1, max_value=30, required=False, default=4)


class ReelVideoExportSerializer(serializers.Serializer):
    PRESET_CHOICES = [
        'ultrafast',
        'superfast',
        'veryfast',
        'faster',
        'fast',
        'medium',
        'slow',
    ]

    frames = ReelVideoFrameSerializer(many=True, allow_empty=False)
    width = serializers.IntegerField(min_value=720, max_value=3840, required=False, default=1080)
    height = serializers.IntegerField(min_value=720, max_value=3840, required=False, default=1920)
    fps = serializers.IntegerField(min_value=24, max_value=60, required=False, default=30)
    crf = serializers.IntegerField(min_value=16, max_value=28, required=False, default=18)
    preset = serializers.ChoiceField(choices=PRESET_CHOICES, required=False, default='veryfast')
    show_subtitles = serializers.BooleanField(required=False, default=False)
    subtitle_offset_percent = serializers.FloatField(min_value=0, max_value=50, required=False, allow_null=True, default=None)
