import re
from rest_framework import serializers
from django.utils.text import slugify

from .models import FreeLearningResource
from synthesis.models import SynthesisSheet
from cours.utils import build_course_image_payload, resolve_course_title
from curriculum.utils import build_exercice_image_payload, resolve_exercice_title


def build_seo_prefixed_slug(prefix, object_id, *, pays='', niveau='', matiere='', titre='', max_length=140):
    """
    Construit un slug SEO stable sous la forme:
      <prefix>-<id>-<pays>-<niveau>-<matiere>-<titre>

    L'ID est toujours présent pour garder une URL stable et permettre
    une résolution robuste côté API même si le titre change.
    """
    base = f"{prefix}-{object_id}"

    def norm(value):
        raw = str(value or '').strip()
        if not raw:
            return ''
        return slugify(raw)  # ASCII, minuscules, tirets

    pays_slug = norm(pays)
    niveau_slug = norm(niveau)
    matiere_slug = norm(matiere)
    titre_slug = norm(titre)

    # Dédupliquer en conservant l'ordre
    parts = []
    for part in (pays_slug, niveau_slug, matiere_slug, titre_slug):
        if not part:
            continue
        if part in parts:
            continue
        parts.append(part)

    if not parts:
        return base

    full = f"{base}-{'-'.join(parts)}"
    if len(full) <= max_length:
        return full

    # Si trop long: on garde base + (pays/niveau/matiere) et on tronque le titre en priorité.
    keep_unique = []
    for part in (pays_slug, niveau_slug, matiere_slug):
        if part and part not in keep_unique:
            keep_unique.append(part)

    prefix_part = f"{base}-{'-'.join(keep_unique)}" if keep_unique else base

    if not titre_slug:
        return prefix_part[:max_length].rstrip('-')

    available = max_length - len(prefix_part) - 1
    if available <= 10:
        # Trop serré: retirer des éléments moins importants (matiere puis pays puis niveau) pour libérer de la place
        reduced_keep = keep_unique[:]
        for drop in (matiere_slug, pays_slug, niveau_slug):
            if available > 10:
                break
            if drop and drop in reduced_keep:
                reduced_keep.remove(drop)
            prefix_part = f"{base}-{'-'.join(reduced_keep)}" if reduced_keep else base
            available = max_length - len(prefix_part) - 1

    if available <= 0:
        return base[:max_length].rstrip('-')

    trimmed_title = titre_slug[:available].rstrip('-')
    if not trimmed_title:
        return prefix_part[:max_length].rstrip('-')

    return f"{prefix_part}-{trimmed_title}"


class FreeLearningResourceSerializer(serializers.ModelSerializer):
    matiere_nom = serializers.CharField(source='matiere.titre', read_only=True)
    niveau_nom = serializers.CharField(source='niveau.nom', read_only=True)
    pays_nom = serializers.CharField(source='niveau.pays.nom', read_only=True)
    notion_nom = serializers.CharField(source='notion.titre', read_only=True)
    type_label = serializers.CharField(read_only=True)
    theme_id = serializers.SerializerMethodField()
    theme_nom = serializers.SerializerMethodField()

    class Meta:
        model = FreeLearningResource
        fields = [
            'id',
            'slug',
            'titre',
            'accroche',
            'resource_type',
            'type_label',
            'excerpt',
            'contenu_html',
            'cover_image',
            'badge',
            'lecture_duree',
            'tag_secondaire',
            'matiere',
            'matiere_nom',
            'niveau',
            'niveau_nom',
            'pays_nom',
            'notion',
            'notion_nom',
            'theme_id',
            'theme_nom',
            'ordre',
            'est_actif',
            'est_publie',
            'date_creation',
            'date_modification',
        ]
        read_only_fields = [
            'slug',
            'date_creation',
            'date_modification',
        ]

    def get_theme_id(self, obj):
        theme = getattr(getattr(obj, 'notion', None), 'theme', None)
        return getattr(theme, 'id', None)

    def get_theme_nom(self, obj):
        theme = getattr(getattr(obj, 'notion', None), 'theme', None)
        return getattr(theme, 'titre', None)


