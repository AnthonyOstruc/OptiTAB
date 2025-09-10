"""
Vues de profil utilisateur refactorisées et simplifiées
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from core.services import ResponseService, QuerySetService
from ..serializers.user_profile import UserDetailSerializer, UserUpdateSerializer
from rest_framework.decorators import api_view
from ..serializers.geographic_data import UserPaysNiveauUpdateSerializer
from pays.models import Pays, Niveau
from django.db.models import F, Q, Count, IntegerField
from django.db.models.functions import Cast, TruncDate
from users.models import CustomUser, ParentChild, UserNotification
from ..serializers.user_profile import UserNotificationSerializer
from suivis.models import SuiviExercice
from django.utils import timezone
from datetime import timedelta
import logging
logger = logging.getLogger(__name__)
import secrets
import string


class MeView(APIView):
    """Récupère les informations de l'utilisateur connecté"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            # Utilise le service de requête optimisée
            user = QuerySetService.get_user_queryset().get(id=request.user.id)
            serializer = UserDetailSerializer(user)
            return ResponseService.success(
                message="Profil récupéré avec succès",
                data=serializer.data
            )
        except Exception as e:
            return ResponseService.error(
                message="Erreur lors de la récupération du profil",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MeGamificationView(APIView):
    """Retourne un résumé gamification (xp, level, progression)."""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            total_xp = user.xp or 0
            
            # Utiliser la nouvelle logique de niveaux progressifs
            from suivis.views import calculate_user_level
            level, next_level_xp, xp_to_next = calculate_user_level(total_xp)
            
            data = {
                'xp': total_xp,
                'level': level,
                'next_level_xp': next_level_xp,
                'xp_to_next': xp_to_next
            }
            return ResponseService.success(
                message="Gamification récupérée avec succès",
                data=data
            )
        except Exception:
            return ResponseService.error(
                message="Erreur lors de la récupération gamification",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateUserXPView(APIView):
    """Met à jour les XP de l'utilisateur connecté"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        try:
            xp_delta = request.data.get('xp_delta')
            reason = request.data.get('reason', 'unknown')
            
            if xp_delta is None or not isinstance(xp_delta, (int, float)):
                return ResponseService.error(
                    message="xp_delta doit être un nombre valide",
                    status_code=status.HTTP_400_BAD_REQUEST
                )
            
            user = request.user
            old_xp = user.xp or 0
            new_xp = old_xp + int(xp_delta)
            
            # Mettre à jour les XP de l'utilisateur
            user.xp = new_xp
            user.save(update_fields=['xp'])
            
            # Calculer le nouveau niveau
            from suivis.views import calculate_user_level
            level, next_level_xp, xp_to_next = calculate_user_level(new_xp)
            
            # Log debug (silencieux en prod)
            logger.debug(f"XP gagnés: {xp_delta} pour {user.email} ({reason})")
            
            data = {
                'old_xp': old_xp,
                'new_xp': new_xp,
                'xp_gained': xp_delta,
                'level': level,
                'xp_to_next': xp_to_next,
                'reason': reason
            }
            
            # Créer une notification XP si gain
            try:
                gained = int(xp_delta)
            except Exception:
                gained = 0

            if gained != 0:
                try:
                    UserNotification.objects.create(
                        user=user,
                        type='xp_gained' if gained > 0 else 'achievement',
                        title='🎉 XP Gagnés !' if gained > 0 else 'Mise à jour XP',
                        message=(f"+{gained} XP" if gained > 0 else f"{gained} XP"),
                        data={'reason': reason, 'xp_delta': gained}
                    )
                except Exception:
                    pass

            # Adapter le message selon si c'est un gain ou une perte d'XP
            message = f"XP mis à jour avec succès ({'+' if xp_delta >= 0 else ''}{xp_delta})"
            
            return ResponseService.success(
                message=message,
                data=data
            )
            
        except Exception as e:
            return ResponseService.error(
                message=f"Erreur lors de la mise à jour des XP: {str(e)}",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class LeaderboardView(APIView):
    """Classement des utilisateurs basé sur l'XP.
    - scope: global | pays | niveau (par défaut: global)
    - limit: nombre d'entrées à retourner (max 100)
    Retourne aussi la position de l'utilisateur courant.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            scope = (request.query_params.get('scope') or 'global').lower()
            try:
                limit = int(request.query_params.get('limit', '20'))
            except ValueError:
                limit = 20
            limit = max(1, min(limit, 100))

            user = request.user

            qs = CustomUser.objects.filter(is_active=True)
            if scope == 'pays' and user.pays_id:
                qs = qs.filter(pays_id=user.pays_id)
            elif scope == 'niveau' and user.niveau_pays_id:
                qs = qs.filter(niveau_pays_id=user.niveau_pays_id)
            # sinon: global

            qs = qs.select_related('pays', 'niveau_pays').order_by('-xp', 'date_joined')

            total = qs.count()

            # Top N
            top_qs = qs[:limit]

            def abbreviate_name(first_name: str, last_name: str):
                first = (first_name or '').strip()
                last = (last_name or '').strip()
                if not first and not last:
                    return 'Étudiant(e)'
                initial = (last[:1] + '.').upper() if last else ''
                return (first + ' ' + initial).strip()

            top = []
            # Calcul des rangs pour le top par cumul des XP supérieurs
            # (OK à cette échelle, optimisable plus tard avec Window/Rank si besoin)
            for u in top_qs:
                better = qs.filter(xp__gt=u.xp).count()
                rank = better + 1
                top.append({
                    'id': u.id,
                    'display_name': abbreviate_name(u.first_name, u.last_name),
                    'xp': u.xp or 0,
                    'pays_flag': getattr(u.pays, 'drapeau_emoji', None),
                    'niveau': getattr(u.niveau_pays, 'nom', None),
                    'rank': rank,
                })

            # Rang de l'utilisateur courant
            me = None
            if total > 0:
                my_better = qs.filter(xp__gt=(user.xp or 0)).count()
                my_rank = my_better + 1
                percentile = 0.0
                try:
                    percentile = round(100.0 * (1.0 - ((my_rank - 1) / float(total))), 2)
                except Exception:
                    percentile = 0.0

                me = {
                    'id': user.id,
                    'display_name': abbreviate_name(user.first_name, user.last_name),
                    'xp': user.xp or 0,
                    'rank': my_rank,
                    'total': total,
                    'percentile': percentile,
                    'pays_flag': getattr(user.pays, 'drapeau_emoji', None),
                    'niveau': getattr(user.niveau_pays, 'nom', None),
                }

            data = {
                'scope': scope,
                'total': total,
                'leaderboard': top,
                'me': me,
            }

            return ResponseService.success(
                message="Leaderboard récupéré avec succès",
                data=data
            )
        except Exception as e:
            return ResponseService.error(
                message="Erreur lors de la récupération du leaderboard",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MyChildrenView(APIView):
    """Liste les enfants rattachés à un compte parent."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if getattr(request.user, 'role', 'student') != 'parent':
                return ResponseService.success(
                    message="Aucun enfant (utilisateur non parent)",
                    data={ 'children': [] }
                )

            children_qs = CustomUser.objects.select_related('pays', 'niveau_pays').filter(
                parent_links__parent=request.user
            )

            weekly_goal = 20

            def child_payload(u: CustomUser):
                # Statistiques basiques
                q = SuiviExercice.objects.filter(user=u)
                try:
                    done_total = q.count()
                    acquired_count = q.filter(est_correct=True).count()
                    not_acquired_count = q.filter(est_correct=False).count()
                    week_cut = timezone.now() - timedelta(days=7)
                    weekly_done = q.filter(date_creation__gte=week_cut).count()

                    # Dernière activité
                    last = q.select_related(
                        'exercice',
                        'exercice__chapitre',
                        'exercice__chapitre__notion',
                        'exercice__chapitre__notion__theme',
                        'exercice__chapitre__notion__theme__matiere',
                    ).order_by('-date_creation').first()
                    last_payload = None
                    if last and getattr(last, 'exercice', None):
                        ex = last.exercice
                        chapitre_title = getattr(ex.chapitre, 'titre', None)
                        last_payload = {
                            'exercice_id': ex.id,
                            'exercice_title': getattr(ex, 'titre', None) or f"Exercice {ex.id}",
                            'chapitre_title': chapitre_title,
                            'when': last.date_creation.isoformat() if last.date_creation else None,
                        }
                except Exception:
                    done_total = acquired_count = not_acquired_count = weekly_done = 0
                    last_payload = None

                weekly_progress = 0
                try:
                    weekly_progress = int(min(100, round((weekly_done / float(weekly_goal)) * 100))) if weekly_goal else 0
                except Exception:
                    weekly_progress = 0

                return {
                    'id': u.id,
                    'first_name': u.first_name,
                    'last_name': u.last_name,
                    'display_name': f"{(u.first_name or '').strip()} {(u.last_name or '')[:1].upper()}.".strip() or 'Élève',
                    'xp': u.xp or 0,
                    'level': (u.xp or 0) // 10,
                    'pays_flag': getattr(u.pays, 'drapeau_emoji', None),
                    'niveau': getattr(u.niveau_pays, 'nom', None),
                    'metrics': {
                        'done_total': done_total,
                        'acquired_count': acquired_count,
                        'not_acquired_count': not_acquired_count,
                        'weekly_done': weekly_done,
                        'weekly_goal': weekly_goal,
                        'weekly_progress': weekly_progress,
                    },
                    'last_activity': last_payload,
                }

            data = {
                'children': [child_payload(u) for u in children_qs]
            }

            return ResponseService.success(
                message="Enfants récupérés avec succès",
                data=data
            )
        except Exception:
            return ResponseService.error(
                message="Erreur lors de la récupération des enfants",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class ChildOverviewView(APIView):
    """Détail d'un enfant pour le parent: métriques, progression, activités."""
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id: int):
        try:
            # Vérifier le lien parent-enfant
            if getattr(request.user, 'role', 'student') != 'parent':
                return ResponseService.error(
                    message="Accès réservé aux parents",
                    status_code=status.HTTP_403_FORBIDDEN
                )

            try:
                link_exists = ParentChild.objects.filter(parent=request.user, child_id=child_id).exists()
                if not link_exists:
                    return ResponseService.error(
                        message="Enfant non lié à ce compte parent",
                        status_code=status.HTTP_404_NOT_FOUND
                    )
            except Exception:
                return ResponseService.error(
                    message="Validation du lien parent-enfant échouée",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            # Infos enfant
            child = CustomUser.objects.select_related('pays', 'niveau_pays').get(id=child_id)

            weekly_goal = 20
            q = SuiviExercice.objects.filter(user_id=child_id)

            # KPIs globaux
            try:
                done_total = q.count()
                acquired_count = q.filter(est_correct=True).count()
                not_acquired_count = q.filter(est_correct=False).count()
            except Exception:
                done_total = acquired_count = not_acquired_count = 0

            # Progression hebdomadaire (7 derniers jours)
            week_cut = timezone.now() - timedelta(days=7)
            weekly_done = q.filter(date_creation__gte=week_cut).count()
            try:
                weekly_progress = int(min(100, round((weekly_done / float(weekly_goal)) * 100))) if weekly_goal else 0
            except Exception:
                weekly_progress = 0

            # Répartition quotidienne sur 7 jours
            daily_raw = (
                q.filter(date_creation__gte=week_cut)
                 .annotate(day=TruncDate('date_creation'))
                 .values('day')
                 .annotate(total=Count('id'), correct=Count('id', filter=Q(est_correct=True)))
                 .order_by('day')
            )
            daily_map = {str(d['day']): {'total': d['total'], 'correct': d['correct']} for d in daily_raw}

            daily_counts = []
            for i in range(6, -1, -1):
                d = (timezone.now() - timedelta(days=i)).date()
                key = str(d)
                vals = daily_map.get(key, {'total': 0, 'correct': 0})
                daily_counts.append({
                    'date': d.isoformat(),
                    'total': vals['total'],
                    'correct': vals['correct']
                })

            # Activités récentes
            last_qs = (
                q.select_related(
                    'exercice',
                    'exercice__chapitre',
                    'exercice__chapitre__notion',
                    'exercice__chapitre__notion__theme',
                    'exercice__chapitre__notion__theme__matiere',
                ).order_by('-date_creation')[:10]
            )
            last_activities = []
            for s in last_qs:
                ex = s.exercice
                chapitre_title = getattr(ex.chapitre, 'titre', None) or getattr(ex.chapitre, 'nom', None)
                matiere_name = None
                try:
                    matiere_name = getattr(ex.chapitre.notion.theme.matiere, 'titre', None)
                except Exception:
                    matiere_name = None
                last_activities.append({
                    'id': s.id,
                    'exercice_id': getattr(ex, 'id', None),
                    'exercice_title': getattr(ex, 'titre', None) or f"Exercice {getattr(ex, 'id', '?')}",
                    'chapitre_title': chapitre_title,
                    'matiere': matiere_name,
                    'est_correct': bool(s.est_correct),
                    'when': s.date_creation.isoformat() if getattr(s, 'date_creation', None) else None,
                })

            # Répartition par matière (acquis / à revoir)
            by_matiere_raw = (
                q.select_related(
                    'exercice__chapitre__notion__theme__matiere'
                )
                .values(
                    'exercice__chapitre__notion__theme__matiere_id',
                    'exercice__chapitre__notion__theme__matiere__titre'
                )
                .annotate(
                    total=Count('id'),
                    correct=Count('id', filter=Q(est_correct=True))
                )
                .order_by('-total')
            )
            by_matieres = []
            for row in by_matiere_raw:
                total = row['total'] or 0
                correct = row['correct'] or 0
                not_correct = max(0, total - correct)
                by_matieres.append({
                    'id': row['exercice__chapitre__notion__theme__matiere_id'],
                    'name': row['exercice__chapitre__notion__theme__matiere__titre'] or 'Matière',
                    'total': total,
                    'acquired': correct,
                    'to_review': not_correct,
                })

            payload = {
                'child': {
                    'id': child.id,
                    'first_name': child.first_name,
                    'last_name': child.last_name,
                    'display_name': f"{(child.first_name or '').strip()} {(child.last_name or '')[:1].upper()}.".strip() or 'Élève',
                    'xp': child.xp or 0,
                    'level': (child.xp or 0) // 10,
                    'pays_flag': getattr(child.pays, 'drapeau_emoji', None),
                    'niveau': getattr(child.niveau_pays, 'nom', None),
                },
                'metrics': {
                    'done_total': done_total,
                    'acquired_count': acquired_count,
                    'not_acquired_count': not_acquired_count,
                    'weekly_done': weekly_done,
                    'weekly_goal': weekly_goal,
                    'weekly_progress': weekly_progress,
                },
                'weekly_trend': daily_counts,
                'last_activities': last_activities,
                'by_matieres': by_matieres,
            }

            return ResponseService.success(
                message="Détail enfant récupéré avec succès",
                data=payload
            )
        except CustomUser.DoesNotExist:
            return ResponseService.error(
                message="Enfant introuvable",
                status_code=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return ResponseService.error(
                message="Erreur lors de la récupération du détail enfant",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MyOverviewView(APIView):
    """Vue d'ensemble pour l'élève courant: métriques, tendance hebdo, activité, répartition par matière."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            weekly_goal = 20
            q = SuiviExercice.objects.filter(user=user)

            # KPIs globaux
            try:
                done_total = q.count()
                acquired_count = q.filter(est_correct=True).count()
                not_acquired_count = q.filter(est_correct=False).count()
            except Exception:
                done_total = acquired_count = not_acquired_count = 0

            # Progression hebdomadaire
            week_cut = timezone.now() - timedelta(days=7)
            weekly_done = q.filter(date_creation__gte=week_cut).count()
            try:
                weekly_progress = int(min(100, round((weekly_done / float(weekly_goal)) * 100))) if weekly_goal else 0
            except Exception:
                weekly_progress = 0

            # Répartition quotidienne sur 7 jours
            daily_raw = (
                q.filter(date_creation__gte=week_cut)
                 .annotate(day=TruncDate('date_creation'))
                 .values('day')
                 .annotate(total=Count('id'), correct=Count('id', filter=Q(est_correct=True)))
                 .order_by('day')
            )
            daily_map = {str(d['day']): {'total': d['total'], 'correct': d['correct']} for d in daily_raw}
            daily_counts = []
            for i in range(6, -1, -1):
                d = (timezone.now() - timedelta(days=i)).date()
                key = str(d)
                vals = daily_map.get(key, {'total': 0, 'correct': 0})
                daily_counts.append({
                    'date': d.isoformat(),
                    'total': vals['total'],
                    'correct': vals['correct']
                })

            # Activités récentes
            last_qs = (
                q.select_related(
                    'exercice',
                    'exercice__chapitre',
                    'exercice__chapitre__notion',
                    'exercice__chapitre__notion__theme',
                    'exercice__chapitre__notion__theme__matiere',
                ).order_by('-date_creation')[:10]
            )
            last_activities = []
            for s in last_qs:
                ex = s.exercice
                chapitre_title = getattr(ex.chapitre, 'titre', None) or getattr(ex.chapitre, 'nom', None)
                matiere_name = None
                try:
                    matiere_name = getattr(ex.chapitre.notion.theme.matiere, 'titre', None)
                except Exception:
                    matiere_name = None
                last_activities.append({
                    'id': s.id,
                    'exercice_id': getattr(ex, 'id', None),
                    'exercice_title': getattr(ex, 'titre', None) or f"Exercice {getattr(ex, 'id', '?')}",
                    'chapitre_title': chapitre_title,
                    'matiere': matiere_name,
                    'est_correct': bool(s.est_correct),
                    'when': s.date_creation.isoformat() if getattr(s, 'date_creation', None) else None,
                })

            # Répartition par matière
            by_matiere_raw = (
                q.select_related('exercice__chapitre__notion__theme__matiere')
                 .values(
                    'exercice__chapitre__notion__theme__matiere_id',
                    'exercice__chapitre__notion__theme__matiere__titre'
                 )
                 .annotate(total=Count('id'), correct=Count('id', filter=Q(est_correct=True)))
                 .order_by('-total')
            )
            by_matieres = []
            for row in by_matiere_raw:
                total = row['total'] or 0
                correct = row['correct'] or 0
                not_correct = max(0, total - correct)
                by_matieres.append({
                    'id': row['exercice__chapitre__notion__theme__matiere_id'],
                    'name': row['exercice__chapitre__notion__theme__matiere__titre'] or 'Matière',
                    'total': total,
                    'acquired': correct,
                    'to_review': not_correct,
                })

            payload = {
                'metrics': {
                    'done_total': done_total,
                    'acquired_count': acquired_count,
                    'not_acquired_count': not_acquired_count,
                    'weekly_done': weekly_done,
                    'weekly_goal': weekly_goal,
                    'weekly_progress': weekly_progress,
                },
                'weekly_trend': daily_counts,
                'last_activities': last_activities,
                'by_matieres': by_matieres,
            }

            return ResponseService.success(
                message="Vue d'ensemble élève récupérée",
                data=payload
            )
        except Exception:
            return ResponseService.error(
                message="Erreur lors de la récupération de la vue d'ensemble",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class MyStreaksView(APIView):
    """Renvoie streak actuel, meilleur streak et activité journalière récente pour l'élève courant."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            # Map activité par jour (90 derniers jours)
            cut = timezone.now() - timedelta(days=90)
            q = SuiviExercice.objects.filter(user=user, date_creation__gte=cut)
            daily_raw = (
                q.annotate(day=TruncDate('date_creation'))
                 .values('day')
                 .annotate(total=Count('id'))
                 .order_by('day')
            )
            activity_map = {str(d['day']): (d['total'] or 0) for d in daily_raw}

            # Calcul streaks sur 365 jours glissants
            today = timezone.now().date()
            def has_activity(d):
                return activity_map.get(str(d), 0) > 0

            # current streak
            cur = 0
            for i in range(0, 366):
                day = today - timedelta(days=i)
                if i == 0 and not has_activity(day):
                    break
                if has_activity(day):
                    cur += 1
                else:
                    break

            # longest streak
            best = 0
            streak = 0
            for i in range(0, 366):
                day = today - timedelta(days=i)
                if has_activity(day):
                    streak += 1
                    best = max(best, streak)
                else:
                    streak = 0

            # Derniers 60 jours pour heatmap
            last_days = []
            for i in range(59, -1, -1):
                day = today - timedelta(days=i)
                last_days.append({
                    'date': str(day),
                    'count': activity_map.get(str(day), 0)
                })

            data = {
                'current_streak': cur,
                'longest_streak': best,
                'last_days': last_days,
            }

            return ResponseService.success(
                message="Streaks récupérés",
                data=data
            )
        except Exception:
            return ResponseService.error(
                message="Erreur lors de la récupération des streaks",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RecommendationsView(APIView):
    """Propose 3 prochaines actions: une révision due, un exercice non tenté, un rappel de quiz (simple)."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = request.user
            q = SuiviExercice.objects.select_related(
                'exercice', 'exercice__chapitre', 'exercice__chapitre__notion', 'exercice__chapitre__notion__theme', 'exercice__chapitre__notion__theme__matiere'
            ).filter(user=user)

            # Index par exercice
            by_ex = {}
            for s in q:
                ex = s.exercice
                if not ex:
                    continue
                d = getattr(s, 'date_creation', None)
                meta = by_ex.setdefault(ex.id, {'attempts': 0, 'last_date': None, 'last_correct': None, 'last_obj': None})
                meta['attempts'] += 1
                if not meta['last_date'] or (d and d > meta['last_date']):
                    meta['last_date'] = d
                    meta['last_correct'] = bool(s.est_correct)
                    meta['last_obj'] = s

            # 1) Révision due: dernier statut incorrect + interval
            def interval_for_attempts(n):
                if n <= 1:
                    return 1
                if n == 2:
                    return 3
                if n == 3:
                    return 7
                return 14
            today = timezone.now().date()
            review_candidate = None
            review_due_date = None
            for ex_id, meta in by_ex.items():
                if meta['last_correct'] is True:
                    continue
                attempts = meta['attempts']
                interval = interval_for_attempts(attempts)
                last_d = (meta['last_date'] or timezone.now()).date()
                due = last_d + timedelta(days=interval)
                if due <= today:
                    if not review_candidate or due < review_due_date:
                        review_candidate = meta['last_obj']
                        review_due_date = due

            review = None
            if review_candidate and getattr(review_candidate, 'exercice', None):
                ex = review_candidate.exercice
                chapitre = ex.chapitre
                review = {
                    'type': 'review',
                    'exercice_id': ex.id,
                    'chapitre_id': getattr(chapitre, 'id', None),
                    'title': getattr(ex, 'titre', None) or f"Exercice {ex.id}",
                    'chapitre_title': getattr(chapitre, 'titre', None) or getattr(chapitre, 'nom', None)
                }

            # 2) Exercice non tenté: on propose un exercice du chapitre le plus faible (simple heuristique: matière avec plus d'erreurs)
            weakest_matiere_id = None
            by_matiere = {}
            for s in q:
                try:
                    mid = s.exercice.chapitre.notion.theme.matiere_id
                except Exception:
                    mid = None
                if not mid:
                    continue
                stat = by_matiere.setdefault(mid, {'total': 0, 'errors': 0})
                stat['total'] += 1
                if not s.est_correct:
                    stat['errors'] += 1
            if by_matiere:
                weakest_matiere_id = sorted(by_matiere.items(), key=lambda kv: (kv[1]['errors'], kv[1]['total']), reverse=True)[0][0]

            # Fallback: aucune matière détectée, on ne propose pas
            new_ex = None
            if weakest_matiere_id:
                # choisir un exercice non tenté dans cette matière (requête légère, best-effort)
                from curriculum.models import Exercice
                tried_ids = set(by_ex.keys())
                ex_qs = Exercice.objects.select_related('chapitre').filter(
                    chapitre__notion__theme__matiere_id=weakest_matiere_id
                ).exclude(id__in=tried_ids)[:1]
                ex = ex_qs.first()
                if ex:
                    new_ex = {
                        'type': 'new_exercice',
                        'exercice_id': ex.id,
                        'chapitre_id': getattr(ex.chapitre, 'id', None),
                        'title': getattr(ex, 'titre', None) or f"Exercice {ex.id}",
                        'chapitre_title': getattr(ex.chapitre, 'titre', None) or getattr(ex.chapitre, 'nom', None)
                    }

            # 3) Quick quiz (placeholder): à brancher sur modèle Quiz si besoin
            quick_quiz = None

            data = {
                'recommendations': [r for r in [review, new_ex, quick_quiz] if r]
            }
            return ResponseService.success(
                message="Recommandations récupérées",
                data=data
            )
        except Exception:
            return ResponseService.error(
                message="Erreur lors de la récupération des recommandations",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AddChildView(APIView):
    """Lie un compte élève existant au parent connecté (par email ou id)."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            if getattr(request.user, 'role', 'student') != 'parent':
                return ResponseService.error(
                    message="Accès réservé aux parents",
                    status_code=status.HTTP_403_FORBIDDEN
                )

            email = (request.data.get('email') or '').strip().lower()
            child_id = request.data.get('child_id')

            child = None
            if email:
                try:
                    child = CustomUser.objects.get(email__iexact=email)
                except CustomUser.DoesNotExist:
                    return ResponseService.error(
                        message="Aucun élève trouvé avec cet email",
                        status_code=status.HTTP_404_NOT_FOUND
                    )
            elif child_id:
                try:
                    child = CustomUser.objects.get(id=child_id)
                except CustomUser.DoesNotExist:
                    return ResponseService.error(
                        message="Élève introuvable",
                        status_code=status.HTTP_404_NOT_FOUND
                    )
            else:
                return ResponseService.error(
                    message="Veuillez fournir un email ou un child_id",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if child.id == request.user.id:
                return ResponseService.error(
                    message="Vous ne pouvez pas vous lier vous‑même",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if getattr(child, 'role', 'student') != 'student':
                return ResponseService.error(
                    message="Le compte spécifié n'est pas un élève",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Création idempotente
            ParentChild.objects.get_or_create(parent=request.user, child=child)

            # Payload simple
            data = {
                'id': child.id,
                'email': child.email,
                'first_name': child.first_name,
                'last_name': child.last_name,
            }
            return ResponseService.success(
                message="Lien parent‑enfant ajouté",
                data=data
            )
        except Exception:
            return ResponseService.error(
                message="Erreur lors de l'ajout de l'enfant",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class RemoveChildView(APIView):
    """Délie un enfant du parent connecté."""
    permission_classes = [IsAuthenticated]

    def delete(self, request, child_id: int):
        try:
            if getattr(request.user, 'role', 'student') != 'parent':
                return ResponseService.error(
                    message="Accès réservé aux parents",
                    status_code=status.HTTP_403_FORBIDDEN
                )

            deleted, _ = ParentChild.objects.filter(parent=request.user, child_id=child_id).delete()
            if deleted == 0:
                # Idempotent: considérer succès même si déjà supprimé
                return ResponseService.success(
                    message="Lien déjà absent",
                    data={'removed': False}
                )
            return ResponseService.success(
                message="Lien parent‑enfant supprimé",
                data={'removed': True}
            )
        except Exception:
            return ResponseService.error(
                message="Erreur lors de la suppression du lien",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CreateChildAccountView(APIView):
    """Permet à un parent de créer un compte élève et de le lier automatiquement."""
    permission_classes = [IsAuthenticated]

    @staticmethod
    def _generate_temp_password(length: int = 12) -> str:
        alphabet = string.ascii_letters + string.digits
        return ''.join(secrets.choice(alphabet) for _ in range(length))

    def post(self, request):
        try:
            if getattr(request.user, 'role', 'student') != 'parent':
                return ResponseService.error(
                    message="Accès réservé aux parents",
                    status_code=status.HTTP_403_FORBIDDEN
                )

            email = (request.data.get('email') or '').strip().lower()
            first_name = (request.data.get('first_name') or '').strip()
            last_name = (request.data.get('last_name') or '').strip()
            pays_id = request.data.get('pays_id')
            niveau_pays_id = request.data.get('niveau_pays_id')

            if not email or not first_name or not last_name:
                return ResponseService.error(
                    message="Champs requis: email, first_name, last_name",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            if CustomUser.objects.filter(email__iexact=email).exists():
                return ResponseService.error(
                    message="Un compte existe déjà avec cet email",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            temp_password = self._generate_temp_password()

            # Créer l'élève actif avec rôle student
            child = CustomUser.objects.create_user(
                email=email,
                first_name=first_name,
                last_name=last_name,
                password=temp_password,
                role='student',
                is_active=True,
            )

            # Renseigner pays/niveau si fournis (validation simple)
            try:
                if pays_id:
                    from pays.models import Pays, Niveau
                    pays = Pays.objects.get(id=pays_id, est_actif=True)
                    child.pays = pays
                if niveau_pays_id:
                    from pays.models import Niveau
                    niveau = Niveau.objects.get(id=niveau_pays_id, est_actif=True)
                    # Si pays aussi fourni, vérifier cohérence
                    if child.pays and niveau.pays_id != child.pays_id:
                        return ResponseService.error(
                            message="Le niveau sélectionné ne correspond pas au pays choisi",
                            status_code=status.HTTP_400_BAD_REQUEST
                        )
                    child.niveau_pays = niveau
                child.save()
            except Exception:
                # En cas d'erreur de pays/niveau, laisser l'utilisateur créé, sans bloquer
                pass

            # Lier au parent (idempotent)
            ParentChild.objects.get_or_create(parent=request.user, child=child)

            data = {
                'child': {
                    'id': child.id,
                    'email': child.email,
                    'first_name': child.first_name,
                    'last_name': child.last_name,
                },
                'temp_password': temp_password,
            }
            return ResponseService.success(
                message="Compte enfant créé et lié",
                data=data
            )
        except Exception:
            return ResponseService.error(
                message="Erreur lors de la création du compte enfant",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UpdateProfileView(APIView):
    """Met à jour les informations de base du profil"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupère les informations de base du profil utilisateur"""
        try:
            user = QuerySetService.get_user_queryset().get(id=request.user.id)
            serializer = UserDetailSerializer(user)
            
            return ResponseService.success(
                message="Profil récupéré avec succès",
                data=serializer.data
            )
        except Exception as e:
            return ResponseService.error(
                message="Erreur lors de la récupération du profil",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request):
        user = request.user
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        
        if serializer.is_valid():
            try:
                serializer.save()
                # Retourne les données mises à jour
                updated_user = QuerySetService.get_user_queryset().get(id=user.id)
                response_data = UserDetailSerializer(updated_user).data
                
                return ResponseService.success(
                    message="Profil mis à jour avec succès",
                    data=response_data
                )
            except Exception as e:
                return ResponseService.error(
                    message="Erreur lors de la sauvegarde",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return ResponseService.validation_error(serializer.errors)


class UpdatePaysView(APIView):
    """Met à jour le pays de l'utilisateur"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupère les informations du pays actuel de l'utilisateur"""
        try:
            user = QuerySetService.get_user_queryset().get(id=request.user.id)
            
            if not user.pays:
                return ResponseService.success(
                    message="Aucun pays défini",
                    data={'pays': None}
                )
            
            response_data = {
                'pays': {
                    'id': user.pays.id,
                    'nom': user.pays.nom,
                    'code_iso': user.pays.code_iso,
                    'drapeau_emoji': user.pays.drapeau_emoji
                }
            }
            
            return ResponseService.success(
                message="Pays récupéré avec succès",
                data=response_data
            )
        except Exception as e:
            return ResponseService.error(
                message="Erreur lors de la récupération du pays",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request):
        user = request.user
        pays_id = request.data.get('pays_id')
        
        if not pays_id:
            return ResponseService.error("Le pays_id est requis")
        
        try:
            pays = Pays.objects.get(id=pays_id, est_actif=True)
        except Pays.DoesNotExist:
            return ResponseService.error(
                "Pays non trouvé", 
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        # Vérifier compatibilité niveau/pays
        niveau_reinitialise = False
        if user.niveau_pays and user.niveau_pays.pays != pays:
            user.niveau_pays = None
            niveau_reinitialise = True
            
        user.pays = pays
        user.save()
        
        response_data = {
            'pays': {
                'id': pays.id,
                'nom': pays.nom,
                'code_iso': pays.code_iso,
                'drapeau_emoji': pays.drapeau_emoji
            }
        }
        
        message = f"Pays mis à jour vers {pays.nom}"
        if niveau_reinitialise:
            message += " (niveau réinitialisé pour compatibilité)"
            
        return ResponseService.success(message, response_data)


class UpdateNiveauView(APIView):
    """Met à jour le niveau de l'utilisateur"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupère les informations du niveau actuel de l'utilisateur"""
        try:
            user = QuerySetService.get_user_queryset().get(id=request.user.id)
            
            if not user.niveau_pays:
                return ResponseService.success(
                    message="Aucun niveau défini",
                    data={'niveau_pays': None}
                )
            
            response_data = {
                'niveau_pays': {
                    'id': user.niveau_pays.id,
                    'nom': user.niveau_pays.nom,
                    'couleur': user.niveau_pays.couleur,
                    'pays': {
                        'id': user.niveau_pays.pays.id,
                        'nom': user.niveau_pays.pays.nom,
                        'code_iso': user.niveau_pays.pays.code_iso,
                        'drapeau_emoji': user.niveau_pays.pays.drapeau_emoji
                    }
                }
            }
            
            return ResponseService.success(
                message="Niveau récupéré avec succès",
                data=response_data
            )
        except Exception as e:
            return ResponseService.error(
                message="Erreur lors de la récupération du niveau",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request):
        user = request.user
        niveau_pays_id = request.data.get('niveau_pays_id')
        
        if not niveau_pays_id:
            return ResponseService.error("Le niveau_pays_id est requis")
        
        try:
            niveau_pays = Niveau.objects.get(id=niveau_pays_id, est_actif=True)
        except Niveau.DoesNotExist:
            return ResponseService.error(
                "Niveau non trouvé", 
                status_code=status.HTTP_404_NOT_FOUND
            )
        
        user.niveau_pays = niveau_pays
        user.save()
        
        response_data = {
            'niveau_pays': {
                'id': niveau_pays.id,
                'nom': niveau_pays.nom,
                'couleur': niveau_pays.couleur,
                'pays': {
                    'id': niveau_pays.pays.id,
                    'nom': niveau_pays.pays.nom,
                    'code_iso': niveau_pays.pays.code_iso,
                    'drapeau_emoji': niveau_pays.pays.drapeau_emoji
                }
            }
        }
        
        return ResponseService.success(
            f"Niveau mis à jour vers {niveau_pays.nom}",
            response_data
        )


class UpdatePaysNiveauView(APIView):
    """Met à jour pays et niveau simultanément avec validation"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Récupère les informations pays et niveau actuels de l'utilisateur"""
        try:
            user = QuerySetService.get_user_queryset().get(id=request.user.id)
            
            response_data = {
                'pays': {
                    'id': user.pays.id if user.pays else None,
                    'nom': user.pays.nom if user.pays else None,
                    'code_iso': user.pays.code_iso if user.pays else None,
                    'drapeau_emoji': user.pays.drapeau_emoji if user.pays else None
                } if user.pays else None,
                'niveau_pays': {
                    'id': user.niveau_pays.id if user.niveau_pays else None,
                    'nom': user.niveau_pays.nom if user.niveau_pays else None,
                    'couleur': user.niveau_pays.couleur if user.niveau_pays else None,
                    'pays': {
                        'id': user.niveau_pays.pays.id if user.niveau_pays and user.niveau_pays.pays else None,
                        'nom': user.niveau_pays.pays.nom if user.niveau_pays and user.niveau_pays.pays else None,
                        'code_iso': user.niveau_pays.pays.code_iso if user.niveau_pays and user.niveau_pays.pays else None,
                        'drapeau_emoji': user.niveau_pays.pays.drapeau_emoji if user.niveau_pays and user.niveau_pays.pays else None
                    } if user.niveau_pays and user.niveau_pays.pays else None
                } if user.niveau_pays else None
            }
            
            return ResponseService.success(
                message="Configuration géographique récupérée avec succès",
                data=response_data
            )
        except Exception as e:
            return ResponseService.error(
                message="Erreur lors de la récupération de la configuration géographique",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def patch(self, request):
        serializer = UserPaysNiveauUpdateSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                user = serializer.save(request.user)
                
                response_data = {
                    'pays': {
                        'id': user.pays.id if user.pays else None,
                        'nom': user.pays.nom if user.pays else None,
                        'drapeau_emoji': user.pays.drapeau_emoji if user.pays else None
                    } if user.pays else None,
                    'niveau_pays': {
                        'id': user.niveau_pays.id if user.niveau_pays else None,
                        'nom': user.niveau_pays.nom if user.niveau_pays else None,
                        'couleur': user.niveau_pays.couleur if user.niveau_pays else None,
                    } if user.niveau_pays else None
                }
                
                return ResponseService.success(
                    "Configuration géographique mise à jour avec succès",
                    response_data
                )
            except Exception as e:
                return ResponseService.error(
                    f"Erreur lors de la sauvegarde: {str(e)}",
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return ResponseService.validation_error(serializer.errors)


class UserProfileAPIView(generics.RetrieveUpdateAPIView):
    """Vue générique combinée pour récupérer et mettre à jour le profil"""
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return QuerySetService.get_user_queryset().get(id=self.request.user.id)
    
    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserDetailSerializer
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            # Retourne avec le serializer de lecture
            response_data = UserDetailSerializer(instance).data
            return ResponseService.success(
                "Profil mis à jour avec succès",
                response_data
            )
        
        return ResponseService.validation_error(serializer.errors)
