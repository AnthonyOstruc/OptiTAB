from django.db import models


class ReelProject(models.Model):
    STATUS_DRAFT = 'draft'
    STATUS_READY = 'ready'
    STATUS_ARCHIVED = 'archived'

    STATUS_CHOICES = [
        (STATUS_DRAFT, 'Draft'),
        (STATUS_READY, 'Ready'),
        (STATUS_ARCHIVED, 'Archived'),
    ]

    title = models.CharField(max_length=255)
    theme = models.CharField(max_length=255, blank=True, default='')
    level = models.CharField(max_length=64, blank=True, default='')
    format_type = models.CharField(max_length=64, blank=True, default='')
    target_duration_seconds = models.PositiveIntegerField(default=30)
    slide_count = models.PositiveIntegerField(default=6)
    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=STATUS_DRAFT)
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

    TYPE_CHOICES = [
        (TYPE_HOOK, 'Hook'),
        (TYPE_KATEX, 'KaTeX'),
        (TYPE_CUMULATIVE_KATEX, 'Cumulative KaTeX'),
        (TYPE_RESULT, 'Result'),
        (TYPE_CTA, 'CTA'),
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
    katex_reset_cumulative = models.BooleanField(default=False)
    duration_seconds = models.PositiveIntegerField(default=4)
    layout_status = models.CharField(max_length=32, choices=LAYOUT_STATUS_CHOICES, default=LAYOUT_UNCHECKED)
    layout_notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'id']
        unique_together = ('reel_project', 'order')

    def __str__(self):
        return f'{self.reel_project_id} - Slide {self.order}'
