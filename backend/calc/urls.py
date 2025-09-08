from django.urls import path
from .views import DerivativeView, IntegralView, ExpandView, FactorView, LimitView

urlpatterns=[
    path('derive/', DerivativeView.as_view()),
    path('integrate/', IntegralView.as_view()),
    path('expand/', ExpandView.as_view()),
    path('factor/', FactorView.as_view()),
    path('limit/', LimitView.as_view()),
] 