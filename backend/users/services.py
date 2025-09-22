"""
User-related domain services.

StreakService computes and persists streak metrics based on user activity
recorded in `suivis.SuiviExercice` for the last N days.

Rules:
- A day counts if the user has at least one `SuiviExercice` that day
- Current streak counts consecutive days ending today only if today has activity
- Longest streak is computed over a 365-day sliding window

Usage:
    StreakService.refresh_user_streak(user)
    StreakService.get_user_streak_data(user)
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta
from django.db import transaction
from django.db.models import Count
from django.db.models.functions import TruncDate
from django.utils import timezone
from users.models import UserNotification


@dataclass(frozen=True)
class StreakData:
    current_streak: int
    longest_streak: int
    activity_map: dict[str, int]


class StreakService:
    @staticmethod
    def _calculate_streak_xp(streak_days: int) -> int:
        """XP rules: day 1..5 => 1..5 XP, then capped at 5 XP/day."""
        if streak_days <= 0:
            return 0
        if streak_days <= 5:
            return int(streak_days)
        return 5
    @staticmethod
    def _fetch_activity_map(user, days: int = 365) -> dict[str, int]:
        from suivis.models import SuiviExercice

        start = timezone.now() - timedelta(days=days)
        rows = (
            SuiviExercice.objects.filter(user=user, date_creation__gte=start)
            .annotate(day=TruncDate('date_creation'))
            .values('day')
            .annotate(total=Count('id'))
            .order_by()
        )
        return {str(r['day']): int(r['total'] or 0) for r in rows}

    @staticmethod
    def _compute_streaks(activity_map: dict[str, int]) -> tuple[int, int]:
        today = timezone.now().date()

        def has_activity(d):
            return (activity_map.get(str(d), 0) or 0) > 0

        # Current streak (must include today)
        current = 0
        for i in range(0, 366):
            day = today - timedelta(days=i)
            if i == 0 and not has_activity(day):
                break
            if has_activity(day):
                current += 1
            else:
                break

        # Longest streak over last 365 days
        best = 0
        streak = 0
        for i in range(0, 366):
            day = today - timedelta(days=i)
            if has_activity(day):
                streak += 1
                best = max(best, streak)
            else:
                streak = 0

        return current, best

    @classmethod
    def get_user_streak_data(cls, user) -> StreakData:
        activity_map = cls._fetch_activity_map(user, days=365)
        current, best = cls._compute_streaks(activity_map)
        return StreakData(current_streak=current, longest_streak=best, activity_map=activity_map)

    @classmethod
    def refresh_user_streak(cls, user, notify_on_increase: bool = True) -> StreakData:
        """Compute, persist and optionally notify on streak increase.

        notify_on_increase: if True, creates a 'daily_streak' notification when
        the streak increases compared to the stored value.
        """
        prev_streak = int(getattr(user, 'streak', 0) or 0)
        data = cls.get_user_streak_data(user)
        try:
            # Persist the current streak on the user model for admin display
            # Do not overwrite other fields to avoid race conditions
            if prev_streak != data.current_streak:
                # If streak increased, we may also award XP once per day (server-authoritative)
                increased = data.current_streak > prev_streak
                today = timezone.now().date()

                # Use a transaction for atomicity when awarding XP and creating notification
                with transaction.atomic():
                    # Always persist the latest streak value
                    user.streak = int(max(0, data.current_streak))

                    xp_awarded = 0
                    if notify_on_increase and increased:
                        # Ensure idempotency using the presence of today's daily_streak notification
                        already = UserNotification.objects.filter(
                            user=user,
                            type='daily_streak',
                            created_at__date=today
                        ).exists()
                        if not already:
                            # Compute XP for the new streak day
                            xp_awarded = int(cls._calculate_streak_xp(data.current_streak))
                            try:
                                # Safely increment XP
                                new_xp = int((user.xp or 0)) + xp_awarded
                                user.xp = max(0, new_xp)
                            except Exception:
                                # In case of unexpected values, do not block the flow
                                xp_awarded = 0

                            # Create the daily streak notification (includes XP info)
                            try:
                                UserNotification.objects.create(
                                    user=user,
                                    type='daily_streak',
                                    title='🔥 Streak quotidien',
                                    message=f"{data.current_streak} jours consécutifs",
                                    data={'current_streak': data.current_streak, 'xp_awarded': xp_awarded}
                                )
                            except Exception:
                                # Notification errors should not break the request
                                pass

                    # Save user updates (streak and maybe xp)
                    try:
                        if xp_awarded > 0:
                            user.save(update_fields=['streak', 'xp'])
                        else:
                            user.save(update_fields=['streak'])
                    except Exception:
                        # Avoid breaking request flow on persistence errors
                        pass
        except Exception:
            # Avoid breaking request flow on persistence errors
            pass
        return data


