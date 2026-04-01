"""
VUES ULTRA SIMPLES pour cours
"""
import os
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated

from subscriptions.permissions import (
    HasActiveSubscriptionOrPass,
    get_content_niveau,
    is_demo_content,
    user_has_active_subscription_or_pass,
)
from .models import Cours, CoursImage
from .serializers import CoursSerializer, CoursImageSerializer
from .services import (
    CoursePdfGenerationError,
    build_course_pdf_filename,
    render_course_pdf_bytes,
    render_course_pdf_html,
)


class CoursViewSet(viewsets.ModelViewSet):
    queryset = Cours.objects.all()
    serializer_class = CoursSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscriptionOrPass]

    def get_permissions(self):
        if self.action in ('list', 'retrieve', 'pdf_draft_preview', 'pdf_draft_download'):
            return [IsAuthenticated()]
        return [IsAuthenticated(), HasActiveSubscriptionOrPass()]

    @staticmethod
    def _is_admin_user(user):
        return bool(user and user.is_authenticated and (user.is_staff or user.is_superuser))

    def _require_admin(self, request):
        if not self._is_admin_user(getattr(request, "user", None)):
            self.permission_denied(
                request,
                message="Acces reserve aux administrateurs.",
            )

    def _build_draft_course_from_payload(self, request):
        payload = request.data or {}
        raw_content = payload.get("contenu") or payload.get("content") or payload.get("source") or ""
        source_content = str(raw_content or "")
        if not source_content.strip():
            raise ValidationError({"detail": "Le contenu du cours est vide."})

        raw_title = payload.get("titre") or payload.get("title") or ""
        title = str(raw_title or "").strip()

        raw_difficulty = payload.get("difficulty") or payload.get("difficulte") or "medium"
        difficulty = str(raw_difficulty or "medium").strip().lower()
        if difficulty not in {"easy", "medium", "hard"}:
            difficulty = "medium"

        return Cours(titre=title, contenu=source_content, difficulty=difficulty)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Bypass subscription check for demo content
        if not user_has_active_subscription_or_pass(
            request.user,
            niveau=get_content_niveau(instance),
        ):
            if not is_demo_content(request.user, 'cours', instance):
                self.permission_denied(request, message=HasActiveSubscriptionOrPass.message)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get_serializer_context(self):
        # Injecter la requête pour construire des URLs absolues dans le serializer
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def get_queryset(self):
        queryset = super().get_queryset()
        # Nouveau filtrage direct par notion (suppression des chapitres)
        notion = self.request.query_params.get('notion')
        matiere = self.request.query_params.get('matiere')
        search = self.request.query_params.get('search') or self.request.query_params.get('q')

        if notion:
            queryset = queryset.filter(notion_id=notion)
        if matiere:
            # Joindre via Notion -> Theme -> Matiere
            queryset = queryset.select_related('notion', 'notion__theme', 'notion__theme__matiere')
            queryset = queryset.filter(notion__theme__matiere_id=matiere)

        if search:
            queryset = queryset.filter(titre__icontains=search)

        return queryset.filter(est_actif=True).select_related('notion', 'notion__theme', 'notion__theme__matiere').order_by('ordre', 'id')

    def list(self, request, *args, **kwargs):
        """Pagination légère pour l'admin via ?limit=5&offset=0."""
        queryset = self.filter_queryset(self.get_queryset())

        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset', 0)

        if limit is not None:
            try:
                limit_value = int(limit)
                offset_value = int(offset or 0)
                if limit_value <= 0 or offset_value < 0:
                    raise ValueError
            except ValueError:
                return Response({'detail': 'Paramètres de pagination invalides'}, status=status.HTTP_400_BAD_REQUEST)

            total = queryset.count()
            serializer = self.get_serializer(queryset[offset_value:offset_value + limit_value], many=True)
            return Response({
                'count': total,
                'limit': limit_value,
                'offset': offset_value,
                'results': serializer.data
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='pdf-draft-preview')
    def pdf_draft_preview(self, request, *args, **kwargs):
        """Prévisualisation HTML d'un cours collé/importé (sans sauvegarde DB)."""
        self._require_admin(request)
        try:
            draft_course = self._build_draft_course_from_payload(request)
            preview_html = render_course_pdf_html(draft_course, request=request)
        except ValidationError:
            raise
        except Exception as exc:
            return Response(
                {"detail": f"Erreur generation preview: {exc}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(
            {
                "html": preview_html,
                "filename": build_course_pdf_filename(draft_course),
            }
        )

    @action(detail=False, methods=['post'], url_path='pdf-draft-download')
    def pdf_draft_download(self, request, *args, **kwargs):
        """Génère et renvoie un PDF natif d'un cours collé/importé (sans sauvegarde DB)."""
        self._require_admin(request)

        try:
            draft_course = self._build_draft_course_from_payload(request)
            pdf_bytes = render_course_pdf_bytes(draft_course, request=request)
        except ValidationError:
            raise
        except CoursePdfGenerationError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        except Exception as exc:
            return Response(
                {"detail": f"Erreur generation PDF: {exc}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        requested_filename = str(request.data.get("filename") or "").strip()
        filename = requested_filename or build_course_pdf_filename(draft_course)

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        response["Cache-Control"] = "no-store"
        return response


class CoursImageViewSet(viewsets.ModelViewSet):
    """CRUD pour les images de cours

    Frontend attend /api/cours/cours-images/ avec filtre ?cours=<id>
    """
    queryset = CoursImage.objects.all()
    serializer_class = CoursImageSerializer
    permission_classes = [IsAuthenticated, HasActiveSubscriptionOrPass]

    def get_permissions(self):
        if self.action in ("list", "retrieve"):
            return [IsAuthenticated()]
        return [IsAuthenticated(), HasActiveSubscriptionOrPass()]

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['request'] = self.request
        return ctx

    def get_queryset(self):
        queryset = super().get_queryset()
        cours_id = self.request.query_params.get('cours')
        if cours_id:
            queryset = queryset.filter(cours_id=cours_id)

        user = getattr(self.request, "user", None)
        if user and user.is_authenticated and not (user.is_staff or user.is_superuser):
            if not user_has_active_subscription_or_pass(user, niveau=getattr(user, "niveau_pays", None)):
                demo_notion_id = getattr(getattr(user, "niveau_pays", None), "demo_notion_id", None)
                if not demo_notion_id:
                    return queryset.none()
                queryset = queryset.filter(cours__notion_id=demo_notion_id)

        return queryset.order_by('position', 'id')

    @action(detail=False, methods=['post'], url_path='duplicate')
    def duplicate_images(self, request, *args, **kwargs):
        source_cours_id = request.data.get('source_cours')
        target_cours_id = request.data.get('target_cours')
        replace_existing = bool(request.data.get('replace_existing'))

        if not source_cours_id or not target_cours_id:
            return Response(
                {'detail': 'source_cours et target_cours sont requis'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            source_cours = Cours.objects.get(pk=source_cours_id)
            target_cours = Cours.objects.get(pk=target_cours_id)
        except Cours.DoesNotExist:
            return Response({'detail': 'Cours introuvable'}, status=status.HTTP_404_NOT_FOUND)

        if replace_existing:
            target_cours.images.all().delete()

        duplicated = 0
        for img in source_cours.images.all().order_by('position', 'id'):
            if not img.image:
                continue
            new_image = CoursImage(
                cours=target_cours,
                image_type=img.image_type,
                position=img.position,
                legende=img.legende,
                alt_text=img.alt_text,
                title_text=img.title_text,
                width=img.width,
                height=img.height,
            )
            try:
                with img.image.open('rb') as original_file:
                    filename = os.path.basename(img.image.name or f'cours-image-{img.id}')
                    new_image.image.save(filename, ContentFile(original_file.read()), save=False)
                new_image.save()
                duplicated += 1
            except Exception:  # pragma: no cover - ignorer les erreurs individuelles
                continue

        serializer = self.get_serializer(
            target_cours.images.all().order_by('position', 'id'),
            many=True
        )
        return Response({'duplicated': duplicated, 'images': serializer.data})
