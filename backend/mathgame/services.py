"""
Core game-engine services for the Arena.

Centralizes scoring, streak logic, XP attribution and CTA decisions so
that views stay thin and business logic stays testable.
"""
from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from django.db import transaction
from django.utils import timezone

from .models import (
    ArenaAnswer,
    ArenaAttempt,
    ArenaConfig,
    ArenaLevel,
    ArenaMistake,
    ArenaQuestion,
    ArenaUserState,
)
from .permissions import is_premium


# --------------------------------------------------------------------------- #
# Answer grading
# --------------------------------------------------------------------------- #

def _is_mcq_correct(question: ArenaQuestion, user_answer: Any) -> bool:
    expected = question.correct or []
    if not isinstance(expected, list):
        return False
    if isinstance(user_answer, dict):
        user_answer = user_answer.get('value')
    if isinstance(user_answer, (int, str)):
        user_answer = [user_answer]
    if not isinstance(user_answer, list):
        return False
    try:
        return sorted(int(x) for x in user_answer) == sorted(int(x) for x in expected)
    except (TypeError, ValueError):
        return False


def _is_numeric_correct(question: ArenaQuestion, user_answer: Any) -> bool:
    expected = question.correct or {}
    if not isinstance(expected, dict):
        return False
    target = expected.get('value')
    tol = float(expected.get('tolerance', 0) or 0)
    if isinstance(user_answer, dict):
        user_answer = user_answer.get('value')
    try:
        target_f = float(target)
        user_f = float(user_answer)
    except (TypeError, ValueError):
        return False
    return abs(user_f - target_f) <= tol


def grade_question(question: ArenaQuestion, user_answer: Any) -> bool:
    if question.type == 'numeric':
        return _is_numeric_correct(question, user_answer)
    return _is_mcq_correct(question, user_answer)


# --------------------------------------------------------------------------- #
# Streaks
# --------------------------------------------------------------------------- #

def update_streak(state: ArenaUserState, played_on: date) -> None:
    """Update streak based on the day the user just completed a level."""
    last = state.last_played_date
    if last == played_on:
        return  # Already counted today.
    if last is None or last == played_on - timedelta(days=1):
        state.current_streak = (state.current_streak or 0) + 1
    else:
        state.current_streak = 1
    state.best_streak = max(state.best_streak or 0, state.current_streak)
    state.last_played_date = played_on


# --------------------------------------------------------------------------- #
# Attempt submission
# --------------------------------------------------------------------------- #

