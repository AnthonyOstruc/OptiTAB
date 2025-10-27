from django.urls import path
from .views import RootView
from .newsletter_views import newsletter_subscribe, newsletter_unsubscribe, newsletter_subscribers_list, newsletter_broadcast

app_name = 'core'

urlpatterns = [
    path('', RootView.as_view(), name='root'),
    path('api/newsletter/subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
    path('api/newsletter/unsubscribe/<str:token>/', newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('api/newsletter/subscribers/', newsletter_subscribers_list, name='newsletter_subscribers_list'),
    path('api/newsletter/broadcast/', newsletter_broadcast, name='newsletter_broadcast'),
]