class CourseFreePreviewSerializer(serializers.Serializer):
    """Sérialise un objet Cours en carte 'ressource gratuite'."""

    def to_representation(self, cours):
        notion = getattr(cours, 'notion', None)
        theme = getattr(notion, 'theme', None)
        matiere = getattr(theme, 'matiere', None)
        contexte = getattr(theme, 'contexte', None)
        niveau = getattr(contexte, 'niveau', None) if contexte else None
        pays = getattr(niveau, 'pays', None) if niveau else None

        titre = cours.titre or getattr(notion, 'titre', 'Cours OptiTAB')
        accroche = getattr(notion, 'description', '') or ''
        raw_content = getattr(cours, 'contenu', '')
        excerpt = accroche or self._build_excerpt(raw_content)
        badge = self._badge_for_scope(cours)
        images = getattr(cours, 'images', None)
        image_data = []
        request = self.context.get('request') if hasattr(self, 'context') else None
        include_images = bool(self.context.get('include_images', True)) if hasattr(self, 'context') else True
        course_title = resolve_course_title(cours) or titre
        if include_images and images is not None:
            for img in images.all().order_by('position', 'id'):
                image_data.append(
                    build_course_image_payload(
                        img,
                        request=request,
                        course_title=course_title
                    )
                )

        return {
            'id': cours.id,
            'slug': build_seo_prefixed_slug(
                'cours-gratuit',
                cours.id,
                pays=getattr(pays, 'nom', ''),
                niveau=getattr(niveau, 'nom', ''),
                matiere=getattr(matiere, 'titre', ''),
                titre=titre
            ),
            'titre': titre,
            'accroche': accroche[:160],
            'resource_type': FreeLearningResource.TYPE_COURSE,
            'type_label': 'Cours',
            'access_scope': cours.access_scope,
            'is_locked': cours.access_scope == cours.ACCESS_SCOPE_PAID,
            'excerpt': excerpt,
            'contenu_html': '',
            'contenu': raw_content,
            'images': image_data,
            'video_url': getattr(cours, 'video_url', ''),
            'pdf_url': self._safe_file_url(getattr(cours, 'pdf_file', None)),
            'cover_image': '',
            'badge': badge,
            'lecture_duree': self._estimate_read_time(getattr(cours, 'contenu', '')),
            'tag_secondaire': getattr(niveau, 'nom', '') or getattr(matiere, 'titre', ''),
            'matiere': getattr(matiere, 'id', None),
            'matiere_nom': getattr(matiere, 'titre', ''),
            'niveau': getattr(niveau, 'id', None),
            'niveau_nom': getattr(niveau, 'nom', ''),
            'pays_nom': getattr(pays, 'nom', ''),
            'notion': getattr(notion, 'id', None),
            'notion_nom': getattr(notion, 'titre', ''),
            'theme_id': getattr(theme, 'id', None),
            'theme_nom': getattr(theme, 'titre', ''),
            'ordre': cours.ordre,
            'est_actif': cours.est_actif,
            'est_publie': True,
            'date_creation': cours.date_creation,
            'date_modification': cours.date_modification,
        }

    @staticmethod
    def _badge_for_scope(cours):
        if getattr(cours, 'access_scope', '') == cours.ACCESS_SCOPE_BOTH:
            return 'Gratuit + Premium'
        if getattr(cours, 'access_scope', '') == cours.ACCESS_SCOPE_FREE:
            return 'Gratuit'
        if getattr(cours, 'access_scope', '') == cours.ACCESS_SCOPE_PAID:
            return 'Premium'
        return ''

    @staticmethod
    def _build_excerpt(content):
        text = re.sub(r'<[^>]+>', ' ', content or '')
        text = text.replace('\n', ' ').strip()
        while '  ' in text:
            text = text.replace('  ', ' ')
        if len(text) <= 220:
            return text
        trimmed = text[:220].rsplit(' ', 1)[0]
        return f"{trimmed}..."

    @staticmethod
    def _estimate_read_time(content):
        words = len((content or '').split())
        if words == 0:
            return ''
        minutes = max(1, int((words + 179) / 180))
        return f"~{minutes} min"

    @staticmethod
    def _safe_file_url(file_field):
        if not file_field:
            return ''
        try:
            return file_field.url
        except Exception:
            return ''


