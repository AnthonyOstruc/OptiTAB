from django.urls import path
from .views import RootView
from .newsletter_views import (
    newsletter_subscribe,
    newsletter_unsubscribe,
    newsletter_subscribers_list,
    newsletter_broadcast,
    diagnostic_lead,
)
from .testimonial_views import (
    testimonial_list,
    admin_testimonial_list,
    admin_testimonial_create,
    admin_testimonial_detail,
    admin_testimonial_reorder,
    bio_landing_status,
    admin_bio_landing_update,
)

app_name = 'core'

urlpatterns = [
    path('', RootView.as_view(), name='root'),
    path('api/newsletter/subscribe/', newsletter_subscribe, name='newsletter_subscribe'),
    path('api/newsletter/unsubscribe/<str:token>/', newsletter_unsubscribe, name='newsletter_unsubscribe'),
    path('api/newsletter/subscribers/', newsletter_subscribers_list, name='newsletter_subscribers_list'),
    path('api/newsletter/broadcast/', newsletter_broadcast, name='newsletter_broadcast'),
    path('api/newsletter/diagnostic-lead/', diagnostic_lead, name='diagnostic_lead'),

    # Temoignages (captures WhatsApp / SMS de la page « lien en bio »)
    path('api/testimonials/', testimonial_list, name='testimonial_list'),
    path('api/admin/testimonials/', admin_testimonial_list, name='admin_testimonial_list'),
    path('api/admin/testimonials/create/', admin_testimonial_create, name='admin_testimonial_create'),
    path('api/admin/testimonials/reorder/', admin_testimonial_reorder, name='admin_testimonial_reorder'),
    path('api/admin/testimonials/<int:pk>/', admin_testimonial_detail, name='admin_testimonial_detail'),

    # Mise en ligne de la page « lien en bio »
    path('api/bio-landing/status/', bio_landing_status, name='bio_landing_status'),
    path('api/admin/bio-landing/', admin_bio_landing_update, name='admin_bio_landing_update'),
]
