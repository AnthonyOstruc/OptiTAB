from django.contrib import admin
from .models import SubscriptionPlan, UserSubscription, PaymentHistory


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "plan_type", "billing_period", "price", "is_active")
    list_filter = ("plan_type", "billing_period", "is_active")
    search_fields = ("name", "stripe_price_id")


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "plan", "status", "current_period_end")
    list_filter = ("status", "plan__plan_type", "plan__billing_period")
    search_fields = ("user__email", "stripe_subscription_id", "stripe_customer_id")


@admin.register(PaymentHistory)
class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ("user", "amount", "currency", "status", "created_at")
    list_filter = ("status", "currency")
    search_fields = ("user__email", "stripe_payment_intent_id")
    readonly_fields = ("created_at",)

