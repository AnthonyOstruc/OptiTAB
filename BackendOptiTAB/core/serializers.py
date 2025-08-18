"""
Core serializers providing base functionality and common patterns.
"""
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base serializer with common functionality for all model serializers.
    """
    
    def validate_positive_integer(self, value, field_name):
        """
        Common validation for positive integer fields.
        """
        if value is not None and value < 0:
            raise serializers.ValidationError(
                _(f"{field_name} doit être un nombre positif.")
            )
        return value


class TimestampedSerializer(BaseModelSerializer):
    """
    Serializer mixin for timestamped models.
    Automatically includes formatted dates.
    """
    date_creation_formatted = serializers.SerializerMethodField()
    date_modification_formatted = serializers.SerializerMethodField()

    def get_date_creation_formatted(self, obj):
        """Return formatted creation date."""
        if obj.date_creation:
            return obj.date_creation.strftime("%d/%m/%Y %H:%M")
        return None

    def get_date_modification_formatted(self, obj):
        """Return formatted modification date."""
        if obj.date_modification:
            return obj.date_modification.strftime("%d/%m/%Y %H:%M")
        return None


class ActiveFieldMixin:
    """
    Mixin for serializers handling active/inactive status.
    """
    
    def validate_est_actif(self, value):
        """
        Validation for active field.
        """
        # Add any business logic for activation/deactivation
        return value


class DifficultyFieldMixin:
    """
    Mixin for serializers handling difficulty levels.
    """
    
    def validate_difficulty(self, value):
        """
        Validation for difficulty field.
        """
        valid_choices = ['easy', 'medium', 'hard']
        if value not in valid_choices:
            raise serializers.ValidationError(
                _("Difficulté invalide. Choix disponibles: {}").format(', '.join(valid_choices))
            )
        return value


class BaseContentSerializer(TimestampedSerializer, ActiveFieldMixin):
    """
    Base serializer for content models.
    """
    
    def validate_titre(self, value):
        """
        Validation for title field.
        """
        if not value or not value.strip():
            raise serializers.ValidationError(_("Le titre ne peut pas être vide."))
        
        if len(value.strip()) < 2:
            raise serializers.ValidationError(_("Le titre doit contenir au moins 2 caractères."))
        
        return value.strip()

    def validate_ordre(self, value):
        """
        Validation for order field.
        """
        return self.validate_positive_integer(value, "ordre")


class BaseEducationalSerializer(BaseContentSerializer, DifficultyFieldMixin):
    """
    Base serializer for educational content.
    """
    
    def validate_contenu(self, value):
        """
        Validation for content field.
        """
        if not value or not value.strip():
            raise serializers.ValidationError(_("Le contenu ne peut pas être vide."))
        
        if len(value.strip()) < 10:
            raise serializers.ValidationError(_("Le contenu doit contenir au moins 10 caractères."))
        
        return value.strip()


class ListSerializer(BaseModelSerializer):
    """
    Optimized serializer for list views with minimal fields.
    """
    
    def to_representation(self, instance):
        """
        Customize representation for list views.
        """
        data = super().to_representation(instance)
        
        # Remove null values to reduce payload size
        return {k: v for k, v in data.items() if v is not None}


class DetailSerializer(BaseModelSerializer):
    """
    Comprehensive serializer for detail views with all fields.
    """
    pass


class WriteSerializer(BaseModelSerializer):
    """
    Serializer optimized for write operations (create/update).
    """
    
    def create(self, validated_data):
        """
        Override create method with common logic.
        """
        # Add any common creation logic here
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        """
        Override update method with common logic.
        """
        # Add any common update logic here
        return super().update(instance, validated_data)
