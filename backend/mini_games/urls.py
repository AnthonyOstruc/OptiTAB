from django.urls import path
from . import views

urlpatterns = [
    path('math-run/score/',       views.submit_score,    name='mathrun-score'),
    path('math-run/leaderboard/', views.get_leaderboard, name='mathrun-leaderboard'),
]
