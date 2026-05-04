from rest_framework import serializers

from .models import ReelProject, ReelSlide


class ReelSlideSerializer(serializers.ModelSerializer):
    speech_audio_url = serializers.SerializerMethodField()

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

    def validate_title_scale(self, value):
        return self._validate_scale(value)

    def validate_screen_text_scale(self, value):
        return self._validate_scale(value)

    def validate_katex_scale(self, value):
        return self._validate_scale(value)

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
            'katex_reset_cumulative',
            'duration_seconds',
            'layout_status',
            'layout_notes',
            'speech_audio',
            'speech_audio_url',
            'speech_voice_id',
            'speech_model_id',
            'speech_output_format',
            'speech_status',
            'speech_error',
            'speech_generated_at',
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
            'created_at',
            'updated_at',
        ]


class ReelProjectSerializer(serializers.ModelSerializer):
    speech_audio_url = serializers.SerializerMethodField()
    video_file_url = serializers.SerializerMethodField()

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
    template_text = serializers.CharField(max_length=12000)
    max_chars_per_line = serializers.IntegerField(min_value=12, max_value=120, default=38, required=False)
    include_hook = serializers.BooleanField(default=None, required=False, allow_null=True)
    include_cta = serializers.BooleanField(default=None, required=False, allow_null=True)
    hook_text = serializers.CharField(max_length=255, allow_blank=True, required=False, default='')
    cta_text = serializers.CharField(max_length=255, allow_blank=True, required=False, default='')


class ReelSpeechGenerateSerializer(serializers.Serializer):
    text = serializers.CharField(max_length=12000, allow_blank=True, required=False, default='')
    voice_id = serializers.CharField(max_length=128, allow_blank=True, required=False, default='')
    model_id = serializers.CharField(max_length=128, allow_blank=True, required=False, default='')
    output_format = serializers.CharField(max_length=64, allow_blank=True, required=False, default='')


class ReelVideoFrameSerializer(serializers.Serializer):
    slide_id = serializers.IntegerField(min_value=1)
    image = serializers.CharField()
    duration_seconds = serializers.FloatField(min_value=1, max_value=30, required=False, default=4)


class ReelVideoExportSerializer(serializers.Serializer):
    frames = ReelVideoFrameSerializer(many=True, allow_empty=False)
    width = serializers.IntegerField(min_value=720, max_value=2160, required=False, default=1080)
    height = serializers.IntegerField(min_value=1280, max_value=3840, required=False, default=1920)
    fps = serializers.IntegerField(min_value=24, max_value=60, required=False, default=30)
    crf = serializers.IntegerField(min_value=16, max_value=28, required=False, default=18)
