"""Règles d'accès communes aux contenus pédagogiques (exercices, cours, quiz...).

Deux règles, écrites une seule fois et partagées par toutes les vues de contenu :

1. ``EcritureAdminMixin`` : créer, modifier, supprimer ou dupliquer un contenu
   est réservé à l'administration (comptes ``is_staff``).
2. ``ListeContenuMixin`` : la liste d'un contenu ne transmet ses parties payantes
   (corrigés, texte du cours, réponses du quiz) qu'aux comptes qui y ont accès,
   avec la même règle que l'ouverture d'un contenu : abonnement ou pass, accès
   offert pour ce niveau, chapitre de découverte du niveau, contenu gratuit.
"""
from rest_framework import status
from rest_framework.response import Response

from .permissions import get_content_niveau, user_has_active_subscription_or_pass

ACTIONS_ADMIN = frozenset({
    'create', 'update', 'partial_update', 'destroy',
    'duplicate', 'duplicate_images',
})
PORTEES_GRATUITES = frozenset({'free', 'both'})


class EcritureAdminMixin:
    """Toute modification de contenu est réservée à l'administration."""

    def check_permissions(self, request):
        super().check_permissions(request)
        if self.action in ACTIONS_ADMIN and not getattr(request.user, 'is_staff', False):
            self.permission_denied(request, message="Action réservée à l'administration.")


class _VerificateurAcces:
    """Dit si un compte peut voir un contenu en entier (mises en cache par requête)."""

    def __init__(self, user):
        self.user = user
        niveau = getattr(user, 'niveau_pays', None)
        self.demo_notion_id = getattr(niveau, 'demo_notion_id', None)
        self._niveau = niveau
        self._demo_exercices = None
        self._par_notion = {}

    def _exercice_de_demo(self, obj):
        if self._niveau is None or obj.__class__.__name__ != 'Exercice':
            return False
        if self._demo_exercices is None:
            self._demo_exercices = set(self._niveau.demo_exercices.values_list('pk', flat=True))
        return obj.pk in self._demo_exercices

    def acces_complet(self, obj):
        if getattr(obj, 'access_scope', None) in PORTEES_GRATUITES:
            return True
        notion_id = getattr(obj, 'notion_id', None)
        if notion_id and notion_id == self.demo_notion_id:
            return True
        if self._exercice_de_demo(obj):
            return True
        if notion_id not in self._par_notion:
            self._par_notion[notion_id] = user_has_active_subscription_or_pass(
                self.user, niveau=get_content_niveau(obj),
            )
        return self._par_notion[notion_id]


class ListeContenuMixin:
    """Liste des contenus, paginée à la demande (``?limit=&offset=``, pour l'admin).

    ``champs_payants`` : ``{champ: valeur envoyée à la place}`` pour un compte sans
    accès. Les autres champs (titre, énoncé...) restent visibles.
    """

    champs_payants = {}

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

    def _donnees(self, request, objets):
        donnees = self.get_serializer(objets, many=True).data
        if not self.champs_payants or user_has_active_subscription_or_pass(request.user):
            return donnees
        verificateur = _VerificateurAcces(request.user)
        for obj, item in zip(objets, donnees):
            if verificateur.acces_complet(obj):
                continue
            for champ, valeur in self.champs_payants.items():
                if champ in item:
                    item[champ] = valeur() if callable(valeur) else valeur
            item['acces_limite'] = True
        return donnees
