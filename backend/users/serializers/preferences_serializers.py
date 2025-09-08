from rest_framework import serializers
from ..models import UserFavoriteMatiere, UserSelectedMatiere
from curriculum.models import Matiere


class MatiereBasicSerializer(serializers.ModelSerializer):
    """Sérialiseur simple pour les informations de base d'une matière"""
    nom = serializers.CharField(source='titre', read_only=True)  # Mapping titre -> nom pour le frontend
    
    class Meta:
        model = Matiere
        fields = ['id', 'nom', 'svg_icon', 'description']


class UserFavoriteMatiereSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les matières favorites de l'utilisateur"""
    matiere = MatiereBasicSerializer(read_only=True)
    matiere_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserFavoriteMatiere
        fields = ['id', 'matiere', 'matiere_id', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        # Récupérer l'utilisateur connecté depuis le contexte
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def validate_matiere_id(self, value):
        """Valider que la matière existe"""
        try:
            Matiere.objects.get(id=value)
            return value
        except Matiere.DoesNotExist:
            raise serializers.ValidationError("Cette matière n'existe pas.")


class UserSelectedMatiereSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les onglets sélectionnés de l'utilisateur"""
    matiere = MatiereBasicSerializer(read_only=True)
    matiere_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = UserSelectedMatiere
        fields = ['id', 'matiere', 'matiere_id', 'order', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def create(self, validated_data):
        # Récupérer l'utilisateur connecté depuis le contexte
        user = self.context['request'].user
        validated_data['user'] = user
        return super().create(validated_data)

    def validate_matiere_id(self, value):
        """Valider que la matière existe"""
        try:
            Matiere.objects.get(id=value)
            return value
        except Matiere.DoesNotExist:
            raise serializers.ValidationError("Cette matière n'existe pas.")


class UserPreferencesSerializer(serializers.Serializer):
    """Sérialiseur pour récupérer toutes les préférences utilisateur d'un coup"""
    favorite_matieres = UserFavoriteMatiereSerializer(many=True, read_only=True)
    selected_matieres = UserSelectedMatiereSerializer(many=True, read_only=True)
    active_matiere_id = serializers.SerializerMethodField()

    def get_active_matiere_id(self, obj):
        """Récupérer l'ID de la matière active"""
        active_matiere = obj.selected_matieres.filter(is_active=True).first()
        return active_matiere.matiere.id if active_matiere else None


class BulkUpdateMatierePreferencesSerializer(serializers.Serializer):
    """Sérialiseur pour mettre à jour en masse les préférences de matières"""
    favorite_matiere_ids = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        help_text="Liste des IDs des matières favorites"
    )
    selected_matieres = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        help_text="Liste des matières sélectionnées avec leur ordre et statut actif"
    )
    active_matiere_id = serializers.IntegerField(
        required=False,
        allow_null=True,
        help_text="ID de la matière actuellement active"
    )

    def validate_favorite_matiere_ids(self, value):
        """Valider que toutes les matières favorites existent"""
        if value:
            existing_ids = set(Matiere.objects.filter(id__in=value).values_list('id', flat=True))
            invalid_ids = set(value) - existing_ids
            if invalid_ids:
                raise serializers.ValidationError(f"Ces matières n'existent pas : {invalid_ids}")
        return value

    def validate_selected_matieres(self, value):
        """Valider le format et l'existence des matières sélectionnées"""
        if not value:
            return value

        for item in value:
            # Vérifier la structure
            if not isinstance(item, dict):
                raise serializers.ValidationError("Chaque élément doit être un dictionnaire.")
            
            required_fields = ['matiere_id', 'order']
            missing_fields = [field for field in required_fields if field not in item]
            if missing_fields:
                raise serializers.ValidationError(f"Champs manquants : {missing_fields}")
            
            # Vérifier les types
            if not isinstance(item['matiere_id'], int):
                raise serializers.ValidationError("matiere_id doit être un entier.")
            if not isinstance(item['order'], int):
                raise serializers.ValidationError("order doit être un entier.")
            if 'is_active' in item and not isinstance(item['is_active'], bool):
                raise serializers.ValidationError("is_active doit être un booléen.")

        # Vérifier que toutes les matières existent
        matiere_ids = [item['matiere_id'] for item in value]
        existing_ids = set(Matiere.objects.filter(id__in=matiere_ids).values_list('id', flat=True))
        invalid_ids = set(matiere_ids) - existing_ids
        if invalid_ids:
            raise serializers.ValidationError(f"Ces matières n'existent pas : {invalid_ids}")

        return value

    def validate_active_matiere_id(self, value):
        """Valider que la matière active existe"""
        if value is not None:
            try:
                Matiere.objects.get(id=value)
                return value
            except Matiere.DoesNotExist:
                raise serializers.ValidationError("Cette matière n'existe pas.")
        return value 