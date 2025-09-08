from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SynthesisSheetViewSet

router = DefaultRouter()
router.register(r'sheets', SynthesisSheetViewSet, basename='synthesissheet')

urlpatterns = [
    path('', include(router.urls)),
]
