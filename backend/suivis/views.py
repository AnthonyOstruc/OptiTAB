"""
VUES ULTRA SIMPLES pour suivis
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .models import SuiviExercice, SuiviQuiz
from .serializers import SuiviExerciceSerializer, SuiviQuizSerializer
from django.db import transaction
from users.models import UserNotification
from django.utils import timezone
from datetime import timedelta
import logging
logger = logging.getLogger(__name__)


def _compute_exercice_xp(points_obtenus: int, est_correct: bool, temps_seconde: int) -> int:
    """
    Les exercices guidés ne donnent AUCUN XP.
    Seuls les quiz donnent des XP.
    """
    return 0


def _compute_quiz_xp(
    user,
    quiz,
    score: int,
    total_points: int,
    temps_total_seconde: int | None,
    tentative_numero: int = 1,
) -> int:
    """
    Logique XP pour quiz (avec coefficients de difficulté et bonus vitesse):
    - Difficulté → coefficient XP : easy=1.0, medium=1.5, hard/difficile=2.0
    - SEULE la 1ère tentative donne des XP : XP = score * coeff (+1 bonus si temps total < 50% du temps autorisé)
    - Tentatives suivantes : 0 XP (système de cooldown de 1h30)

    Le temps autorisé est calculé par question: easy=20s, medium=25s, hard=30s,
    donc total_autorisé = nb_questions * temps_par_question.
    """
    # Seule la première tentative donne des XP
    if tentative_numero > 1:
        return 0

    if total_points <= 0:
        return 0

    # Coefficients selon la difficulté
    difficulty = (getattr(quiz, 'difficulty', None) or getattr(quiz, 'difficulte', None) or 'easy')
    difficulty = str(difficulty).lower()
    coeff_map = {
        'easy': 1.0,
        'facile': 1.0,
        'medium': 1.5,
        'moyen': 1.5,
        'hard': 2.0,
        'difficile': 2.0,
    }
    coeff = coeff_map.get(difficulty, 1.0)

    # Temps par question selon difficulté
    per_question_time_map = {
        'easy': 20,
        'facile': 20,
        'medium': 25,
        'moyen': 25,
        'hard': 30,
        'difficile': 30,
    }
    per_q_time = per_question_time_map.get(difficulty, 20)

    # 1ère tentative : score * coeff (+ éventuel bonus vitesse)
    base_xp = score * coeff
    # Bonus vitesse: +1 XP si répondu à toutes les questions en moins de 50% du temps autorisé
    bonus = 0
    try:
        if temps_total_seconde is not None and total_points > 0:
            allowed_total = total_points * per_q_time
            if temps_total_seconde < 0.5 * allowed_total:
                bonus = 1
    except Exception:
        bonus = 0
    # DB XP est un entier → arrondir à l'entier le plus proche
    return max(0, int(round(base_xp)) + bonus)


def calculate_user_level(total_xp: int) -> tuple[int, int, int]:
    """
    Calcule le niveau, les XP requis pour le niveau suivant et les XP manquants
    Progression exponentielle : niveau N nécessite N * N * 10 XP
    """
    if total_xp <= 0:
        return 0, 10, 10
    
    level = 0
    while True:
        xp_for_next_level = (level + 1) * (level + 1) * 10
        if total_xp < xp_for_next_level:
            break
        level += 1
    
    next_level_xp = (level + 1) * (level + 1) * 10
    xp_to_next = next_level_xp - total_xp
    
    return level, next_level_xp, xp_to_next


def get_next_quiz_attempt_number(user, quiz_id: int) -> int:
    """Retourne le numéro de la prochaine tentative pour ce quiz"""
    try:
        last_attempt = SuiviQuiz.objects.filter(
            user=user, 
            quiz_id=quiz_id
        ).order_by('-tentative_numero').first()
        
        return (last_attempt.tentative_numero + 1) if last_attempt else 1
    except:
        return 1


def check_quiz_cooldown(user, quiz_id: int) -> dict:
    """
    Vérifie si l'utilisateur peut faire une nouvelle tentative du quiz.
    Cooldown de 1h30 entre chaque tentative.
    """
    try:
        last_attempt = SuiviQuiz.objects.filter(
            user=user,
            quiz_id=quiz_id
        ).order_by('-date_creation').first()
        
        if not last_attempt:
            return {
                'can_attempt': True,
                'message': 'Première tentative autorisée'
            }
        
        # Calculer le temps écoulé depuis la dernière tentative
        now = timezone.now()
        time_since_last = now - last_attempt.date_creation
        cooldown_duration = timedelta(hours=1, minutes=30)  # 1h30
        
        if time_since_last >= cooldown_duration:
            return {
                'can_attempt': True,
                'message': 'Nouvelle tentative autorisée'
            }
        else:
            # Calculer le temps restant
            time_remaining = cooldown_duration - time_since_last
            hours = int(time_remaining.total_seconds() // 3600)
            minutes = int((time_remaining.total_seconds() % 3600) // 60)
            
            return {
                'can_attempt': False,
                'message': f'Prochaine tentative dans {hours}h{minutes:02d}min',
                'time_remaining_seconds': int(time_remaining.total_seconds()),
                'time_remaining_formatted': f'{hours}h{minutes:02d}min',
                'next_attempt_time': (last_attempt.date_creation + cooldown_duration).isoformat()
            }
    except Exception as e:
        logger.warning(f"Erreur vérification cooldown: {e}")
        return {
            'can_attempt': True,
            'message': 'Tentative autorisée (erreur de vérification)'
        }


class SuiviExerciceViewSet(viewsets.ModelViewSet):
    queryset = SuiviExercice.objects.all()
    serializer_class = SuiviExerciceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        # Créer le suivi (les exercices guidés ne donnent pas d'XP)
        suivi = serializer.save(user=self.request.user)
        return suivi

    def perform_update(self, serializer):
        # Mettre à jour le suivi (les exercices guidés ne donnent pas d'XP)
        suivi = serializer.save(user=self.request.user)
        return suivi

    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """
        Endpoint pour récupérer les statistiques complètes des exercices de l'utilisateur
        avec filtrage par matière, notion et chapitre
        """
        try:
            # Récupérer tous les exercices de l'utilisateur avec les relations
            user_exercice_suivis = SuiviExercice.objects.filter(user=request.user).select_related(
                'exercice__chapitre__notion__theme__matiere'
            ).order_by('-date_creation')
            
            # Filtres optionnels
            matiere_id = request.query_params.get('matiere')
            notion_id = request.query_params.get('notion')
            chapitre_id = request.query_params.get('chapitre')
            # Limite optionnelle sur le nombre d'éléments renvoyés dans "exercice_list"
            # (utile pour alléger le dashboard tout en conservant les stats globales)
            limit_param = request.query_params.get('limit')
            try:
                limit = int(limit_param) if limit_param is not None else None
                if limit is not None and limit <= 0:
                    limit = None
            except Exception:
                limit = None
            
            if matiere_id:
                user_exercice_suivis = user_exercice_suivis.filter(
                    exercice__chapitre__notion__theme__matiere_id=matiere_id
                )
            if notion_id:
                user_exercice_suivis = user_exercice_suivis.filter(
                    exercice__chapitre__notion_id=notion_id
                )
            if chapitre_id:
                user_exercice_suivis = user_exercice_suivis.filter(
                    exercice__chapitre_id=chapitre_id
                )
            
            # Construire la liste des exercices (avec limitation facultative pour la réponse)
            exercice_list = []  # liste limitée renvoyée au front (payload)
            score_sum = 0       # somme sur tous les suivis
            correct_count = 0   # total correct sur tous les suivis
            total_all_count = 0 # nombre total de suivis
            # Agrégats matière -> notion
            matiere_notion_stats = {}
            
            for idx, suivi in enumerate(user_exercice_suivis):
                exercice = suivi.exercice
                chapitre = exercice.chapitre
                notion = chapitre.notion
                theme = notion.theme
                matiere = theme.matiere
                
                # Score sur 10 basé sur la réussite
                score_on_10 = 10.0 if suivi.est_correct else 0.0
                
                # Construire les données élémentaires (n'ajouter à la liste que si < limit)
                exercice_data = {
                    'id': suivi.id,
                    'exercice_id': exercice.id,
                    'exercice_titre': getattr(exercice, 'titre', ''),
                    'reponse_donnee': suivi.reponse_donnee,
                    'est_correct': suivi.est_correct,
                    'points_obtenus': suivi.points_obtenus,
                    'temps_seconde': suivi.temps_seconde,
                    'score_on_10': score_on_10,
                    'date_creation': suivi.date_creation.isoformat(),
                    'chapitre': {
                        'id': getattr(chapitre, 'id', None),
                        'titre': getattr(chapitre, 'titre', '')
                    },
                    'notion': {
                        'id': getattr(notion, 'id', None),
                        'titre': getattr(notion, 'titre', '')
                    },
                    'theme': {
                        'id': getattr(theme, 'id', None),
                        'titre': getattr(theme, 'titre', '')
                    },
                    'matiere': {
                        'id': getattr(matiere, 'id', None),
                        'titre': getattr(matiere, 'titre', '')
                    }
                }

                # Appliquer la limite de taille sur la payload renvoyée
                if limit is None or idx < limit:
                    exercice_list.append(exercice_data)
                total_all_count += 1
                score_sum += score_on_10
                if suivi.est_correct:
                    correct_count += 1
                # Agrégats matière/notion
                key = (exercice_data['matiere']['id'], exercice_data['notion']['id'])
                if key not in matiere_notion_stats:
                    matiere_notion_stats[key] = {
                        'matiere': {
                            'id': exercice_data['matiere']['id'],
                            'titre': exercice_data['matiere']['titre']
                        },
                        'notion': {
                            'id': exercice_data['notion']['id'],
                            'titre': exercice_data['notion']['titre']
                        },
                        'exercice_count': 0,
                        'correct_count': 0,
                        'incorrect_count': 0,
                    }
                agg = matiere_notion_stats[key]
                agg['exercice_count'] += 1
                if suivi.est_correct:
                    agg['correct_count'] += 1
                else:
                    agg['incorrect_count'] += 1
            
            # Compteurs finaux
            total_exercices_display = len(exercice_list)  # ce qui est renvoyé en liste
            total_exercices_all = total_all_count        # total réel pour les stats globales
            
            # Calculer les notions maîtrisées (au moins un exercice correct par notion)
            notions_with_correct = set()
            for suivi in user_exercice_suivis:
                if suivi.est_correct:
                    notions_with_correct.add(suivi.exercice.chapitre.notion.id)
            mastered_notions = len(notions_with_correct)
            
            # Moyenne générale (sur l'ensemble des suivis)
            average = round(score_sum / total_exercices_all, 1) if total_exercices_all > 0 else 0
            
            # Statistiques par matière (sur l'ensemble des suivis, pas uniquement la liste limitée)
            matiere_stats = {}
            for agg in matiere_notion_stats.values():
                matiere_id = agg['matiere']['id']
                matiere_titre = agg['matiere']['titre']
                if matiere_id not in matiere_stats:
                    matiere_stats[matiere_id] = {
                        'id': matiere_id,
                        'titre': matiere_titre,
                        'exercice_count': 0,
                        'correct_count': 0,
                        'percentage': 0,
                        'average': 0
                    }
                matiere_stats[matiere_id]['exercice_count'] += int(agg.get('exercice_count', 0))
                matiere_stats[matiere_id]['correct_count'] += int(agg.get('correct_count', 0))
            
            # Calculer les pourcentages et moyennes par matière
            for matiere_data in matiere_stats.values():
                if matiere_data['exercice_count'] > 0:
                    matiere_data['percentage'] = round(
                        (matiere_data['correct_count'] / matiere_data['exercice_count']) * 100, 1
                    )
                    matiere_data['average'] = round(
                        (matiere_data['correct_count'] / matiere_data['exercice_count']) * 10, 1
                    )
            
            # Trier l'agrégat matière/notion pour un rendu stable
            matiere_notion_stats_list = list(matiere_notion_stats.values())
            try:
                matiere_notion_stats_list.sort(key=lambda x: (str(x['matiere']['titre']).lower(), str(x['notion']['titre']).lower()))
            except Exception:
                pass

            return Response({
                'global_stats': {
                    'completed': total_exercices_all,
                    'correct': correct_count,
                    'incorrect': max(0, total_exercices_all - correct_count),
                    'percentage': round((correct_count / total_exercices_all) * 100, 1) if total_exercices_all > 0 else 0,
                    'average': round(score_sum / total_exercices_all, 1) if total_exercices_all > 0 else 0,
                    'masteredNotions': mastered_notions
                },
                'exercice_list': exercice_list,
                'matiere_stats': list(matiere_stats.values()),
                'matiere_notion_stats': matiere_notion_stats_list,
                'filters_applied': {
                    'matiere': matiere_id,
                    'notion': notion_id,
                    'chapitre': chapitre_id
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors du calcul des statistiques: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class SuiviQuizViewSet(viewsets.ModelViewSet):
    queryset = SuiviQuiz.objects.all()
    serializer_class = SuiviQuizSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        
        # Filtrer par quiz spécifique si demandé
        quiz_id = self.request.query_params.get('quiz')
        if quiz_id:
            queryset = queryset.filter(quiz_id=quiz_id)
            
        # Filtrer par chapitre si demandé
        chapitre_id = self.request.query_params.get('chapitre')
        if chapitre_id:
            queryset = queryset.filter(quiz__chapitre_id=chapitre_id)
        
        # Ordonner par tentative puis date
        return queryset.order_by('quiz_id', '-tentative_numero', '-date_creation')

    def perform_create(self, serializer):
        with transaction.atomic():
            # Déterminer le numéro de tentative
            quiz_id = serializer.validated_data.get('quiz').id
            
            # Vérifier le cooldown avant de créer la tentative
            cooldown_info = check_quiz_cooldown(self.request.user, quiz_id)
            if not cooldown_info['can_attempt']:
                from rest_framework.exceptions import ValidationError
                raise ValidationError({
                    'detail': cooldown_info['message'],
                    'cooldown_info': cooldown_info
                })
            
            tentative_numero = get_next_quiz_attempt_number(self.request.user, quiz_id)
            
            logger.debug(f"Création tentative quiz {quiz_id} pour user {self.request.user.id}, tentative #{tentative_numero}")
            
            # Calculer les XP pour cette tentative
            quiz_obj = serializer.validated_data.get('quiz')
            xp_gain = _compute_quiz_xp(
                user=self.request.user,
                quiz=quiz_obj,
                score=serializer.validated_data.get('score', 0),
                total_points=serializer.validated_data.get('total_points', 0),
                temps_total_seconde=serializer.validated_data.get('temps_total_seconde', 0),
                tentative_numero=tentative_numero,
            )
            
            logger.debug(f"XP calculés: {xp_gain}")
            
            # Sauvegarder le suivi avec les XP gagnés
            suivi = serializer.save(
                user=self.request.user,
                tentative_numero=tentative_numero,
                xp_gagne=xp_gain
            )
            
            logger.debug(f"Suivi sauvegardé: {suivi.id}")

            try:
                # Mettre à jour les XP et le niveau de l'utilisateur
                user = self.request.user
                user.xp = (user.xp or 0) + max(0, xp_gain)
                
                # Le niveau est calculé dynamiquement dans le serializer, pas stocké en BDD
                user.save(update_fields=["xp"])
                
                print(f"🆙 Utilisateur mis à jour: XP={user.xp}")

                # Notification persistante si XP gagnés
                if int(max(0, xp_gain)) > 0:
                    try:
                        UserNotification.objects.create(
                            user=user,
                            type='xp_gained',
                            title='🎉 XP Gagnés !',
                            message=f"+{int(max(0, xp_gain))} XP pour \"{getattr(quiz_obj, 'titre', 'Quiz')}\"",
                            data={'quiz_id': getattr(quiz_obj, 'id', None), 'tentative': tentative_numero}
                        )
                    except Exception:
                        pass
            except Exception as e:
                logger.error(f"Erreur mise à jour utilisateur: {e}")
                pass
                
            return suivi
            
    def create(self, request, *args, **kwargs):
        """Override pour retourner les XP gagnés dans la réponse"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        suivi = self.perform_create(serializer)
        
        # Retourner les données avec les XP gagnés
        response_data = SuiviQuizSerializer(suivi).data
        # Ajout de champs utiles pour le frontend
        response_data.update({
            'xp_gagne': getattr(suivi, 'xp_gagne', 0),
            'tentative_numero': getattr(suivi, 'tentative_numero', 1)
        })
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_update(self, serializer):
        # Empêcher la modification des tentatives de quiz pour préserver l'intégrité
        # Une fois un quiz terminé, le résultat ne peut plus être modifié
        pass

    @action(detail=False, methods=['get'], url_path='check-cooldown/(?P<quiz_id>[^/.]+)')
    def check_cooldown(self, request, quiz_id=None):
        """
        Endpoint pour vérifier le cooldown d'un quiz spécifique
        """
        try:
            quiz_id = int(quiz_id)
            cooldown_info = check_quiz_cooldown(request.user, quiz_id)
            return Response(cooldown_info)
        except (ValueError, TypeError):
            return Response(
                {'error': 'ID de quiz invalide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f'Erreur lors de la vérification: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """
        Endpoint pour récupérer les statistiques complètes des quiz de l'utilisateur
        avec filtrage par matière, notion et chapitre
        """
        try:
            # Récupérer tous les quiz de l'utilisateur avec les relations
            user_quiz_attempts = SuiviQuiz.objects.filter(user=request.user).select_related(
                'quiz__chapitre__notion__theme__matiere'
            ).order_by('-date_creation')
            
            # Filtres optionnels
            matiere_id = request.query_params.get('matiere')
            notion_id = request.query_params.get('notion')
            chapitre_id = request.query_params.get('chapitre')
            
            # Paramètre facultatif pour limiter la taille de la payload renvoyée dans "quiz_list"
            # Les statistiques globales sont toujours calculées sur l'ensemble des données
            limit_param = request.query_params.get('limit')
            try:
                limit = int(limit_param) if limit_param is not None else None
                if limit is not None and limit <= 0:
                    limit = None
            except Exception:
                limit = None

            if matiere_id:
                user_quiz_attempts = user_quiz_attempts.filter(
                    quiz__chapitre__notion__theme__matiere_id=matiere_id
                )
            if notion_id:
                user_quiz_attempts = user_quiz_attempts.filter(
                    quiz__chapitre__notion_id=notion_id
                )
            if chapitre_id:
                user_quiz_attempts = user_quiz_attempts.filter(
                    quiz__chapitre_id=chapitre_id
                )
            
            # Construire la liste des quiz avec seulement la dernière tentative de chaque quiz
            quiz_latest_attempts = {}
            quiz_best_scores = {}
            
            # D'abord, identifier la dernière tentative pour chaque quiz
            for attempt in user_quiz_attempts:
                quiz_id = attempt.quiz.id
                score_on_10 = 0
                if attempt.total_points > 0:
                    score_on_10 = round((attempt.score / attempt.total_points) * 10, 1)
                
                # Garder seulement la dernière tentative (date la plus récente)
                if quiz_id not in quiz_latest_attempts or attempt.date_creation > quiz_latest_attempts[quiz_id]['date_creation']:
                    quiz = attempt.quiz
                    chapitre = quiz.chapitre
                    notion = chapitre.notion
                    theme = notion.theme
                    matiere = theme.matiere
                    
                    quiz_latest_attempts[quiz_id] = {
                        'id': attempt.id,
                        'quiz_id': quiz.id,
                        'quiz_titre': quiz.titre,
                        'score': attempt.score,
                        'total_points': attempt.total_points,
                        'score_on_10': score_on_10,
                        'tentative_numero': attempt.tentative_numero,
                        'date_creation': attempt.date_creation,
                        'temps_total_seconde': attempt.temps_total_seconde,
                        'total_attempts': user_quiz_attempts.filter(quiz_id=quiz_id).count(),
                        'chapitre': {
                            'id': chapitre.id,
                            'titre': chapitre.titre
                        },
                        'notion': {
                            'id': notion.id,
                            'titre': notion.titre
                        },
                        'theme': {
                            'id': theme.id,
                            'titre': theme.titre
                        },
                        'matiere': {
                            'id': matiere.id,
                            'titre': matiere.titre
                        }
                    }
                
                # Toujours tracker le meilleur score pour les notions maîtrisées
                if quiz_id not in quiz_best_scores or score_on_10 > quiz_best_scores[quiz_id]:
                    quiz_best_scores[quiz_id] = score_on_10
            
            # Construire la liste complète (toutes dernières tentatives) triée par date
            full_quiz_list = []
            total_score_sum = 0

            for quiz_data in quiz_latest_attempts.values():
                quiz_data['date_creation'] = quiz_data['date_creation'].isoformat()
                full_quiz_list.append(quiz_data)
                total_score_sum += quiz_data['score_on_10']

            # Trier par date décroissante pour la payload et l'affichage
            try:
                full_quiz_list.sort(key=lambda x: x['date_creation'], reverse=True)
            except Exception:
                pass

            total_attempts = len(full_quiz_list)
            
            # Calculer les notions maîtrisées (quiz avec meilleur score >= 7/10)
            mastered_notions = sum(1 for score in quiz_best_scores.values() if score >= 7)
            
            # Moyenne générale
            average = round(total_score_sum / total_attempts, 1) if total_attempts > 0 else 0
            
            # Statistiques par matière
            matiere_stats = {}
            for attempt_data in full_quiz_list:
                matiere_id = attempt_data['matiere']['id']
                matiere_titre = attempt_data['matiere']['titre']
                
                if matiere_id not in matiere_stats:
                    matiere_stats[matiere_id] = {
                        'id': matiere_id,
                        'titre': matiere_titre,
                        'quiz_count': 0,
                        'total_score': 0,
                        'average': 0
                    }
                
                matiere_stats[matiere_id]['quiz_count'] += 1
                matiere_stats[matiere_id]['total_score'] += attempt_data['score_on_10']
            
            # Agrégat matière/notion (mêmes clés que exercices pour cohérence frontend)
            matiere_notion_stats = {}
            for attempt_data in full_quiz_list:
                mat = attempt_data['matiere']
                notion = attempt_data['notion']
                key = (mat['id'], notion['id'])
                if key not in matiere_notion_stats:
                    matiere_notion_stats[key] = {
                        'matiere': { 'id': mat['id'], 'titre': mat['titre'] },
                        'notion': { 'id': notion['id'], 'titre': notion['titre'] },
                        'exercice_count': 0,
                        'correct_count': 0,
                        'incorrect_count': 0,
                    }
                agg = matiere_notion_stats[key]
                agg['exercice_count'] += 1
                if (attempt_data.get('score_on_10') or 0) >= 7:
                    agg['correct_count'] += 1
                else:
                    agg['incorrect_count'] += 1

            # Liste triée pour stabilité d'affichage
            matiere_notion_stats_list = list(matiere_notion_stats.values())
            try:
                matiere_notion_stats_list.sort(key=lambda x: (str(x['matiere']['titre']).lower(), str(x['notion']['titre']).lower()))
            except Exception:
                pass

            # Calculer les moyennes par matière
            for matiere_data in matiere_stats.values():
                if matiere_data['quiz_count'] > 0:
                    matiere_data['average'] = round(matiere_data['total_score'] / matiere_data['quiz_count'], 1)
            
            # Appliquer la limite sur la payload de la liste (sans impacter les stats)
            quiz_list_payload = full_quiz_list
            if limit is not None:
                try:
                    quiz_list_payload = full_quiz_list[:limit]
                except Exception:
                    pass

            return Response({
                'global_stats': {
                    'completed': total_attempts,
                    'average': average,
                    'masteredNotions': mastered_notions
                },
                'quiz_list': quiz_list_payload,
                'matiere_stats': list(matiere_stats.values()),
                'matiere_notion_stats': matiere_notion_stats_list,
                'filters_applied': {
                    'matiere': matiere_id,
                    'notion': notion_id,
                    'chapitre': chapitre_id
                }
            })
            
        except Exception as e:
            return Response(
                {'error': f'Erreur lors du calcul des statistiques: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Alias pour les "statuts" - renvoie les suivis d'exercices
class StatusViewSet(viewsets.ModelViewSet):
    """
    Alias pour les statuts - utilise les suivis d'exercices
    Compatible avec l'ancienne API frontend
    """
    queryset = SuiviExercice.objects.all()
    serializer_class = SuiviExerciceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)

    def perform_create(self, serializer):
        # Créer le suivi via l'alias "status" (les exercices guidés ne donnent pas d'XP)
        suivi = serializer.save(user=self.request.user)
        return suivi

    def perform_update(self, serializer):
        # Mettre à jour le suivi via l'alias "status" (les exercices guidés ne donnent pas d'XP)
        suivi = serializer.save(user=self.request.user)
        return suivi

    def create(self, request, *args, **kwargs):
        """Retourne le suivi. Les exercices guidés ne donnent pas d'XP."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        suivi = self.perform_create(serializer)

        response_data = SuiviExerciceSerializer(suivi).data
        # Les exercices guidés ne donnent jamais d'XP
        response_data.update({ 'xp_gagne': 0 })
        return Response(response_data, status=status.HTTP_201_CREATED)