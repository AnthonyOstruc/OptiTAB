"""
SERIALIZERS ULTRA SIMPLES pour exercices
"""
from rest_framework import serializers
from .models import Matiere, Theme, Notion, Chapitre, Exercice, MatiereContexte, ExerciceImage
from pays.models import Niveau


class MatiereSerializer(serializers.ModelSerializer):
    # Compteurs supprimés avec la fin des M2M
    
    class Meta:
        model = Matiere
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Alias 'nom' pour compatibilité frontend admin
        data['nom'] = data.get('titre')
        return data


class MatiereContexteSerializer(serializers.ModelSerializer):
    matiere_nom = serializers.CharField(source='matiere.titre', read_only=True)
    pays = serializers.SerializerMethodField()

    class Meta:
        model = MatiereContexte
        fields = ['id', 'matiere', 'matiere_nom', 'niveau', 'pays', 'titre', 'description', 'ordre', 'est_actif', 'couleur', 'svg_icon', 'date_creation', 'date_modification']
        extra_kwargs = {
            'titre': {'required': False, 'allow_blank': True},
            'description': {'required': False, 'allow_blank': True},
            'couleur': {'required': False},
            'svg_icon': {'required': False, 'allow_blank': True},
            'ordre': {'required': False},
            'est_actif': {'required': False},
        }

    def get_pays(self, obj):
        p = getattr(obj.niveau, 'pays', None)
        if not p:
            return None
        return {
            'id': p.id,
            'nom': p.nom,
            'drapeau_emoji': getattr(p, 'drapeau_emoji', '') or ''
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Enrichir le champ niveau avec ses métadonnées (id, nom)
        try:
            data['niveau'] = {
                'id': instance.niveau.id,
                'nom': instance.niveau.nom,
            }
        except Exception:
            pass
        return data

    def create(self, validated_data):
        # Auto-générer un titre si non fourni: "{Matiere} ({Pays}, {Niveau})"
        matiere = validated_data.get('matiere')
        niveau = validated_data.get('niveau')
        titre = validated_data.get('titre')
        if not titre:
            matiere_nom = getattr(matiere, 'titre', None)
            pays_nom = getattr(getattr(niveau, 'pays', None), 'nom', None)
            niveau_nom = getattr(niveau, 'nom', None)
            parts = [p for p in [matiere_nom, f"({pays_nom}, {niveau_nom})" if pays_nom and niveau_nom else None] if p]
            validated_data['titre'] = ' '.join(parts) if parts else 'Contexte'
        return super().create(validated_data)


class ThemeSerializer(serializers.ModelSerializer):
    notion_count = serializers.IntegerField(read_only=True)
    # Champ niveaux supprimé
    contexte = serializers.PrimaryKeyRelatedField(queryset=MatiereContexte.objects.all(), required=False, allow_null=True)
    contexte_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Theme
        fields = '__all__'

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Alias 'nom' pour compatibilité frontend admin
        data['nom'] = data.get('titre')
        # S'assurer que notion_count existe dans la réponse
        if 'notion_count' not in data:
            data['notion_count'] = getattr(instance, 'notion_count', 0) or 0
        data['contexte_detail'] = self.get_contexte_detail(instance)
        return data

    def create(self, validated_data):
        # Auto-déduire la matière depuis le contexte si fournie
        contexte = validated_data.get('contexte')
        if contexte and not validated_data.get('matiere'):
            validated_data['matiere'] = contexte.matiere
        obj = super().create(validated_data)
        return obj

    def update(self, instance, validated_data):
        contexte = validated_data.get('contexte')
        if contexte and not validated_data.get('matiere'):
            validated_data['matiere'] = contexte.matiere
        obj = super().update(instance, validated_data)
        return obj

    def get_contexte_detail(self, instance):
        c = getattr(instance, 'contexte', None)
        if not c:
            return None
        return MatiereContexteSerializer(c).data


class NotionSerializer(serializers.ModelSerializer):
    # niveaux supprimé
    matiere = serializers.SerializerMethodField()
    matiere_nom = serializers.SerializerMethodField()
    theme_nom = serializers.SerializerMethodField()
    theme_couleur = serializers.SerializerMethodField()
    contexte_detail = serializers.SerializerMethodField()
    # Détails imbriqués pour le frontend admin
    theme_detail = serializers.SerializerMethodField(read_only=True)
    matiere_detail = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Notion
        fields = '__all__'

    def get_matiere(self, obj):
        return obj.theme.matiere_id if obj.theme and obj.theme.matiere_id else None

    def get_matiere_nom(self, obj):
        return obj.theme.matiere.titre if obj.theme and obj.theme.matiere else None

    def get_theme_nom(self, obj):
        return obj.theme.titre if obj.theme else None

    def get_theme_couleur(self, obj):
        return getattr(obj.theme, 'couleur', None)

    def get_contexte_detail(self, obj):
        try:
            contexte = getattr(obj.theme, 'contexte', None)
            if not contexte:
                return None
            return MatiereContexteSerializer(contexte).data
        except Exception:
            return None

    def get_theme_detail(self, obj):
        theme = getattr(obj, 'theme', None)
        if not theme:
            return None
        matiere = getattr(theme, 'matiere', None)
        return {
            'id': theme.id,
            'titre': theme.titre,
            'matiere': (
                {'id': matiere.id, 'titre': getattr(matiere, 'titre', None)} if matiere else None
            )
        }

    def get_matiere_detail(self, obj):
        theme = getattr(obj, 'theme', None)
        matiere = getattr(theme, 'matiere', None) if theme else None
        if not matiere:
            return None
        return {'id': matiere.id, 'titre': matiere.titre}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Alias cohérents avec l'admin
        data['nom'] = data.get('titre')
        return data

    def create(self, validated_data):
        obj = super().create(validated_data)
        return obj

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)
        return obj