class ExerciceFreePreviewSerializer(serializers.Serializer):
    """Serialize un exercice gratuit en vignette."""

    def to_representation(self, exercice):
        notion = getattr(exercice, 'notion', None)
        theme = getattr(notion, 'theme', None)
        contexte = getattr(theme, 'contexte', None)
        niveau = getattr(contexte, 'niveau', None) if contexte else None
        matiere = getattr(theme, 'matiere', None)
        pays = getattr(niveau, 'pays', None) if niveau else None

        accroche = exercice.question or exercice.contenu or ''
        excerpt = accroche[:220]
        images = getattr(exercice, 'images', None)
        image_data = []
        request = self.context.get('request') if hasattr(self, 'context') else None
        include_images = bool(self.context.get('include_images', True)) if hasattr(self, 'context') else True
        exercice_title = resolve_exercice_title(exercice) or (exercice.titre or '')
        if include_images and images is not None:
            for img in images.all().order_by('position', 'id'):
                image_data.append(
                    build_exercice_image_payload(
                        img,
                        request=request,
                        exercice_title=exercice_title
                    )
                )
        cover_image = image_data[0]['image'] if image_data else ''

        return {
            'id': exercice.id,
            'slug': build_seo_prefixed_slug(
                'exercice-gratuit',
                exercice.id,
                pays=getattr(pays, 'nom', ''),
                niveau=getattr(niveau, 'nom', ''),
                matiere=getattr(matiere, 'titre', ''),
                titre=(exercice.titre or (notion.titre if notion else 'Exercice OptiTAB'))
            ),
            'titre': exercice.titre or (notion.titre if notion else 'Exercice OptiTAB'),
            'accroche': accroche[:160],
            'resource_type': FreeLearningResource.TYPE_EXERCISE,
            'type_label': 'Exercice',
            'access_scope': exercice.access_scope,
            'is_locked': exercice.access_scope == getattr(exercice, 'ACCESS_SCOPE_PAID', 'paid'),
            'excerpt': excerpt,
            'contenu_html': '',
            'contenu': exercice.contenu or '',
            'question': exercice.question or '',
            'solution': exercice.reponse_correcte or '',
            'etapes': exercice.etapes or '',
            'images': image_data,
            'difficulty': getattr(exercice, 'difficulty', '') or '',
            'cover_image': cover_image,
            'badge': self._safe_badge(exercice),
            'lecture_duree': self._estimate_read_time(accroche),
            'tag_secondaire': getattr(niveau, 'nom', '') or getattr(matiere, 'titre', ''),
            'matiere': getattr(matiere, 'id', None),
            'matiere_nom': getattr(matiere, 'titre', ''),
            'niveau': getattr(niveau, 'id', None),
            'niveau_nom': getattr(niveau, 'nom', ''),
            'pays_nom': getattr(pays, 'nom', ''),
            'notion': getattr(notion, 'id', None),
            'notion_nom': getattr(notion, 'titre', ''),
            'theme_id': getattr(theme, 'id', None),
            'theme_nom': getattr(theme, 'titre', ''),
            'ordre': exercice.ordre,
            'est_actif': exercice.est_actif,
            'est_publie': True,
            'date_creation': exercice.date_creation,
            'date_modification': exercice.date_modification,
        }

    @staticmethod
    def _estimate_read_time(content):
        words = len((content or '').split())
        if words == 0:
            return ''
        minutes = max(1, int((words + 179) / 180))
        return f"~{minutes} min"

    @staticmethod
    def _safe_badge(exercice):
        try:
            return exercice.get_difficulty_display()
        except Exception:
            return ''