@transaction.atomic
def submit_attempt(*, user, level: ArenaLevel, answers: list[dict],
                   duration_sec: int, used_hint: bool, is_daily: bool) -> dict:
    """
    Persist an attempt, grade it, update streak / XP / mistakes.

    Returns a dict with the attempt summary AND the CTAs the frontend
    should display (so persuasion logic stays server-side).
    """
    config = ArenaConfig.get_solo()
    questions = list(level.questions.all().order_by('order'))
    questions_by_id = {q.id: q for q in questions}

    attempt = ArenaAttempt.objects.create(
        user=user,
        level=level,
        max_score=sum(q.weight for q in questions) or len(questions),
        is_daily=is_daily,
        used_hint=used_hint,
        duration_sec=max(0, int(duration_sec or 0)),
    )

    score = 0
    correct_count = 0
    for entry in answers or []:
        try:
            qid = int(entry.get('question_id'))
        except (TypeError, ValueError):
            continue
        q = questions_by_id.get(qid)
        if not q:
            continue
        is_correct = grade_question(q, entry.get('answer'))
        ArenaAnswer.objects.create(
            attempt=attempt,
            question=q,
            user_answer=entry.get('answer') or {},
            is_correct=is_correct,
            time_ms=max(0, int(entry.get('time_ms') or 0)),
        )
        if is_correct:
            score += q.weight
            correct_count += 1
            mistake = ArenaMistake.objects.filter(user=user, question=q).first()
            if mistake:
                mistake.mastery = min(3, (mistake.mastery or 0) + 1)
                mistake.last_seen = timezone.now()
                mistake.save(update_fields=['mastery', 'last_seen'])
        else:
            mistake, _ = ArenaMistake.objects.get_or_create(user=user, question=q)
            mistake.times_wrong = (mistake.times_wrong or 0) + 1
            mistake.last_seen = timezone.now()
            mistake.mastery = max(0, (mistake.mastery or 0) - 1)
            mistake.save(update_fields=['times_wrong', 'last_seen', 'mastery'])

    attempt.score = score
    attempt.accuracy = (correct_count / len(questions)) if questions else 0.0
    attempt.passed = (attempt.accuracy * 100) >= level.pass_threshold

    # XP — scaled by accuracy, halved if hint was used (free + premium).
    base_xp = level.xp_reward if attempt.passed else int(level.xp_reward * 0.3)
    if used_hint:
        base_xp = int(base_xp * 0.7)
    if is_daily and attempt.passed:
        base_xp += config.daily_xp_bonus
    attempt.xp_awarded = max(0, base_xp)
    attempt.save()

    # Streak / state.
    state, _ = ArenaUserState.objects.get_or_create(user=user)
    state.total_levels_completed = (state.total_levels_completed or 0) + (1 if attempt.passed else 0)
    state.total_xp_earned = (state.total_xp_earned or 0) + attempt.xp_awarded
    if attempt.passed:
        update_streak(state, timezone.localdate())
    if is_daily and attempt.passed:
        state.last_daily_completed_date = timezone.localdate()
    state.save()

    # Apply XP to the user model (existing OptiTAB XP system).
    if attempt.xp_awarded and hasattr(user, 'xp'):
        user.xp = (user.xp or 0) + attempt.xp_awarded
        user.save(update_fields=['xp'])

    # Build CTA payload for the frontend.
    ctas = build_post_attempt_ctas(user=user, attempt=attempt, level=level)

    return {
        'attempt_id': attempt.id,
        'score': attempt.score,
        'max_score': attempt.max_score,
        'accuracy': round(attempt.accuracy, 3),
        'passed': attempt.passed,
        'xp_awarded': attempt.xp_awarded,
        'streak': state.current_streak,
        'best_streak': state.best_streak,
        'ctas': ctas,
    }


# --------------------------------------------------------------------------- #
# CTA decision logic
# --------------------------------------------------------------------------- #

def build_post_attempt_ctas(*, user, attempt: ArenaAttempt, level: ArenaLevel) -> list[dict]:
    """
    Decide which subscription CTAs to show after an attempt.

    All copy is intentionally encouraging, not aggressive.
    """
    if is_premium(user):
        return []

    ctas: list[dict] = []

    if not attempt.passed:
        ctas.append({
            'id': 'unlock_solution',
            'title': 'Bloqué·e ? La solution détaillée vous attend',
            'body': "Avec OptiTAB+, accédez à l'explication étape par étape de chaque question.",
            'cta': "Voir l'offre",
            'route': '/tarifs',
            'trigger': 'level_failed',
        })

    if level.is_premium:
        ctas.append({
            'id': 'unlock_advanced',
            'title': 'Vous avez de l’avance — passez en niveau Élite',
            'body': "Les niveaux Élite et l’entraînement illimité sont inclus dans OptiTAB+.",
            'cta': "Découvrir OptiTAB+",
            'route': '/tarifs',
            'trigger': 'elite_locked_view',
        })

    if attempt.is_daily and attempt.passed:
        ctas.append({
            'id': 'streak_shield',
            'title': 'Protégez votre série',
            'body': "Avec OptiTAB+, un bouclier hebdomadaire évite la perte de votre série en cas d’oubli.",
            'cta': "Activer le bouclier",
            'route': '/tarifs',
            'trigger': 'daily_completed',
        })

    return ctas


# --------------------------------------------------------------------------- #
# Daily challenge access
# --------------------------------------------------------------------------- #

def can_play_daily(user, daily_date: date) -> tuple[bool, str | None]:
    """Free users can play the daily once per day; premium replays unlimited."""
    if is_premium(user):
        return True, None
    state = ArenaUserState.objects.filter(user=user).first()
    if state and state.last_daily_completed_date == daily_date:
        return False, 'daily_limit_reached'
    return True, None
