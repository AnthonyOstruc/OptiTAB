from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SynthesisSheetViewSet, SynthesisImageViewSet

router = DefaultRouter()
router.register(r'sheets', SynthesisSheetViewSet, basename='synthesissheet')
router.register(r'sheet-images', SynthesisImageViewSet, basename='synthesis-image')

urlpatterns = [
    path('', include(router.urls)),
]
