"""
User Profile Serializers - Professional Implementation
====================================================

Clean, maintainable user profile serializers with DRY principles
and comprehensive validation.

Classes:
    - UserBaseSerializer: Core user data
    - UserDetailSerializer: Complete user information
    - UserUpdateSerializer: Profile modification
"""

from rest_framework import serializers
from ..models import CustomUser, UserNotification
from pays.serializers import NiveauSerializer, PaysSerializer


class UserBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer for essential user information.
    
    Provides core user data with computed fields and clean structure.
    Used as foundation for other user serializers.
    """
    
    full_name = serializers.ReadOnlyField(
        help_text="User's complete name (computed field)"
    )
    level = serializers.SerializerMethodField(read_only=True, help_text="Computed level from XP")
    xp_to_next = serializers.SerializerMethodField(read_only=True, help_text="XP needed to reach next level")
    
    class Meta:
        model = CustomUser
        fields = [
            'id',
            'email', 
            'first_name', 
            'last_name', 
            'full_name',
            'role',
            'civilite',
            'date_naissance',
            'telephone',
            'is_active',
            'is_staff',
            'xp',
            'streak',
            'level',
            'xp_to_next'
        ]
        read_only_fields = ['id', 'email', 'is_active', 'is_staff']
        extra_kwargs = {
            'first_name': {'help_text': 'User first name'},
            'last_name': {'help_text': 'User last name'},
            'civilite': {'help_text': 'User civility (M/Mme)'},
            'date_naissance': {'help_text': 'User birth date'},
            'telephone': {'help_text': 'User phone number'},
        }

    @staticmethod
    def _compute_level_and_next(xp: int):
        # Palier simple: lvl n atteint à 10*n XP total
        safe_xp = max(0, int(xp or 0))
        level = safe_xp // 10
        next_threshold = (level + 1) * 10
        xp_to_next = max(0, next_threshold - safe_xp)
        return level, xp_to_next

    def get_level(self, obj):
        level, _ = self._compute_level_and_next(getattr(obj, 'xp', 0))
        return level

    def get_xp_to_next(self, obj):
        _, xp_to_next = self._compute_level_and_next(getattr(obj, 'xp', 0))
        return xp_to_next


class UserDetailSerializer(UserBaseSerializer):
    """
    Detailed user serializer with geographic and educational information.
    
    Extends base serializer with country and education level data.
    Optimized with select_related for performance.
    """
    
    pays = PaysSerializer(
        read_only=True,
        help_text="User's country information"
    )
    niveau_pays = NiveauSerializer(
        read_only=True,
        help_text="User's education level"
    )
    
    class Meta(UserBaseSerializer.Meta):
        fields = UserBaseSerializer.Meta.fields + [
            'pays',
            'niveau_pays', 
            'date_joined'
        ]
        read_only_fields = UserBaseSerializer.Meta.read_only_fields + [
            'date_joined'
        ]


class UserUpdateSerializer(serializers.ModelSerializer):
    """
    Professional user profile update serializer.
    
    Features:
        - Validates geographic data consistency
        - Clean error messages
        - Secure field filtering
    """
    
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'last_name',
            'civilite',
            'date_naissance',
            'telephone',
            'role',
            'pays',
            'niveau_pays'
        ]
        extra_kwargs = {
            'first_name': {
                'required': False,
                'help_text': 'User first name'
            },
            'last_name': {
                'required': False,
                'help_text': 'User last name'
            },
            'civilite': {
                'required': False,
                'help_text': 'User civility (M/Mme)'
            },
            'date_naissance': {
                'required': False,
                'help_text': 'User birth date'
            },
            'telephone': {
                'required': False,
                'help_text': 'User phone number'
            },
            'role': {
                'required': False,
                'help_text': "User role: 'student' or 'parent'"
            },
            'pays': {
                'required': False,
                'help_text': 'User country'
            },
            'niveau_pays': {
                'required': False,
                'help_text': 'Education level (must match selected country)'
            },
        }

    def validate_role(self, value: str):
        """Validate role is one of allowed choices."""
        if value is None:
            return value
        normalized = str(value).strip().lower()
        if normalized not in ('student', 'parent'):
            raise serializers.ValidationError("Rôle invalide. Utilisez 'student' ou 'parent'.")
        return normalized

    def validate_first_name(self, value):
        """Validate first name format."""
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Le prénom doit contenir au moins 2 caractères."
            )
        return value.strip() if value else value

    def validate_last_name(self, value):
        """Validate last name format."""
        if value and len(value.strip()) < 2:
            raise serializers.ValidationError(
                "Le nom doit contenir au moins 2 caractères."
            )
        return value.strip() if value else value

    def validate(self, data):
        """
        Cross-field validation for geographic consistency.
        
        Ensures that the selected education level is available
        in the chosen country.
        """
        pays = data.get('pays')
        niveau_pays = data.get('niveau_pays')
        
        # If both are provided, validate consistency
        if pays and niveau_pays:
            if niveau_pays.pays != pays:
                raise serializers.ValidationError({
                    'niveau_pays': (
                        'Le niveau sélectionné ne correspond pas au pays choisi. '
                        f'Ce niveau appartient à {niveau_pays.pays.nom}.'
                    )
                })
        
        # If only niveau_pays is provided, auto-set pays
        elif niveau_pays and not pays:
            data['pays'] = niveau_pays.pays
        
        return data

    def update(self, instance, validated_data):
        """
        Update user with geographic validation.
        
        Automatically handles country changes and education level
        compatibility checks.
        """
        pays = validated_data.get('pays')
        niveau_pays = validated_data.get('niveau_pays')
        
        # If changing country, validate education level compatibility
        if pays and pays != instance.pays:
            if instance.niveau_pays and instance.niveau_pays.pays != pays:
                # Reset education level if incompatible with new country
                instance.niveau_pays = None
                
        # Apply updates
        for field, value in validated_data.items():
            setattr(instance, field, value)
        
        instance.save()
        return instance


class UserSummarySerializer(serializers.ModelSerializer):
    """
    Lightweight user serializer for lists and references.
    
    Minimal fields for performance in large datasets.
    """
    
    full_name = serializers.ReadOnlyField()
    
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'full_name', 'is_active']
        read_only_fields = fields


# Professional aliases for consistency
UserSerializer = UserDetailSerializer  # Main user serializer
UserSerializerWithNiveau = UserDetailSerializer  # Compatibility alias


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = ['id', 'type', 'title', 'message', 'data', 'read', 'created_at']
