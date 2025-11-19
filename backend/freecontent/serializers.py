import re
from rest_framework import serializers

from .models import FreeLearningResource
from synthesis.models import SynthesisSheet


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
        if images is not None:
            for img in images.all():
                image_url = ''
                try:
                    image_url = getattr(img.image, 'url', '') or ''
                except Exception:
                    image_url = ''
                image_data.append({
                    'id': img.id,
                    'image': image_url,
                    'image_type': img.image_type,
                    'position': img.position,
                    'legende': img.legende,
                })

        return {
            'id': cours.id,
            'slug': f'cours-gratuit-{cours.id}',
            'titre': titre,
            'accroche': accroche[:160],
            'resource_type': FreeLearningResource.TYPE_COURSE,
            'type_label': 'Cours',
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
        return 'Gratuit'

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
    """Sérialise un exercice gratuit en vignette."""

    def to_representation(self, exercice):
        notion = getattr(exercice, 'notion', None)
        theme = getattr(notion, 'theme', None)
        contexte = getattr(theme, 'contexte', None)
        niveau = getattr(contexte, 'niveau', None) if contexte else None
        matiere = getattr(theme, 'matiere', None)
        pays = getattr(niveau, 'pays', None) if niveau else None

        accroche = exercice.question or exercice.contenu or ''
        excerpt = accroche[:220]
        cover_image = self._first_image(exercice)
        images = getattr(exercice, 'images', None)
        image_data = []
        if images is not None:
            for img in images.all():
                image_url = ''
                try:
                    image_url = getattr(img.image, 'url', '') or ''
                except Exception:
                    image_url = ''
                image_data.append({
                    'id': img.id,
                    'image': image_url,
                    'image_type': img.image_type,
                    'position': img.position,
                    'legende': img.legende,
                })

        return {
            'id': exercice.id,
            'slug': f'exercice-gratuit-{exercice.id}',
            'titre': exercice.titre or (notion.titre if notion else 'Exercice OptiTAB'),
            'accroche': accroche[:160],
            'resource_type': FreeLearningResource.TYPE_EXERCISE,
            'type_label': 'Exercice',
            'excerpt': excerpt,
            'contenu_html': '',
            'contenu': exercice.contenu or '',
            'question': exercice.question or '',
            'solution': exercice.reponse_correcte or '',
            'etapes': exercice.etapes or '',
            'images': image_data,
            'difficulty': exercice.difficulty or '',
            'cover_image': cover_image,
            'badge': exercice.get_difficulty_display(),
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
    def _first_image(exercice):
        images = getattr(exercice, 'images', None)
        if not images:
            return ''
        image = images.all().order_by('position', 'id').first()
        if not image:
            return ''
        try:
            return image.image.url or ''
        except Exception:
            return ''

    @staticmethod
    def _estimate_read_time(content):
        words = len((content or '').split())
        if words == 0:
            return ''
        minutes = max(1, int((words + 179) / 180))
        return f"~{minutes} min"


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
        if images_qs is not None:
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
            'slug': f'synthese-gratuite-{sheet.id}',
            'titre': sheet.titre,
            'accroche': excerpt[:160],
            'resource_type': FreeLearningResource.TYPE_SUMMARY,
            'type_label': 'Résumé',
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
