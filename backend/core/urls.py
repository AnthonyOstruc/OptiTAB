from django.urls import path
from .views import RootView

app_name = 'core'

urlpatterns = [
    path('', RootView.as_view(), name='root'),
]
