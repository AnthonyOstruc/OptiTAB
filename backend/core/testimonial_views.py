"""
Vues API des temoignages (captures WhatsApp / SMS de la page « lien en bio »).

Endpoint public en lecture seule + CRUD reserve aux administrateurs pour le
studio d'administration. Meme style que les vues admin du blog : fonctions
decorees, pas de ViewSet.
"""
import logging

from rest_framework import status
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from .models import BioLandingSettings, Testimonial
from .serializers import TestimonialAdminSerializer, TestimonialPublicSerializer

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Mise en ligne de la page /avis
# ---------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def bio_landing_status(request):
    """La page est-elle ouverte au public ?

    Appele par la page elle-meme au chargement : si la reponse est `false`
    et que le visiteur n'est pas administrateur, il est renvoye a l'accueil.
    """
    return Response({'published': BioLandingSettings.load().is_published})


@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_bio_landing_update(request):
    """Met la page en ligne ou la retire, depuis le studio."""
    value = request.data.get('published')

    # Le multipart transmet des chaines. On n'accepte QUE des valeurs connues :
    # interpreter une saisie inattendue comme « false » retirerait la page en
    # silence, ce qui est bien pire qu'une erreur explicite.
    if isinstance(value, str):
        normalized = value.strip().lower()
        if normalized in ('true', '1', 'on', 'yes'):
            value = True
        elif normalized in ('false', '0', 'off', 'no'):
            value = False
        else:
            value = None

    if not isinstance(value, bool):
        return Response(
            {'published': ['Valeur booleenne attendue.']},
            status=status.HTTP_400_BAD_REQUEST,
        )

    settings_obj = BioLandingSettings.load()
    settings_obj.is_published = value
    settings_obj.save()

    return Response({'published': settings_obj.is_published})


# ---------------------------------------------------------------------------
# Public
# ---------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([AllowAny])
def testimonial_list(request):
    """Temoignages publies, dans l'ordre choisi dans le studio."""
    queryset = (
        Testimonial.objects
        .filter(is_published=True, est_actif=True)
        .exclude(image='')
        .order_by('ordre', '-date_creation')
    )
    serializer = TestimonialPublicSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)


# ---------------------------------------------------------------------------
# Administration
# ---------------------------------------------------------------------------

@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_testimonial_list(request):
    """Tous les temoignages, publies ou non."""
    queryset = Testimonial.objects.all().order_by('ordre', '-date_creation')
    serializer = TestimonialAdminSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def admin_testimonial_create(request):
    """Ajoute une capture. L'image arrive en multipart."""
    serializer = TestimonialAdminSerializer(data=request.data, context={'request': request})
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Nouvelle entree placee en fin de liste par defaut.
    if not serializer.validated_data.get('ordre'):
        last = Testimonial.objects.order_by('-ordre').first()
        serializer.validated_data['ordre'] = (last.ordre + 1) if last else 0

    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def admin_testimonial_detail(request, pk):
    """Modifie ou supprime un temoignage."""
    try:
        testimonial = Testimonial.objects.get(pk=pk)
    except Testimonial.DoesNotExist:
        return Response({'detail': 'Temoignage introuvable.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'DELETE':
        # On tente d'effacer le fichier pour ne pas laisser de capture
        # orpheline sur le stockage. Mais l'utilisateur IAM du bucket n'a pas
        # forcement le droit s3:DeleteObject : dans ce cas la suppression du
        # temoignage doit quand meme aboutir, sinon l'admin reste bloque avec
        # une entree qu'il ne peut plus retirer de la page.
        if testimonial.image:
            try:
                testimonial.image.delete(save=False)
            except Exception:
                logger.warning(
                    "Capture non supprimee du stockage (droits insuffisants ?) : %s",
                    testimonial.image.name,
                    exc_info=True,
                )

        testimonial.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = TestimonialAdminSerializer(
        testimonial,
        data=request.data,
        partial=True,
        context={'request': request},
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    serializer.save()
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def admin_testimonial_reorder(request):
    """Reordonne la liste. Corps attendu : {"order": [12, 5, 9]}."""
    ids = request.data.get('order')
    if not isinstance(ids, list) or not ids:
        return Response(
            {'order': ['Fournir la liste ordonnee des identifiants.']},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        ids = [int(value) for value in ids]
    except (TypeError, ValueError):
        return Response(
            {'order': ['Identifiants invalides.']},
            status=status.HTTP_400_BAD_REQUEST,
        )

    existing = set(Testimonial.objects.filter(pk__in=ids).values_list('pk', flat=True))
    missing = [pk for pk in ids if pk not in existing]
    if missing:
        return Response(
            {'order': [f'Identifiants inconnus : {missing}.']},
            status=status.HTTP_400_BAD_REQUEST,
        )

    for position, pk in enumerate(ids):
        Testimonial.objects.filter(pk=pk).update(ordre=position)

    queryset = Testimonial.objects.all().order_by('ordre', '-date_creation')
    serializer = TestimonialAdminSerializer(queryset, many=True, context={'request': request})
    return Response(serializer.data)
