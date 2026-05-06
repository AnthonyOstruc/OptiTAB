from django.db import models
from django.utils import timezone


CATEGORY_CHOICES = [
    ('all',            'Mixte'),
    ('addition',       'Addition'),
    ('subtraction',    'Soustraction'),
    ('multiplication', 'Multiplication'),
    ('division',       'Division'),
    ('limits',         'Limites'),
    ('derivatives',    'Dérivées'),
    ('integrals',      'Intégrales'),
    ('sequences',      'Suites'),
]


class MathRunScore(models.Model):
    user = models.ForeignKey(
        'users.CustomUser',
        on_delete=models.CASCADE,
        related_name='math_run_scores',
    )
    score = models.PositiveIntegerField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='all')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-score', '-created_at']
        indexes = [
            models.Index(fields=['user', 'category'], name='mr_score_user_cat_idx'),
            models.Index(fields=['-score'], name='mr_score_score_idx'),
        ]

    def __str__(self):
        return f'{self.user} — {self.category} — {self.score}'
