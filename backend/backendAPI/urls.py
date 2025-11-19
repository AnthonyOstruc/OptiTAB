from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from core.views import redirect_to_frontend, contact_send

urlpatterns = [
    path('', include('core.urls')),  # Root view
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
    path('api/', include('curriculum.urls')),
    path('api/cours/', include('cours.urls')),
    path('api/', include('synthesis.urls')),
    path('api/suivis/', include('suivis.urls')),
    path('api/calc/', include('calc.urls')),
    path('api/quiz/', include('quiz.urls')),
    path('api/ai/', include('ai.urls')),
    path('api/subscriptions/', include('subscriptions.urls')),
    path('api/free/', include('freecontent.urls')),
    path('api/contact/send/', contact_send, name='contact_send'),
    # path('api/', include('niveaux.urls')),  # Removed - using NiveauPays in pays
    path('api/', include('pays.urls')),  # API pour les pays et niveaux par pays
    # Catch-all for non-API, non-admin paths when they accidentally hit backend
    #re_path(r'^(?!admin/|api/).*$', redirect_to_frontend),
]

# Servir les fichiers statiques et médias
# - Statiques: déjà gérées par WhiteNoise en production
# - Médias: exposés aussi en production (Render) via Django pour simplifier le déploiement
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Servir les médias depuis le disque local uniquement si MEDIA_URL est un chemin local
# En mode S3 (MEDIA_URL absolue https), ne pas ajouter de route /media/
if isinstance(settings.MEDIA_URL, str) and settings.MEDIA_URL.startswith('/'):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Vérifier la configuration média au démarrage (debug)
if settings.DEBUG:
    from django.core.management import execute_from_command_line
    import sys
    try:
        execute_from_command_line(['manage.py', 'check', '--deploy'])
    except SystemExit:
        pass
else:
    # En production, vérifier que les répertoires médias existent
    import os
    media_root = settings.MEDIA_ROOT
    if not os.path.exists(media_root):
        print(f"AVERTISSEMENT: Répertoire médias manquant: {media_root}")
    else:
        print(f"Répertoire médias OK: {media_root}")
