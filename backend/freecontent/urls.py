from rest_framework.routers import DefaultRouter

from .views import FreeLearningResourceViewSet

router = DefaultRouter()
router.register(r'learning-resources', FreeLearningResourceViewSet, basename='free-learning-resource')

urlpatterns = router.urls
