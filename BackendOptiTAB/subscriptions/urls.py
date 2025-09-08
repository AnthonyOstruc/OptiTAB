from django.urls import path
from .views import (
    CreateCheckoutSessionView,
    SubscriptionStatusView,
    CancelSubscriptionView,
    PlansListView,
    stripe_webhook
)

urlpatterns = [
    path('plans/', PlansListView.as_view(), name='plans-list'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('status/', SubscriptionStatusView.as_view(), name='subscription-status'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel-subscription'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
]
