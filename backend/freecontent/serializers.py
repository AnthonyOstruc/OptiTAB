import re
from rest_framework import serializers

from .models import FreeLearningResource


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