class ChapitreSerializer(serializers.ModelSerializer):
    notion_detail = serializers.SerializerMethodField(read_only=True)
    theme_detail = serializers.SerializerMethodField(read_only=True)
    matiere_detail = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Chapitre
        fields = '__all__'
        extra_kwargs = {
            'contenu': {'required': False, 'allow_blank': True, 'default': ''},
            'difficulty': {'required': False}
        }

    def get_notion_detail(self, obj):
        if not obj.notion:
            return None
        return {
            'id': obj.notion.id,
            'titre': obj.notion.titre,
            'theme': self.get_theme_detail(obj)
        }
    
    def get_theme_detail(self, obj):
        if not obj.notion or not obj.notion.theme:
            return None
        return {
            'id': obj.notion.theme.id,
            'titre': obj.notion.theme.titre,
            'matiere': self.get_matiere_detail(obj)
        }
    
    def get_matiere_detail(self, obj):
        if not obj.notion or not obj.notion.theme or not obj.notion.theme.matiere:
            return None
        return {
            'id': obj.notion.theme.matiere.id,
            'nom': obj.notion.theme.matiere.titre
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Alias 'nom' pour compatibilité frontend admin
        data['nom'] = data.get('titre')
        return data


class ExerciceSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Exercice
        fields = '__all__'

    def get_images(self, obj):
        qs = getattr(obj, 'images', None)
        if qs is None:
            return []
        return [
            {
                'id': img.id,
                'image': img.image.url if getattr(img.image, 'url', None) else '',
                'image_type': img.image_type,
                'position': img.position,
                'legende': img.legende,
            }
            for img in qs.all().order_by('position', 'id')
        ]


class ExerciceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciceImage
        fields = '__all__'
        extra_kwargs = {
            'legende': {'required': False, 'allow_blank': True},
            'position': {'required': False},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['nom'] = data.get('titre')
        return data