import stripe
try:
    from stripe import error as stripe_error
except ImportError:
    from stripe import _error as stripe_error  # type: ignore[attr-defined]

from stripe_config import STRIPE_SECRET_KEY

stripe.api_key = STRIPE_SECRET_KEY

__all__ = ['stripe', 'stripe_error']
