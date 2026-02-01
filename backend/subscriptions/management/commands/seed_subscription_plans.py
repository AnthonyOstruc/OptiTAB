from django.core.management.base import BaseCommand, CommandError
from subscriptions.models import SubscriptionPlan


class Command(BaseCommand):
    help = "Create or update the 4 OptiTAB plans (monthly, yearly, pass month, pass day)."

    def add_arguments(self, parser):
        parser.add_argument('--monthly', dest='monthly', help='Stripe Price ID for monthly subscription (price_...)')
        parser.add_argument('--yearly', dest='yearly', help='Stripe Price ID for yearly subscription (price_...)')
        parser.add_argument('--pass-month', dest='pass_month', help='Stripe Price ID for one-time 1 month pass (price_...)')
        parser.add_argument('--pass-day', dest='pass_day', help='Stripe Price ID for one-time 1 day pass (price_...)')

    def handle(self, *args, **opts):
        monthly = (opts.get('monthly') or '').strip()
        yearly = (opts.get('yearly') or '').strip()
        pass_month = (opts.get('pass_month') or '').strip()
        pass_day = (opts.get('pass_day') or '').strip()

        # Accept any subset; error only if none provided
        provided = {
            'monthly': monthly,
            'yearly': yearly,
            'pass-month': pass_month,
            'pass-day': pass_day,
        }
        if not any(provided.values()):
            raise CommandError(
                "No Stripe Price ID provided. Provide at least one using: "
                "--monthly/--yearly/--pass-month/--pass-day"
            )

        created, updated = 0, 0

        def upsert(name, plan_type, mode, billing_period, price, stripe_price_id, access_days=None, features=None):
            nonlocal created, updated
            features = features or []

            # Build defaults dynamically (ignore fields not present in model)
            allowed = {f.name for f in SubscriptionPlan._meta.get_fields()}
            defaults = {
                'name': name,
                'plan_type': plan_type,
                'billing_period': billing_period,
                'price': price,
                'features': features,
                'is_active': True,
            }
            if 'mode' in allowed:
                defaults['mode'] = mode
            if 'access_days' in allowed and access_days is not None:
                defaults['access_days'] = access_days

            # Unique anchor: stripe_price_id is unique
            obj, is_created = SubscriptionPlan.objects.update_or_create(
                stripe_price_id=stripe_price_id,
                defaults=defaults,
            )
            if is_created:
                created += 1
            else:
                updated += 1
            return obj

        # Plans definition (keep plan_type distinct to avoid unique_together clash)
        if monthly:
            upsert(
                name='Mensuel', plan_type='basic', mode='subscription', billing_period='monthly', price=4.99,
                stripe_price_id=monthly,
                features=['Accès complet à OptiTAB', 'Sans engagement, annulable à tout moment']
            )
        if yearly:
            upsert(
                name='Annuel', plan_type='premium', mode='subscription', billing_period='yearly', price=50.00,
                stripe_price_id=yearly,
                features=['Accès complet pendant 12 mois', 'Économisez ~16% vs mensuel']
            )
        if pass_month:
            upsert(
                name='Pass 1 mois', plan_type='basic', mode='one_time', billing_period='monthly', price=6.99,
                stripe_price_id=pass_month, access_days=30,
                features=['Accès 30 jours', 'Paiement unique, non reconduit']
            )
        if pass_day:
            upsert(
                name='Pass 24h', plan_type='premium', mode='one_time', billing_period='monthly', price=0.99,
                stripe_price_id=pass_day, access_days=1,
                features=['Accès 24 heures', 'Idéal pour un contrôle/devoir']
            )

        self.stdout.write(self.style.SUCCESS(f"Plans created: {created}, updated: {updated}"))
