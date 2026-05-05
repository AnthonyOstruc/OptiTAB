"""
Arena (Math Game) models.

Designed to maximize engagement, retention and subscription conversion:
- Free vs premium content via `is_premium` flags + central permission helpers.
- Streak / XP / mistakes / daily challenge / leaderboard primitives.
- Visibility flag on ArenaConfig keeps the game admin-only until launch.
"""
from django.conf import settings
from django.db import models
from django.utils import timezone


class ArenaConfig(models.Model):
    """Singleton configuration row for the Arena game."""
    is_public = models.BooleanField(
        default=False,
        verbose_name="Visible publiquement",
        help_text="Tant que la valeur est False, seuls les administrateurs peuvent accéder au jeu.",
    )
    daily_xp_bonus = models.PositiveIntegerField(default=50)
    streak_shield_enabled = models.BooleanField(default=True)
    free_levels_per_chapter = models.PositiveIntegerField(default=2)
    free_hints_per_day = models.PositiveIntegerField(default=1)
    version = models.CharField(max_length=20, default='1.0.0')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuration Arena"
        verbose_name_plural = "Configuration Arena"

    def save(self, *args, **kwargs):
        # Enforce singleton (pk=1).
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"ArenaConfig(public={self.is_public}, v{self.version})"


class ArenaChapter(models.Model):
    """A themed chapter (e.g. 'Fonctions affines', 'Probabilités')."""
    notion = models.ForeignKey(
        'curriculum.Notion',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='arena_chapters',
        help_text="Notion pédagogique liée (optionnel mais recommandé pour la cohérence).",
    )
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    description = models.TextField(blank=True, default='')
    icon = models.CharField(max_length=10, blank=True, default='', help_text="Emoji ou code icône.")
    color = models.CharField(max_length=7, default='#2563eb')
    order = models.PositiveIntegerField(default=0)
    is_premium = models.BooleanField(default=False, help_text="Réserve tout le chapitre aux abonnés.")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']
        verbose_name = "Chapitre Arena"
        verbose_name_plural = "Chapitres Arena"

    def __str__(self):
        return self.title


class ArenaLevel(models.Model):
    """One playable level (5 questions by default) inside a chapter."""
    DIFFICULTY_CHOICES = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'),
        ('hard', 'Difficile'),
        ('elite', 'Élite (premium)'),
    ]

    chapter = models.ForeignKey(ArenaChapter, on_delete=models.CASCADE, related_name='levels')
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    time_limit_sec = models.PositiveIntegerField(default=120)
    xp_reward = models.PositiveIntegerField(default=20)
    pass_threshold = models.PositiveIntegerField(default=60, help_text="Pourcentage minimal pour réussir.")
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['chapter', 'order']
        unique_together = ('chapter', 'order')
        verbose_name = "Niveau Arena"
        verbose_name_plural = "Niveaux Arena"

    def __str__(self):
        return f"{self.chapter.title} · N{self.order} · {self.title}"


class ArenaQuestion(models.Model):
    """A single question. LaTeX content allowed (rendered with KaTeX on the frontend)."""
    TYPE_CHOICES = [
        ('mcq', 'Choix multiple'),
        ('numeric', 'Réponse numérique'),
    ]

    level = models.ForeignKey(ArenaLevel, on_delete=models.CASCADE, related_name='questions')
    order = models.PositiveIntegerField(default=0)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='mcq')
    prompt = models.TextField(help_text="Énoncé. LaTeX accepté entre $...$.")
    choices = models.JSONField(
        default=list,
        blank=True,
        help_text="Liste de propositions pour MCQ. Vide pour numeric.",
    )
    correct = models.JSONField(
        default=list,
        help_text="Pour MCQ: indices corrects, ex [0]. Pour numeric: ex {'value': 1.5, 'tolerance': 0.01}.",
    )
    hint = models.TextField(blank=True, default='', help_text="Indice (premium uniquement).")
    explanation = models.TextField(
        blank=True,
        default='',
        help_text="Solution détaillée. Tronquée pour les utilisateurs non premium.",
    )
    weight = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['level', 'order']
        unique_together = ('level', 'order')
        verbose_name = "Question Arena"
        verbose_name_plural = "Questions Arena"

    def __str__(self):
        return f"{self.level} · Q{self.order}"


class ArenaDailyChallenge(models.Model):
    """Pinned daily challenge level for a given date."""
    date = models.DateField(unique=True)
    level = models.ForeignKey(ArenaLevel, on_delete=models.CASCADE, related_name='daily_uses')
    bonus_xp = models.PositiveIntegerField(default=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']
        verbose_name = "Défi quotidien"
        verbose_name_plural = "Défis quotidiens"

    def __str__(self):
        return f"Daily {self.date} · {self.level}"


class ArenaUserState(models.Model):
    """Per-user game state."""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='arena_state',
    )
    current_streak = models.PositiveIntegerField(default=0)
    best_streak = models.PositiveIntegerField(default=0)
    last_played_date = models.DateField(null=True, blank=True)
    streak_shields_used = models.PositiveIntegerField(default=0)
    daily_hints_used = models.PositiveIntegerField(default=0)
    daily_hints_reset_date = models.DateField(null=True, blank=True)
    total_levels_completed = models.PositiveIntegerField(default=0)
    total_xp_earned = models.PositiveIntegerField(default=0)
    last_daily_completed_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "État joueur Arena"
        verbose_name_plural = "États joueurs Arena"

    def __str__(self):
        return f"State<{self.user_id}>"


class ArenaAttempt(models.Model):
    """A single play-through of a level."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='arena_attempts',
    )
    level = models.ForeignKey(ArenaLevel, on_delete=models.CASCADE, related_name='attempts')
    score = models.PositiveIntegerField(default=0)
    max_score = models.PositiveIntegerField(default=0)
    accuracy = models.FloatField(default=0.0)
    duration_sec = models.PositiveIntegerField(default=0)
    used_hint = models.BooleanField(default=False)
    is_daily = models.BooleanField(default=False)
    passed = models.BooleanField(default=False)
    xp_awarded = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['level', '-score']),
        ]
        verbose_name = "Tentative Arena"
        verbose_name_plural = "Tentatives Arena"

    def __str__(self):
        return f"Attempt<{self.user_id}, {self.level_id}, {self.score}/{self.max_score}>"


class ArenaAnswer(models.Model):
    """A single answered question inside an attempt."""
    attempt = models.ForeignKey(ArenaAttempt, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(ArenaQuestion, on_delete=models.CASCADE, related_name='answers')
    user_answer = models.JSONField(default=dict, blank=True)
    is_correct = models.BooleanField(default=False)
    time_ms = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "Réponse Arena"
        verbose_name_plural = "Réponses Arena"


class ArenaMistake(models.Model):
    """Mistakes tracked for the personal Mistake Forge feature."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='arena_mistakes',
    )
    question = models.ForeignKey(ArenaQuestion, on_delete=models.CASCADE, related_name='mistakes')
    last_seen = models.DateTimeField(default=timezone.now)
    times_wrong = models.PositiveIntegerField(default=1)
    mastery = models.PositiveSmallIntegerField(default=0, help_text="0..3, 3 = maîtrisé")

    class Meta:
        unique_together = ('user', 'question')
        ordering = ['-last_seen']
        verbose_name = "Erreur (Forge)"
        verbose_name_plural = "Erreurs (Forge)"


class ArenaEvent(models.Model):
    """Lightweight analytics event store (admin / dashboards)."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='arena_events',
    )
    name = models.CharField(max_length=80, db_index=True)
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Événement Arena"
        verbose_name_plural = "Événements Arena"
