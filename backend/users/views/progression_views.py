"""
Progression par chapitre (lecture seule) pour le nouvel espace élève et parent.

GET /api/users/me/progression/                    -> élève connecté
GET /api/users/children/<child_id>/progression/   -> parent d'un enfant lié (lien accepté)

Pour chaque chapitre (notion) de la classe de l'élève : nombre d'exercices
publiés, exercices faits, acquis et à revoir, date de la dernière activité.
Ajoute la liste des derniers exercices « à revoir » et le dernier chapitre
travaillé, pour proposer « Reprendre où tu t'es arrêté ».

Quiz de chapitre : chaque chapitre porte sa dernière et sa meilleure note
(sur 20) ; `quiz_recents` liste les derniers quiz passés.
POST /api/users/me/quiz-resultats/  -> enregistre la note d'un quiz complet.
"""
from decimal import Decimal, ROUND_HALF_UP

from django.db.models import Count, Max, Q
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from core.services import ResponseService
from curriculum.models import Exercice, Notion
from suivis.models import ResultatQuizChapitre, SuiviExercice
from users.models import CustomUser, ParentChild

A_REVOIR_MAX = 8
QUIZ_RECENTS_MAX = 6


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
        .order_by('theme__matiere__ordre', 'theme__ordre', 'theme__titre', 'ordre', 'titre')
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

    # Quiz de chapitre : dernière note, meilleure note, nombre de passages
    quiz = {}
    resultats = (
        ResultatQuizChapitre.objects.filter(user=user, notion_id__in=notion_ids)
        .order_by('-date_creation')
        .values('notion_id', 'note', 'date_creation', 'parties')
    )
    for r in resultats:
        q = quiz.get(r['notion_id'])
        note = float(r['note'])
        if q is None:
            quiz[r['notion_id']] = {
                'derniere': note,
                'meilleure': note,
                'essais': 1,
                'quand': _iso(r['date_creation']),
                'a_revoir': [p.get('nom') for p in (r['parties'] or []) if p.get('etat') != 'acquis'],
            }
        else:
            q['meilleure'] = max(q['meilleure'], note)
            q['essais'] += 1
    titres = {n['id']: n['titre'] for n in notions}
    quiz_recents = [
        {'notion_id': r['notion_id'], 'notion': titres.get(r['notion_id']), 'note': float(r['note']),
         'quand': _iso(r['date_creation'])}
        for r in resultats[:QUIZ_RECENTS_MAX]
    ]

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
            'quiz': quiz.get(n['id']),
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
        'quiz_recents': quiz_recents,
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


class MyQuizResultView(APIView):
    """Enregistre la note d'un quiz de chapitre passé en entier par l'élève."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data or {}
        try:
            notion_id = int(data.get('notion'))
            bonnes = int(data.get('bonnes'))
            total = int(data.get('total'))
        except (TypeError, ValueError):
            return ResponseService.error(message="Résultat incomplet", status_code=status.HTTP_400_BAD_REQUEST)
        if not (0 < total <= 100 and 0 <= bonnes <= total):
            return ResponseService.error(message="Résultat invalide", status_code=status.HTTP_400_BAD_REQUEST)
        if not Notion.objects.filter(id=notion_id, est_actif=True).exists():
            return ResponseService.error(message="Chapitre introuvable", status_code=status.HTTP_404_NOT_FOUND)
        parties = []
        for p in (data.get('parties') or [])[:20]:
            if isinstance(p, dict):
                parties.append({
                    'nom': str(p.get('nom', ''))[:120],
                    'bonnes': int(p.get('bonnes') or 0),
                    'total': int(p.get('total') or 0),
                    'etat': str(p.get('etat', ''))[:12],
                })
        note = (Decimal(20 * bonnes) / Decimal(total)).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP)
        resultat = ResultatQuizChapitre.objects.create(
            user=request.user, notion_id=notion_id, bonnes=bonnes, total=total, note=note, parties=parties,
        )
        return ResponseService.success(
            message="Note enregistrée",
            data={'id': resultat.id, 'note': float(note), 'quand': _iso(resultat.date_creation)},
        )
