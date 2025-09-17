from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from core.views import redirect_to_frontend

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
    # path('api/', include('niveaux.urls')),  # Removed - using NiveauPays in pays
    path('api/', include('pays.urls')),  # API pour les pays et niveaux par pays
    # Catch-all for non-API, non-admin paths when they accidentally hit backend
    #re_path(r'^(?!admin/|api/).*$', redirect_to_frontend),
]

# Servir les fichiers statiques et médias
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
