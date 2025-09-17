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
                user.streak = int(max(0, data.current_streak))
                user.save(update_fields=['streak'])

                # Notify only on increase and only once per day
                if notify_on_increase and data.current_streak > prev_streak:
                    try:
                        today = timezone.now().date()
                        already = UserNotification.objects.filter(
                            user=user,
                            type='daily_streak',
                            created_at__date=today
                        ).exists()
                        if not already:
                            UserNotification.objects.create(
                                user=user,
                                type='daily_streak',
                                title='🔥 Streak quotidien',
                                message=f"{data.current_streak} jours consécutifs",
                                data={'current_streak': data.current_streak}
                            )
                    except Exception:
                        pass
        except Exception:
            # Avoid breaking request flow on persistence errors
            pass
        return data


