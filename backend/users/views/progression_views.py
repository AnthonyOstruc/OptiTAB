"""
Progression par chapitre (lecture seule) pour le nouvel espace élève et parent.

GET /api/users/me/progression/                    -> élève connecté
GET /api/users/children/<child_id>/progression/   -> parent d'un enfant lié (lien accepté)

Pour chaque chapitre (notion) de la classe de l'élève : nombre d'exercices
publiés, exercices faits, acquis et à revoir, date de la dernière activité.
Ajoute la liste des derniers exercices « à revoir » et le dernier chapitre
travaillé, pour proposer « Reprendre où tu t'es arrêté ».
"""
from django.db.models import Count, Max, Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.services import ResponseService
from curriculum.models import Exercice, Notion
from suivis.models import SuiviExercice
from users.models import CustomUser, ParentChild

A_REVOIR_MAX = 8


def _iso(value):
    return value.isoformat() if value else None


def build_progression(user):
    niveau = getattr(user, 'niveau_pays', None)
    pays = getattr(user, 'pays', None)

    notions_qs = Notion.objects.filter(est_actif=True, theme__est_actif=True)
    if niveau:
        notions_qs = notions_qs.filter(theme__contexte__niveau=niveau)
    elif pays:
        notions_qs = notions_qs.filter(theme__contexte__niveau__pays=pays)
    else:
        notions_qs = notions_qs.none()

    notions = list(
        notions_qs
        .order_by('theme__ordre', 'theme__titre', 'ordre', 'titre')
        .values('id', 'titre', 'ordre', 'theme_id', 'theme__titre', 'theme__ordre',
                'theme__matiere_id', 'theme__matiere__titre')
    )
    notion_ids = [n['id'] for n in notions]

    totals = dict(
        Exercice.objects
        .filter(notion_id__in=notion_ids, est_actif=True)
        .values('notion_id')
        .annotate(n=Count('id'))
        .values_list('notion_id', 'n')
    )

    suivis = SuiviExercice.objects.filter(user=user, exercice__notion_id__in=notion_ids)
    stats = {
        row['exercice__notion_id']: row
        for row in suivis.values('exercice__notion_id').annotate(
            faits=Count('id'),
            acquis=Count('id', filter=Q(est_correct=True)),
            derniere=Max('date_modification'),
        )
    }

    chapitres = []
    for n in notions:
        s = stats.get(n['id'], {})
        faits = s.get('faits', 0)
        acquis = s.get('acquis', 0)
        chapitres.append({
            'id': n['id'],
            'titre': n['titre'],
            'theme_id': n['theme_id'],
            'theme': n['theme__titre'],
            'matiere_id': n['theme__matiere_id'],
            'matiere': n['theme__matiere__titre'],
            'exercices': totals.get(n['id'], 0),
            'faits': faits,
            'acquis': acquis,
            'a_revoir': max(0, faits - acquis),
            'derniere_activite': _iso(s.get('derniere')),
        })

    a_revoir = [
        {
            'exercice_id': s.exercice_id,
            'exercice': s.exercice.titre,
            'notion_id': s.exercice.notion_id,
            'notion': getattr(s.exercice.notion, 'titre', None),
            'quand': _iso(s.date_modification),
        }
        for s in (
            suivis.filter(est_correct=False)
            .select_related('exercice', 'exercice__notion')
            .order_by('-date_modification')[:A_REVOIR_MAX]
        )
    ]

    derniere = suivis.select_related('exercice', 'exercice__notion').order_by('-date_modification').first()
    derniere_activite = None
    if derniere and derniere.exercice:
        derniere_activite = {
            'notion_id': derniere.exercice.notion_id,
            'notion': getattr(derniere.exercice.notion, 'titre', None),
            'exercice_id': derniere.exercice_id,
            'quand': _iso(derniere.date_modification),
        }

    return {
        'niveau': getattr(niveau, 'nom', None),
        'chapitres': chapitres,
        'a_revoir': a_revoir,
        'derniere_activite': derniere_activite,
    }


class MyProgressionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            return ResponseService.success(message="Progression récupérée", data=build_progression(request.user))
        except Exception:
            return ResponseService.error(
                message="Erreur lors du calcul de la progression",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class ChildProgressionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, child_id: int):
        if getattr(request.user, 'role', 'student') != 'parent':
            return ResponseService.error(message="Accès réservé aux parents", status_code=status.HTTP_403_FORBIDDEN)
        linked = ParentChild.objects.filter(
            parent=request.user, child_id=child_id, status=ParentChild.STATUS_ACCEPTED
        ).exists()
        if not linked:
            return ResponseService.error(message="Enfant non lié à ce compte parent", status_code=status.HTTP_404_NOT_FOUND)
        try:
            child = CustomUser.objects.select_related('pays', 'niveau_pays').get(id=child_id)
            return ResponseService.success(message="Progression récupérée", data=build_progression(child))
        except CustomUser.DoesNotExist:
            return ResponseService.error(message="Enfant introuvable", status_code=status.HTTP_404_NOT_FOUND)
        except Exception:
            return ResponseService.error(
                message="Erreur lors du calcul de la progression",
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
