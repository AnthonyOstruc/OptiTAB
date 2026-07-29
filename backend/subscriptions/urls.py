from django.urls import path
from .views import (
    CreateCheckoutSessionView,
    GuestCheckoutSessionView,
    GuestCheckoutStatusView,
    SubscriptionStatusView,
    InvoiceListView,
    InvoiceEmailView,
    CheckoutSessionStatusView,
    CancelSubscriptionView,
    ReactivateSubscriptionView,
    PlansListView,
    stripe_webhook,
    stripe_webhook_test,
    AdminPlansView,
    AdminPlanDetailView,
    AdminSubscribersView,
    AdminPassesView,
    AdminPassDetailView,
    AdminStripeSyncView,
    AdminSubscriptionPlanChangeView,
    AdminSubscriptionCancelView,
)

from .lesson_payment_views import (
    lesson_payment_config,
    lesson_payment_create_session,
    lesson_payment_status,
    admin_lesson_payments,
)

urlpatterns = [
    path('plans/', PlansListView.as_view(), name='plans-list'),

    # Versements ponctuels pour cours particuliers (montant libre)
    path('lesson-payment/config/', lesson_payment_config, name='lesson-payment-config'),
    path('lesson-payment/create-session/', lesson_payment_create_session, name='lesson-payment-create'),
    path('lesson-payment/status/', lesson_payment_status, name='lesson-payment-status'),
    path('admin/lesson-payments/', admin_lesson_payments, name='admin-lesson-payments'),

    path('create-checkout-session/', CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('guest-checkout-session/', GuestCheckoutSessionView.as_view(), name='guest-checkout-session'),
    path('guest-checkout/status/', GuestCheckoutStatusView.as_view(), name='guest-checkout-status'),
    path('checkout-session/status/', CheckoutSessionStatusView.as_view(), name='checkout-session-status'),
    path('status/', SubscriptionStatusView.as_view(), name='subscription-status'),
    path('invoices/', InvoiceListView.as_view(), name='subscription-invoices'),
    path('invoices/<int:pk>/email/', InvoiceEmailView.as_view(), name='subscription-invoice-email'),
    path('cancel/', CancelSubscriptionView.as_view(), name='cancel-subscription'),
    path('reactivate/', ReactivateSubscriptionView.as_view(), name='reactivate-subscription'),
    path('webhook/', stripe_webhook, name='stripe-webhook'),
    path('webhook/test/', stripe_webhook_test, name='stripe-webhook-test'),
    # Admin management endpoints
    path('admin/plans/', AdminPlansView.as_view(), name='admin-plans'),
    path('admin/plans/<int:pk>/', AdminPlanDetailView.as_view(), name='admin-plan-detail'),
    path('admin/subscribers/', AdminSubscribersView.as_view(), name='admin-subscribers'),
    path('admin/passes/', AdminPassesView.as_view(), name='admin-passes'),
    path('admin/passes/<int:pk>/', AdminPassDetailView.as_view(), name='admin-pass-detail'),
    path('admin/sync-from-stripe/', AdminStripeSyncView.as_view(), name='admin-sync-from-stripe'),
    path('admin/subscribers/change-plan/', AdminSubscriptionPlanChangeView.as_view(), name='admin-change-subscription-plan'),
    path('admin/subscribers/cancel/', AdminSubscriptionCancelView.as_view(), name='admin-cancel-subscription'),
]
