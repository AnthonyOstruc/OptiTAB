"""Règles d'accès communes aux contenus pédagogiques (cours, fiches, exercices, quiz).

Écrites une seule fois et partagées par toutes les vues de contenu :

1. ``EcritureAdminMixin`` : créer, modifier, supprimer ou dupliquer un contenu
   est réservé à l'administration (comptes ``is_staff``).

2. ``ContenuMixin`` : ce qu'un compte reçoit en lecture (liste et détail).
   - Accès complet : administration, abonnement ou pass pour la classe du
     contenu, accès offert pour cette classe.
   - Sinon, APERÇU, identique pour tous les chapitres (maths, physique-chimie) :
       cours      -> la première partie seulement (jusqu'au deuxième « ## ») ;
       exercices  -> un seul exercice ouvert par chapitre (le premier facile) ;
                     les autres ne transmettent que leur titre et leur difficulté ;
       fiches, quiz -> verrouillés (aucun contenu transmis).
   La portée « gratuit » d'un contenu (access_scope) désigne les pages publiques
   /ressources-gratuites/ : elle n'ouvre rien de plus dans l'espace connecté.
   Le reste ne quitte jamais le serveur : rien n'est « caché » côté navigateur.
"""
import re

from rest_framework import status
from rest_framework.response import Response

from .permissions import HasActiveSubscriptionOrPass, get_content_niveau, user_has_active_subscription_or_pass

ACTIONS_ADMIN = frozenset({
    'create', 'update', 'partial_update', 'destroy',
    'duplicate', 'duplicate_images',
})
PORTEES_GRATUITES = frozenset({'free', 'both'})
TITRE_DE_PARTIE = re.compile(r'^##\s', re.M)


class EcritureAdminMixin:
    """Toute modification de contenu est réservée à l'administration."""

    def check_permissions(self, request):
        super().check_permissions(request)
        if self.action in ACTIONS_ADMIN and not getattr(request.user, 'is_staff', False):
            self.permission_denied(request, message="Action réservée à l'administration.")


def debut_du_cours(texte):
    """Première partie d'un cours au format OptiTAB v1 (aperçu gratuit).

    Coupe juste avant le deuxième titre de partie (« ## II. … »). Sans titres de
    partie, garde le premier tiers, arrêté à un paragraphe hors encadré (``:::``) ;
    s'il n'existe aucune coupe sûre, ne montre rien plutôt que tout.
    """
    texte = texte or ''
    titres = [m.start() for m in TITRE_DE_PARTIE.finditer(texte)]
    if len(titres) >= 2:
        return texte[:titres[1]].rstrip() + '\n'

    cible, position, ouverts = len(texte) // 3, 0, 0
    for ligne in texte.splitlines(keepends=True):
        position += len(ligne)
        contenu = ligne.strip()
        if contenu.startswith(':::'):
            ouverts += 1 if contenu != ':::' else -1
        if not contenu and ouverts <= 0 and cible <= position < len(texte):
            return texte[:position].rstrip() + '\n'
    return ''


class AccesContenu:
    """Dit, pour un compte, si un contenu est reçu en entier (résultats gardés le temps d'une requête)."""

    def __init__(self, user):
        self.user = user
        self._par_notion = {}
        self._exercices_ouverts = {}

    def _classe_ouverte(self, obj):
        notion_id = getattr(obj, 'notion_id', None)
        if notion_id not in self._par_notion:
            self._par_notion[notion_id] = user_has_active_subscription_or_pass(
                self.user, niveau=get_content_niveau(obj),
            )
        return self._par_notion[notion_id]

    def _exercice_d_apercu(self, exercice):
        """L'exercice ouvert à tous dans ce chapitre : le premier exercice facile, pris de
        préférence parmi ceux des pages gratuites publiques (portée « gratuit »)."""
        notion_id = exercice.notion_id
        if notion_id not in self._exercices_ouverts:
            exercices = list(
                type(exercice).objects.filter(notion_id=notion_id, est_actif=True)
                .order_by('id').values_list('id', 'difficulty', 'access_scope')  # ordre affiché à l'élève
            )
            publics = [e for e in exercices if e[2] in PORTEES_GRATUITES]
            candidats = (
                [i for i, difficulte, _ in publics if difficulte == 'easy']
                or [i for i, difficulte, _ in exercices if difficulte == 'easy']
                or [i for i, _, _ in publics]
                or [i for i, _, _ in exercices]
            )
            self._exercices_ouverts[notion_id] = candidats[0] if candidats else None
        return exercice.pk == self._exercices_ouverts[notion_id]

    def complet(self, obj):
        if getattr(self.user, 'is_staff', False) or self._classe_ouverte(obj):
            return True
        return obj.__class__.__name__ == 'Exercice' and self._exercice_d_apercu(obj)


class ContenuMixin:
    """Lecture d'un contenu : liste (paginée à la demande, ``?limit=&offset=``) et détail.

    ``champs_payants`` : ``{champ: remplacement}`` appliqué quand le compte n'a pas
    l'accès complet. Le remplacement est une valeur, ou une fonction qui reçoit la
    valeur d'origine (ex. ``debut_du_cours``). Sans ``champs_payants``, rien n'est limité.
    ``detail_en_apercu`` : le détail est servi limité (cours) au lieu d'être refusé.
    """

    champs_payants = {}
    detail_en_apercu = False

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        limit = request.query_params.get('limit')
        if limit is None:
            return Response(self._donnees(request, list(queryset)))

        try:
            limit_value = int(limit)
            offset_value = int(request.query_params.get('offset') or 0)
            if limit_value <= 0 or offset_value < 0:
                raise ValueError
        except ValueError:
            return Response({'detail': 'Paramètres de pagination invalides'}, status=status.HTTP_400_BAD_REQUEST)

        objets = list(queryset[offset_value:offset_value + limit_value])
        return Response({
            'count': queryset.count(),
            'limit': limit_value,
            'offset': offset_value,
            'results': self._donnees(request, objets),
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        donnees = self.get_serializer(instance).data
        if self.champs_payants and not AccesContenu(request.user).complet(instance):
            if not self.detail_en_apercu:
                self.permission_denied(request, message=HasActiveSubscriptionOrPass.message)
            self._limiter(donnees)
        return Response(donnees)

    def _limiter(self, item):
        for champ, remplacement in self.champs_payants.items():
            if champ in item:
                item[champ] = remplacement(item[champ]) if callable(remplacement) else remplacement
        item['acces_limite'] = True

    def _donnees(self, request, objets):
        donnees = self.get_serializer(objets, many=True).data
        if not self.champs_payants or getattr(request.user, 'is_staff', False):
            return donnees
        acces = AccesContenu(request.user)
        for obj, item in zip(objets, donnees):
            if not acces.complet(obj):
                self._limiter(item)
        return donnees


def images_visibles(queryset, user, parent, apercu=False):
    """Images d'un contenu qu'un compte peut recevoir.

    Administration ou classe ouverte : toutes. Sinon, seulement celles du contenu
    demandé (``parent``), s'il est reçu en entier — ou en aperçu (cours).
    """
    if getattr(user, 'is_staff', False) or getattr(user, 'is_superuser', False):
        return queryset
    if user_has_active_subscription_or_pass(user, niveau=getattr(user, 'niveau_pays', None)):
        return queryset
    if parent is not None and (apercu or AccesContenu(user).complet(parent)):
        return queryset
    return queryset.none()


def vide(_valeur):
    """Remplacement pour un champ de type liste."""
    return []
