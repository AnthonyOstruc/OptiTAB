"""
VUES ULTRA SIMPLES pour suivis
"""
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from .models import SuiviExercice, SuiviQuiz, QuizSubmission
from .serializers import SuiviExerciceSerializer, SuiviQuizSerializer, QuizSubmissionSerializer
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
    Nouvelle logique XP pour quiz (seulement première tentative):
    - EASY: 1 XP par bonne réponse + 2 XP bonus si sans faute
    - MEDIUM: 2 XP par bonne réponse + 3 XP bonus si sans faute  
    - HARD: 3 XP par bonne réponse + 3 XP bonus si sans faute
    - Tentatives suivantes : 0 XP
    """
    # Seule la première tentative donne des XP
    if tentative_numero > 1:
        return 0

    if total_points <= 0:
        return 0

    # Déterminer la difficulté
    difficulty = (getattr(quiz, 'difficulty', None) or getattr(quiz, 'difficulte', None) or 'easy')
    difficulty = str(difficulty).lower()
    
    # XP par bonne réponse selon la difficulté
    xp_per_correct_map = {
        'easy': 1,
        'facile': 1,
        'medium': 2,
        'moyen': 2,
        'hard': 3,
        'difficile': 3,
    }
    
    # Bonus sans faute selon la difficulté
    perfect_bonus_map = {
        'easy': 2,
        'facile': 2,
        'medium': 3,
        'moyen': 3,
        'hard': 3,
        'difficile': 3,
    }
    
    xp_per_correct = xp_per_correct_map.get(difficulty, 1)
    perfect_bonus = perfect_bonus_map.get(difficulty, 2)
    
    # Calculer les XP de base (bonnes réponses)
    base_xp = score * xp_per_correct
    
    # Bonus si sans faute (score = total_points)
    perfect_bonus_xp = 0
    if score == total_points and total_points > 0:
        perfect_bonus_xp = perfect_bonus
    
    total_xp = base_xp + perfect_bonus_xp
    
    return max(0, total_xp)


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
            # Choisir l'utilisateur cible (lui-même, ou un enfant si parent)
            target_user_id = request.user.id
            child_id_param = request.query_params.get('child_id') or request.query_params.get('child')
            if child_id_param:
                try:
                    child_id_int = int(child_id_param)
                except Exception:
                    return Response({'error': 'child_id invalide'}, status=status.HTTP_400_BAD_REQUEST)

                # Vérifier le lien parent-enfant
                from users.models import ParentChild
                link_exists = ParentChild.objects.filter(
                    parent=request.user,
                    child_id=child_id_int,
                    status=ParentChild.STATUS_ACCEPTED,
                ).exists()
                if not link_exists:
                    return Response({'error': 'Enfant non lié à ce compte parent'}, status=status.HTTP_403_FORBIDDEN)
                target_user_id = child_id_int

            # Récupérer tous les exercices de l'utilisateur cible avec les relations
            user_exercice_suivis = SuiviExercice.objects.filter(user_id=target_user_id).select_related(
                'exercice__notion__theme__matiere'
            ).order_by('-date_creation')
            
            # Filtres optionnels
            matiere_id = request.query_params.get('matiere')
            notion_id = request.query_params.get('notion')
            chapitre_id = request.query_params.get('chapitre')  # obsolète
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
                    exercice__notion__theme__matiere_id=matiere_id
                )
            if notion_id:
                user_exercice_suivis = user_exercice_suivis.filter(
                    exercice__notion_id=notion_id
                )
            # chapitre_id ignoré désormais
            
            # Construire la liste des exercices (avec limitation facultative pour la réponse)
            exercice_list = []  # liste limitée renvoyée au front (payload)
            score_sum = 0       # somme sur tous les suivis
            correct_count = 0   # total correct sur tous les suivis
            total_all_count = 0 # nombre total de suivis
            # Agrégats matière -> notion
            matiere_notion_stats = {}
            
            for idx, suivi in enumerate(user_exercice_suivis):
                exercice = suivi.exercice
                notion = exercice.notion
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
                if suivi.est_correct and getattr(suivi.exercice, 'notion', None):
                    notions_with_correct.add(getattr(suivi.exercice.notion, 'id', None))
            mastered_notions = len([n for n in notions_with_correct if n is not None])
            
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

                # Streak supprimé: ne rien faire ici
                
                print(f"🆙 Utilisateur mis à jour: XP={user.xp}")

                # Notification XP gérée par le frontend (notificationStore)
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

    
    @action(detail=False, methods=['get'], url_path='stats')
    def stats(self, request):
        """
        Endpoint pour récupérer les statistiques complètes des quiz de l'utilisateur
        avec filtrage par matière, notion et chapitre
        """
        try:
            # Récupérer tous les quiz de l'utilisateur avec les relations
            user_quiz_attempts = SuiviQuiz.objects.filter(user=request.user).select_related(
                'quiz__notion__theme__matiere'
            ).order_by('-date_creation')
            
            # Filtres optionnels
            matiere_id = request.query_params.get('matiere')
            notion_id = request.query_params.get('notion')
            chapitre_id = request.query_params.get('chapitre')  # obsolète
            
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
                    quiz__notion__theme__matiere_id=matiere_id
                )
            if notion_id:
                user_quiz_attempts = user_quiz_attempts.filter(
                    quiz__notion_id=notion_id
                )
            # chapitre_id ignoré désormais
            
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
                    notion = quiz.notion
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


class QuizSubmissionViewSet(viewsets.ModelViewSet):
    """
    ViewSet pour gérer les soumissions manuelles de quiz
    - Les élèves peuvent voir leurs propres soumissions
    - Les admins peuvent voir toutes les soumissions et les noter
    """
    queryset = QuizSubmission.objects.all()
    serializer_class = QuizSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """Filtre selon le rôle de l'utilisateur"""
        user = self.request.user
        queryset = super().get_queryset().select_related(
            'user', 'quiz', 'quiz__notion', 'corrige_par'
        )
        
        # Les admins voient tout, les élèves voient seulement leurs soumissions
        if not user.is_staff:
            queryset = queryset.filter(user=user)
        
        # Filtres optionnels pour l'admin
        if user.is_staff:
            status_filter = self.request.query_params.get('status')
            user_id = self.request.query_params.get('user')
            quiz_id = self.request.query_params.get('quiz')
            pays_id = self.request.query_params.get('pays')
            niveau_id = self.request.query_params.get('niveau')
            
            if status_filter:
                queryset = queryset.filter(status=status_filter)
            if user_id:
                queryset = queryset.filter(user_id=user_id)
            if quiz_id:
                queryset = queryset.filter(quiz_id=quiz_id)
            if pays_id:
                queryset = queryset.filter(user__pays_id=pays_id)
            if niveau_id:
                queryset = queryset.filter(user__niveau_pays_id=niveau_id)
        
        return queryset.order_by('-date_creation')

    def perform_create(self, serializer):
        """
        Créer une soumission
        - Élève: crée pour lui-même
        - Admin: peut spécifier un user_id pour créer pour un élève
        """
        user = self.request.user
        target_user = user
        
        # Si admin et user_id fourni, créer pour cet utilisateur
        if user.is_staff:
            user_id = self.request.data.get('user_id') or self.request.data.get('user')
            if user_id:
                from django.contrib.auth import get_user_model
                User = get_user_model()
                try:
                    target_user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    pass
        
        # Sauvegarder la soumission
        submission = serializer.save(user=target_user)
        
        # Envoyer un email de confirmation à l'élève
        try:
            from core.services import EmailService
            from django.conf import settings
            from django.core.mail import EmailMultiAlternatives
            
            quiz_title = submission.quiz.titre if submission.quiz else "Quiz"
            student_name = target_user.first_name or 'OptiTABien'
            
            subject = f'Votre quiz "{quiz_title}" a bien été reçu'
            text_body = (
                f"Bonjour {student_name},\n\n"
                f"Nous avons bien reçu votre soumission pour le quiz \"{quiz_title}\".\n\n"
                f"Votre travail sera corrigé et noté dans les plus brefs délais.\n"
                f"Vous recevrez un email dès que la correction sera disponible.\n\n"
                f"Bon courage pour la suite !\n"
                f"L'équipe OptiTAB"
            )
            
            logo_url = EmailService._resolve_logo_url()
            html_body = f"""
                <div style="font-family:'Helvetica Neue',Arial,sans-serif;background:#f9fafb;padding:24px 0;">
                  <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;margin:0 auto;background:#ffffff;border-radius:16px;border:1px solid #e5e7eb;overflow:hidden;">
                    <tr>
                      <td style="padding:24px 24px 0 24px;">
                        {f'<img src="{logo_url}" alt="OptiTAB" style="height:56px;width:auto;display:block;margin-bottom:16px;"/>' if logo_url else ''}
                        <h1 style="margin:0 0 12px 0;font-size:22px;color:#111827;">Quiz bien reçu ✅</h1>
                        <p style="margin:0;color:#4b5563;font-size:15px;line-height:1.6;">
                          Bonjour {student_name},<br/>
                          Nous avons bien reçu votre soumission pour le quiz <strong>"{quiz_title}"</strong>.
                        </p>
                      </td>
                    </tr>
                    <tr>
                      <td style="padding:24px;">
                        <div style="background:#eff6ff;border:2px solid #93c5fd;padding:16px;border-radius:10px;margin-bottom:16px;">
                          <p style="margin:0;color:#1e40af;font-size:14px;line-height:1.6;">
                            📝 Votre travail sera corrigé et noté dans les plus brefs délais.
                          </p>
                        </div>
                        <p style="margin:16px 0 0 0;color:#6b7280;font-size:14px;line-height:1.6;">
                          Vous recevrez un email dès que la correction sera disponible dans votre espace personnel.
                        </p>
                        <p style="margin:16px 0 0 0;color:#6b7280;font-size:14px;line-height:1.6;">
                          Bon courage pour la suite !<br/>
                          L'équipe OptiTAB
                        </p>
                      </td>
                    </tr>
                  </table>
                </div>
            """
            
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[target_user.email],
            )
            email.attach_alternative(html_body, "text/html")
            email.send(fail_silently=False)
            logger.info(f"Email de confirmation de soumission envoyé à {target_user.email}")
        except Exception as e:
            logger.warning(f"Erreur lors de l'envoi de l'email de confirmation: {e}")

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminUser])
    def grade(self, request, pk=None):
        """Action pour noter une soumission (admin seulement)"""
        submission = self.get_object()
        
        note = request.data.get('note')
        commentaire = request.data.get('commentaire', '')
        
        # Validation de la note
        if note is None:
            return Response(
                {'error': 'La note est requise'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            note = float(note)
            if note < 0 or note > 20:
                return Response(
                    {'error': 'La note doit être entre 0 et 20'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
        except (ValueError, TypeError):
            return Response(
                {'error': 'Note invalide'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Mettre à jour la soumission
        submission.note = note
        submission.commentaire = commentaire
        submission.status = 'graded'
        submission.corrige_par = request.user
        submission.date_correction = timezone.now()
        submission.save()
        
        # Envoyer un email de notification à l'élève
        try:
            from core.services import EmailService
            quiz_title = submission.quiz.titre if submission.quiz else "Quiz"
            EmailService.send_quiz_grade_notification(
                user=submission.user,
                quiz_title=quiz_title,
                note=note,
                commentaire=commentaire
            )
        except Exception as e:
            logger.warning(f"Erreur lors de l'envoi de l'email de notation: {e}")
        
        serializer = self.get_serializer(submission)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Statistiques pour l'élève ou l'admin"""
        user = request.user
        
        if user.is_staff:
            # Stats admin: toutes les soumissions
            total = QuizSubmission.objects.count()
            pending = QuizSubmission.objects.filter(status='pending').count()
            graded = QuizSubmission.objects.filter(status='graded').count()
            
            return Response({
                'total': total,
                'pending': pending,
                'graded': graded
            })
        else:
            # Stats élève: ses propres soumissions
            user_submissions = QuizSubmission.objects.filter(user=user)
            total = user_submissions.count()
            pending = user_submissions.filter(status='pending').count()
            graded = user_submissions.filter(status='graded').count()
            
            # Calculer la moyenne des notes
            graded_submissions = user_submissions.filter(status='graded', note__isnull=False)
            moyenne = None
            if graded_submissions.exists():
                moyenne = round(
                    sum(s.note for s in graded_submissions) / graded_submissions.count(), 
                    2
                )
            
            return Response({
                'total': total,
                'pending': pending,
                'graded': graded,
                'moyenne': moyenne
            })
