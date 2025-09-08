from django.urls import path
from . import views

app_name = 'ai'

urlpatterns = [
    path('ask/', views.ask_ai, name='ask_ai'),
    path('history/', views.get_conversation_history, name='conversation_history'),
]
