from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
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
]

# Servir les fichiers médias en développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
