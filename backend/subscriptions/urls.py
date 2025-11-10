from django.urls import path
from .views import (
    CreateCheckoutSessionView,
    SubscriptionStatusView,
    InvoiceListView,
    InvoiceEmailView,
    CheckoutSessionStatusView,
    CancelSubscriptionView,
    PlansListView,
    stripe_webhook,
    AdminPlansView,
    AdminPlanDetailView,
    AdminSubscribersView,
    AdminStripeSyncView,
    AdminSubscriptionCancelView,
)

urlpatterns = [
    path('plans/', PlansListView.as_view(), name='plans-list'),
    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('checkout-session/status/', CheckoutSessionStatusView.as_view(), name='checkout-session-status'),
    path('status/', SubscriptionStatusView.as_view(), name='subscription-status'),
    path('invoices/', InvoiceListView.as_view(), name='subscription-invoices'),
    path('invoices/<int:pk>/email/', InvoiceEmailView.as_view(), name='subscription-invoice-email'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel-subscription'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
    # Admin management endpoints
    path('admin/plans/', AdminPlansView.as_view(), name='admin-plans'),
    path('admin/plans/<int:pk>/', AdminPlanDetailView.as_view(), name='admin-plan-detail'),
    path('admin/subscribers/', AdminSubscribersView.as_view(), name='admin-subscribers'),
    path('admin/sync-from-stripe/', AdminStripeSyncView.as_view(), name='admin-sync-from-stripe'),
    path('admin/subscribers/cancel/', AdminSubscriptionCancelView.as_view(), name='admin-cancel-subscription'),
]
