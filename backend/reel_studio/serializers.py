from rest_framework import serializers

from .models import ReelProject, ReelSlide


class ReelSlideSerializer(serializers.ModelSerializer):
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
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class ReelProjectSerializer(serializers.ModelSerializer):
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
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


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
