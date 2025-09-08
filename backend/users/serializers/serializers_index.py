"""
User Serializers Package - Professional Organization
==================================================

Centralized imports for all user-related serializers with clean
organization and backward compatibility.
"""

# Authentication serializers
from .authentication import RegisterSerializer, EmailVerificationSerializer
from .verify_code_serializers import VerifyCodeSerializer

# User profile serializers  
from .user_profile import (
    UserSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    UserSerializerWithNiveau,
)

# Geographic data serializers
from .geographic_data import UserPaysNiveauUpdateSerializer

# User preferences serializers
from .preferences_serializers import (
    MatiereBasicSerializer,
    UserFavoriteMatiereSerializer,
    UserSelectedMatiereSerializer,
    UserPreferencesSerializer,
    BulkUpdateMatierePreferencesSerializer,
)

# JWT authentication serializers
from .token_serializers import CustomTokenObtainPairSerializer

# Clean exports
__all__ = [
    # Authentication
    'RegisterSerializer',
    'EmailVerificationSerializer',
    'VerifyCodeSerializer', 
    'CustomTokenObtainPairSerializer',
    
    # User Profile
    'UserSerializer',
    'UserDetailSerializer',
    'UserUpdateSerializer', 
    'UserSerializerWithNiveau',
    
    # Geographic Data
    'UserPaysNiveauUpdateSerializer',
    
    # User Preferences
    'MatiereBasicSerializer',
    'UserFavoriteMatiereSerializer',
    'UserSelectedMatiereSerializer',
    'UserPreferencesSerializer', 
    'BulkUpdateMatierePreferencesSerializer',
]
