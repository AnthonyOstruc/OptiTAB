from django.db import models


def reel_project_speech_upload_to(instance, filename):
    project_id = instance.pk or 'new'
    return f'reel_studio/speech/project_{project_id}/{filename}'


def reel_project_video_upload_to(instance, filename):
    project_id = instance.pk or 'new'
    return f'reel_studio/video/project_{project_id}/{filename}'


def reel_slide_speech_upload_to(instance, filename):
    project_id = instance.reel_project_id or 'new'
    slide_id = instance.pk or 'new'
    return f'reel_studio/speech/project_{project_id}/slides/slide_{slide_id}/{filename}'


class ReelProject(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_READY = 'ready'
    STATUS_ARCHIVED = 'archived'

    SPEECH_STATUS_EMPTY = 'empty'
    SPEECH_STATUS_READY = 'ready'
    SPEECH_STATUS_ERROR = 'error'
    VIDEO_STATUS_EMPTY = 'empty'
    VIDEO_STATUS_READY = 'ready'
    VIDEO_STATUS_ERROR = 'error'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_READY, 'Ready'),
        (STATUS_ARCHIVED, 'Archived'),
    ]
    SPEECH_STATUS_CHOICES = [
        (SPEECH_STATUS_EMPTY, 'Empty'),
        (SPEECH_STATUS_READY, 'Ready'),
        (SPEECH_STATUS_ERROR, 'Error'),
    ]
    VIDEO_STATUS_CHOICES = [
        (VIDEO_STATUS_EMPTY, 'Empty'),
        (VIDEO_STATUS_READY, 'Ready'),
        (VIDEO_STATUS_ERROR, 'Error'),
    ]

    title = models.CharField(max_length=255)
    theme = models.CharField(max_length=255, blank=True, default='')
    level = models.CharField(max_length=64, blank=True, default='')
    format_type = models.CharField(max_length=64, blank=True, default='')
    instagram_caption = models.TextField(blank=True, default='')
    target_duration_seconds = models.PositiveIntegerField(default=30)
    slide_count = models.PositiveIntegerField(default=6)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_DRAFT)
    speech_audio = models.FileField(upload_to=reel_project_speech_upload_to, blank=True, null=True)
    speech_text = models.TextField(blank=True, default='')
    speech_voice_id = models.CharField(max_length=128, blank=True, default='')
    speech_model_id = models.CharField(max_length=128, blank=True, default='')
    speech_output_format = models.CharField(max_length=64, blank=True, default='')
    speech_status = models.CharField(
        max_length=32,
        choices=SPEECH_STATUS_CHOICES,
        default=SPEECH_STATUS_EMPTY,
    )
    speech_error = models.TextField(blank=True, default='')
    speech_generated_at = models.DateTimeField(blank=True, null=True)
    video_file = models.FileField(upload_to=reel_project_video_upload_to, blank=True, null=True)
    video_status = models.CharField(
        max_length=32,
        choices=VIDEO_STATUS_CHOICES,
        default=VIDEO_STATUS_EMPTY,
    )
    video_error = models.TextField(blank=True, default='')
    video_generated_at = models.DateTimeField(blank=True, null=True)
    video_width = models.PositiveIntegerField(default=1080)
    video_height = models.PositiveIntegerField(default=1920)
    video_fps = models.PositiveIntegerField(default=30)
    pronunciation_overrides = models.JSONField(blank=True, default=list)
    pronunciation_overrides_by_voice = models.JSONField(blank=True, null=True, default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return self.title


class ReelSlide(models.Model):
    TYPE_HOOK = 'hook'
    TYPE_KATEX = 'katex'
    TYPE_CUMULATIVE_KATEX = 'cumulative_katex'
    TYPE_RESULT = 'result'
    TYPE_CTA = 'cta'
    INLINE_SEPARATOR_SEMICOLON = 'semicolon'
    INLINE_SEPARATOR_ARROW = 'arrow'
    INLINE_SEPARATOR_NONE = 'none'

    TYPE_CHOICES = [
        (TYPE_HOOK, 'Hook'),
        (TYPE_KATEX, 'KaTeX'),
        (TYPE_CUMULATIVE_KATEX, 'Cumulative KaTeX'),
        (TYPE_RESULT, 'Result'),
        (TYPE_CTA, 'CTA'),
    ]
    INLINE_SEPARATOR_CHOICES = [
        (INLINE_SEPARATOR_SEMICOLON, 'Semicolon'),
        (INLINE_SEPARATOR_ARROW, 'Arrow'),
        (INLINE_SEPARATOR_NONE, 'None'),
    ]

    LAYOUT_UNCHECKED = 'unchecked'
    LAYOUT_OK = 'ok'
    LAYOUT_WARNING = 'warning'
    LAYOUT_ERROR = 'error'

    LAYOUT_STATUS_CHOICES = [
        (LAYOUT_UNCHECKED, 'Unchecked'),
        (LAYOUT_OK, 'OK'),
        (LAYOUT_WARNING, 'Warning'),
        (LAYOUT_ERROR, 'Error'),
    ]

    reel_project = models.ForeignKey(ReelProject, on_delete=models.CASCADE, related_name='slides')
    order = models.PositiveIntegerField(default=1)
    slide_type = models.CharField(max_length=32, choices=TYPE_CHOICES)
    title = models.CharField(max_length=255, blank=True, default='')
    screen_text = models.TextField(blank=True, default='')
    katex = models.TextField(blank=True, default='')
    voice_script = models.TextField(blank=True, default='')
    title_scale = models.FloatField(default=1.0)
    screen_text_scale = models.FloatField(default=1.0)
    katex_scale = models.FloatField(default=1.0)
    katex_inline_with_previous = models.BooleanField(default=False)
    katex_inline_separator = models.CharField(
        max_length=16,
        choices=INLINE_SEPARATOR_CHOICES,
        default=INLINE_SEPARATOR_SEMICOLON,
    )
    katex_inline_offset_percent = models.FloatField(default=0.0)
    katex_inline_vertical_offset_em = models.FloatField(default=0.0)
    katex_cumulative_gap_em = models.FloatField(default=0.4)
    katex_reset_cumulative = models.BooleanField(default=False)
    katex_reset_keep_previous_line = models.BooleanField(default=True)
    katex_reveal_with_speech = models.BooleanField(default=False)
    katex_drop_previous_line = models.BooleanField(default=False)
    duration_seconds = models.PositiveIntegerField(default=4)
    layout_status = models.CharField(max_length=32, choices=LAYOUT_STATUS_CHOICES, default=LAYOUT_UNCHECKED)
    layout_notes = models.TextField(blank=True, default='')
    speech_audio = models.FileField(upload_to=reel_slide_speech_upload_to, blank=True, null=True)
    speech_text = models.TextField(blank=True, default='')
    speech_voice_id = models.CharField(max_length=128, blank=True, default='')
    speech_model_id = models.CharField(max_length=128, blank=True, default='')
    speech_output_format = models.CharField(max_length=64, blank=True, default='')
    speech_status = models.CharField(
        max_length=32,
        choices=ReelProject.SPEECH_STATUS_CHOICES,
        default=ReelProject.SPEECH_STATUS_EMPTY,
    )
    speech_error = models.TextField(blank=True, default='')
    speech_generated_at = models.DateTimeField(blank=True, null=True)
    speech_word_timings = models.JSONField(blank=True, null=True, default=None)
    annotations = models.JSONField(blank=True, default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        unique_together = ('reel_project', 'order')

    def __str__(self):
        return f'{self.reel_project_id} - Slide {self.order}'