class SynthesisFreePreviewSerializer(serializers.Serializer):
    """Sérialise une fiche de synthèse accessible gratuitement."""

    def to_representation(self, sheet: SynthesisSheet):
        notion = getattr(sheet, 'notion', None)
        theme = getattr(notion, 'theme', None)
        contexte = getattr(theme, 'contexte', None)
        niveau = getattr(contexte, 'niveau', None) if contexte else None
        matiere = getattr(theme, 'matiere', None)
        pays = getattr(niveau, 'pays', None) if niveau else None

        summary = sheet.summary or ''
        excerpt = summary.strip().split('\n')[0]
        if not excerpt:
            excerpt = summary[:200]

        images_payload = []
        images_qs = getattr(sheet, 'images', None)
        include_images = bool(self.context.get('include_images', True)) if hasattr(self, 'context') else True
        if include_images and images_qs is not None:
            for img in images_qs.all():
                image_url = ''
                try:
                    image_url = getattr(img.image, 'url', '') or ''
                except Exception:
                    image_url = ''
                images_payload.append({
                    'id': img.id,
                    'image': image_url,
                    'image_type': img.image_type,
                    'position': img.position,
                    'caption': img.caption,
                    'legende': img.caption,
                })

        return {
            'id': sheet.id,
            'slug': build_seo_prefixed_slug(
                'synthese-gratuite',
                sheet.id,
                pays=getattr(pays, 'nom', ''),
                niveau=getattr(niveau, 'nom', ''),
                matiere=getattr(matiere, 'titre', ''),
                titre=(sheet.titre or (notion.titre if notion else 'Synthese OptiTAB'))
            ),
            'titre': sheet.titre,
            'accroche': excerpt[:160],
            'resource_type': FreeLearningResource.TYPE_SUMMARY,
            'type_label': 'Résumé',
            'access_scope': sheet.access_scope,
            'is_locked': sheet.access_scope == SynthesisSheet.ACCESS_SCOPE_PAID,
            'excerpt': summary[:400],
            'contenu_html': '',
            'contenu': summary,
            'images': images_payload,
            'cover_image': images_payload[0]['image'] if images_payload else '',
            'badge': self._badge_for_scope(sheet),
            'lecture_duree': self._format_reading_time(sheet.reading_time_minutes, summary),
            'tag_secondaire': getattr(niveau, 'nom', '') or getattr(matiere, 'titre', ''),
            'matiere': getattr(matiere, 'id', None),
            'matiere_nom': getattr(matiere, 'titre', ''),
            'niveau': getattr(niveau, 'id', None),
            'niveau_nom': getattr(niveau, 'nom', ''),
            'pays_nom': getattr(pays, 'nom', ''),
            'notion': getattr(notion, 'id', None),
            'notion_nom': getattr(notion, 'titre', ''),
            'theme_id': getattr(theme, 'id', None),
            'theme_nom': getattr(theme, 'titre', ''),
            'ordre': sheet.ordre,
            'est_actif': sheet.est_actif,
            'est_publie': True,
            'date_creation': sheet.date_creation,
            'date_modification': sheet.date_modification,
        }

    @staticmethod
    def _badge_for_scope(sheet: SynthesisSheet):
        if getattr(sheet, 'access_scope', SynthesisSheet.ACCESS_SCOPE_PAID) == SynthesisSheet.ACCESS_SCOPE_BOTH:
            return 'Gratuit + Premium'
        if sheet.access_scope == SynthesisSheet.ACCESS_SCOPE_FREE:
            return 'Gratuit'
        return 'Premium'

    @staticmethod
    def _format_reading_time(minutes, summary):
        if minutes:
            return f"~{max(1, minutes)} min"
        words = len((summary or '').split())
        if words == 0:
            return ''
        approx = max(1, int((words + 179) / 180))
        return f"~{approx} min"


class ExerciseNotionSummarySerializer(serializers.Serializer):
    """
    Résumé par chapitre (notion) pour les exercices gratuits.
    Utilisé pour paginer par notion plutôt que par exercice.
    """

    notion = serializers.IntegerField()
    notion_nom = serializers.CharField()
    matiere_nom = serializers.CharField(required=False, allow_blank=True, default='')
    niveau_nom = serializers.CharField(required=False, allow_blank=True, default='')
    pays_nom = serializers.CharField(required=False, allow_blank=True, default='')
    tag_secondaire = serializers.CharField(required=False, allow_blank=True, default='')
    is_locked = serializers.BooleanField(default=False)
    count = serializers.IntegerField()
    resource_type = serializers.SerializerMethodField()

    def get_resource_type(self, obj):
        return getattr(FreeLearningResource, 'TYPE_EXERCISE', 'exercise')

