from django.urls import path
from users.views.authentication_views import UserRegistrationView, CustomLoginView, EmailVerificationView, UserLogoutView
from users.views.profile_views import MeView, UpdateProfileView, UpdateNiveauView, UpdatePaysView, UpdatePaysNiveauView, MeGamificationView, LeaderboardView, MyChildrenView, ChildOverviewView, AddChildView, RemoveChildView, CreateChildAccountView, MyOverviewView, MyStreaksView, RecommendationsView
from users.views.preferences_views import (
    UserFavoriteMatiereListCreateView,
    UserFavoriteMatiereDetailView,
    UserSelectedMatiereListCreateView,
    UserSelectedMatiereDetailView,
    get_user_preferences,
    bulk_update_preferences,
    add_favorite_matiere,
    remove_favorite_matiere,
    add_selected_matiere,
    remove_selected_matiere,
    set_active_matiere
)
from rest_framework_simplejwt.views import TokenRefreshView
from django_rest_passwordreset.views import reset_password_request_token, reset_password_confirm

urlpatterns = [
    
    # API REST Endpoints existants
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),  #  login personnalisé
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # renouveler le token
    path('password/reset/', reset_password_request_token, name='password_reset'), #reset password
    path('password/reset/confirm/', reset_password_confirm, name='password_reset_confirm'),
    path('verify-code/', EmailVerificationView.as_view(), name='verify_code'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('me/', MeView.as_view(), name='me'),  # pour obtenir les infos de l'utilisateur connecté
    path('me/gamification/', MeGamificationView.as_view(), name='me_gamification'),
    path('me/overview/', MyOverviewView.as_view(), name='me_overview'),
    path('me/streaks/', MyStreaksView.as_view(), name='me_streaks'),
    path('me/recommendations/', RecommendationsView.as_view(), name='me_recommendations'),
    path('leaderboard/', LeaderboardView.as_view(), name='leaderboard'),
    path('me/children/', MyChildrenView.as_view(), name='me_children'),
    path('me/children/add/', AddChildView.as_view(), name='add_child'),
    path('me/children/create/', CreateChildAccountView.as_view(), name='create_child_account'),
    path('me/children/<int:child_id>/remove/', RemoveChildView.as_view(), name='remove_child'),
    path('children/<int:child_id>/overview/', ChildOverviewView.as_view(), name='child_overview'),
    path('me/update/', UpdateProfileView.as_view(), name='me_update'),  # pour modifier les coordonnées utilisateur
    path('me/niveau/', UpdateNiveauView.as_view(), name='me_niveau'),  # pour modifier le niveau utilisateur
    path('me/pays/', UpdatePaysView.as_view(), name='me_pays'),  # pour modifier le pays utilisateur
    path('me/pays-niveau/', UpdatePaysNiveauView.as_view(), name='me_pays_niveau'),  # pour modifier pays et niveau ensemble
    
    # URLs pour les préférences utilisateur
    path('preferences/', get_user_preferences, name='user_preferences'),
    path('preferences/bulk-update/', bulk_update_preferences, name='bulk_update_preferences'),
    
    # URLs pour les matières favorites
    path('favorites/', UserFavoriteMatiereListCreateView.as_view(), name='favorite_matieres'),
    path('favorites/<int:pk>/', UserFavoriteMatiereDetailView.as_view(), name='favorite_matiere_detail'),
    path('favorites/add/<int:matiere_id>/', add_favorite_matiere, name='add_favorite_matiere'),
    path('favorites/remove/<int:matiere_id>/', remove_favorite_matiere, name='remove_favorite_matiere'),
    
    # URLs pour les onglets sélectionnés
    path('selected/', UserSelectedMatiereListCreateView.as_view(), name='selected_matieres'),
    path('selected/<int:pk>/', UserSelectedMatiereDetailView.as_view(), name='selected_matiere_detail'),
    path('selected/add/<int:matiere_id>/', add_selected_matiere, name='add_selected_matiere'),
    path('selected/remove/<int:matiere_id>/', remove_selected_matiere, name='remove_selected_matiere'),
    path('selected/set-active/<int:matiere_id>/', set_active_matiere, name='set_active_matiere'),
]
