"""
Geographic Data Serializers - Professional Implementation
========================================================

Clean serializers for managing user geographic and educational data
with comprehensive validation and country/education level coordination.

Classes:
    - UserGeographicUpdateSerializer: Handles country and education level updates
"""

from rest_framework import serializers
from ..models import CustomUser
from pays.models import Pays, Niveau


class UserGeographicUpdateSerializer(serializers.ModelSerializer):
    """
    Professional serializer for user geographic and educational data updates.
    
    Features:
        - Validates country and education level compatibility
        - Handles automatic country assignment from education level
        - Clean error messages with helpful context
        - Atomic updates with rollback on validation errors
    """
    
    pays_id = serializers.IntegerField(
        write_only=True, 
        required=False,
        help_text="Country ID for user's geographic location"
    )
    niveau_pays_id = serializers.IntegerField(
        write_only=True, 
        required=False,
        help_text="Education level ID (must be compatible with selected country)"
    )
    
    class Meta:
        model = CustomUser
        fields = [
            'pays', 
            'niveau_pays', 
            'pays_id', 
            'niveau_pays_id'
        ]
        extra_kwargs = {
            'pays': {'read_only': True},
            'niveau_pays': {'read_only': True},
        }

    def validate_pays_id(self, value):
        """Validate country exists and is active."""
        if value is not None:
            try:
                pays = Pays.objects.get(id=value, est_actif=True)
                return pays
            except Pays.DoesNotExist:
                raise serializers.ValidationError(
                    f"Pays avec l'ID {value} introuvable ou inactif."
                )
        return None

    def validate_niveau_pays_id(self, value):
        """Validate education level exists and is active."""
        if value is not None:
            try:
                niveau = Niveau.objects.get(id=value, est_actif=True)
                return niveau
            except Niveau.DoesNotExist:
                raise serializers.ValidationError(
                    f"Niveau avec l'ID {value} introuvable ou inactif."
                )
        return None

    def validate(self, data):
        """
        Cross-field validation for geographic consistency.
        
        Ensures education level is compatible with selected country
        and handles automatic country assignment when appropriate.
        """
        pays_id = data.get('pays_id')
        niveau_pays_id = data.get('niveau_pays_id')
        
        # Convert IDs to objects using individual field validation
        pays = self.validate_pays_id(pays_id) if pays_id else None
        niveau_pays = self.validate_niveau_pays_id(niveau_pays_id) if niveau_pays_id else None
        
        # Validate compatibility if both are provided
        if pays and niveau_pays:
            if niveau_pays.pays != pays:
                available_levels = Niveau.objects.filter(
                    pays=pays, 
                    est_actif=True
                ).values_list('nom', flat=True)
                
                raise serializers.ValidationError({
                    'niveau_pays_id': (
                        f"Le niveau '{niveau_pays.nom}' n'est pas disponible "
                        f"pour {pays.nom}. Niveaux disponibles: "
                        f"{', '.join(available_levels)}"
                    )
                })
        
        # Auto-assign country from education level if not provided
        elif niveau_pays and not pays:
            pays = niveau_pays.pays
            data['pays_id'] = pays.id
        
        # Store validated objects for update method
        if pays:
            data['pays'] = pays
        if niveau_pays:
            data['niveau_pays'] = niveau_pays
        
        return data

    def update(self, instance, validated_data):
        """
        Update user geographic data with intelligent handling.
        
        Features:
            - Automatic education level reset on country change
            - Maintains data consistency
            - Provides clear feedback on changes
        """
        pays = validated_data.get('pays')
        niveau_pays = validated_data.get('niveau_pays')
        
        changes_made = []
        
        # Handle country change
        if pays and pays != instance.pays:
            # Check if current education level is compatible
            if instance.niveau_pays and instance.niveau_pays.pays != pays:
                instance.niveau_pays = None
                changes_made.append(
                    f"Niveau d'éducation réinitialisé (incompatible avec {pays.nom})"
                )
            
            instance.pays = pays
            changes_made.append(f"Pays mis à jour vers {pays.nom}")
        
        # Handle education level change
        if niveau_pays and niveau_pays != instance.niveau_pays:
            instance.niveau_pays = niveau_pays
            changes_made.append(f"Niveau mis à jour vers {niveau_pays.nom}")
            
            # Auto-update country if needed
            if instance.pays != niveau_pays.pays:
                instance.pays = niveau_pays.pays
                changes_made.append(f"Pays mis à jour vers {niveau_pays.pays.nom}")
        
        instance.save()
        
        # Log changes for audit trail
        if changes_made:
            import logging
            logger = logging.getLogger(__name__)
            logger.info(
                f"Geographic data updated for user {instance.email}: "
                f"{'; '.join(changes_made)}"
            )
        
        return instance

    def to_representation(self, instance):
        """
        Return complete geographic information in response.
        
        Includes full country and education level details.
        """
        from pays.serializers import PaysSerializer, NiveauSerializer
        
        data = {}
        
        if instance.pays:
            data['pays'] = PaysSerializer(instance.pays).data
        
        if instance.niveau_pays:
            data['niveau_pays'] = NiveauSerializer(instance.niveau_pays).data
        
        return data


class UserPaysNiveauUpdateSerializer(serializers.Serializer):
    """
    Serializer simplifié pour mettre à jour pays et niveau utilisateur.
    """
    
    pays_id = serializers.IntegerField(required=False, allow_null=True)
    niveau_pays_id = serializers.IntegerField(required=False, allow_null=True)
    
    def validate_pays_id(self, value):
        """Valide que le pays existe et est actif."""
        if value is not None:
            try:
                Pays.objects.get(id=value, est_actif=True)
                return value  # Retourner l'ID, pas l'objet
            except Pays.DoesNotExist:
                raise serializers.ValidationError(f"Pays avec l'ID {value} introuvable.")
        return None
    
    def validate_niveau_pays_id(self, value):
        """Valide que le niveau existe et est actif."""
        if value is not None:
            try:
                Niveau.objects.get(id=value, est_actif=True)
                return value  # Retourner l'ID, pas l'objet
            except Niveau.DoesNotExist:
                raise serializers.ValidationError(f"Niveau avec l'ID {value} introuvable.")
        return None
    
    def validate(self, data):
        """Validation croisée pays/niveau."""
        pays_id = data.get('pays_id')
        niveau_pays_id = data.get('niveau_pays_id')
        
        # Vérifier la compatibilité si les deux sont fournis
        if pays_id and niveau_pays_id:
            try:
                pays = Pays.objects.get(id=pays_id, est_actif=True)
                niveau = Niveau.objects.get(id=niveau_pays_id, est_actif=True)
                
                if niveau.pays != pays:
                    raise serializers.ValidationError(
                        f"Le niveau {niveau.nom} n'est pas compatible avec le pays {pays.nom}"
                    )
            except (Pays.DoesNotExist, Niveau.DoesNotExist):
                pass  # Les erreurs seront gérées par les validations individuelles
        
        return data
    
    def save(self, user):
        """Met à jour l'utilisateur avec les nouvelles données."""
        validated_data = self.validated_data
        
        if 'pays_id' in validated_data and validated_data['pays_id']:
            user.pays_id = validated_data['pays_id']
        if 'niveau_pays_id' in validated_data and validated_data['niveau_pays_id']:
            user.niveau_pays_id = validated_data['niveau_pays_id']
            
        user.save()
        return user
