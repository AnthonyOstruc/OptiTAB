import os

# Stripe credentials
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', '')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')
STRIPE_WEBHOOK_SECRET_LIVE = os.getenv('STRIPE_WEBHOOK_SECRET_LIVE', '')
STRIPE_WEBHOOK_SECRET_TEST = os.getenv('STRIPE_WEBHOOK_SECRET_TEST', '')

# Frontend URLs for redirect after checkout
FRONTEND_BASE_URL = os.getenv('FRONTEND_BASE_URL', 'http://localhost:3000')
SUCCESS_URL = os.getenv('STRIPE_SUCCESS_URL', f"{FRONTEND_BASE_URL}/billing/success")
CANCEL_URL = os.getenv('STRIPE_CANCEL_URL', f"{FRONTEND_BASE_URL}/billing/cancel")

# Trial configuration (0 = no trial)
FREE_TRIAL_DAYS = max(0, int(os.getenv('STRIPE_FREE_TRIAL_DAYS', '0')))


def _is_truthy(value):
    return (value or '').strip().lower() in {'1', 'true', 'yes', 'on'}


def _is_production_runtime():
    # Optional explicit override when needed in uncommon environments.
    stripe_env = (os.getenv('STRIPE_ENV') or '').strip().lower()
    if stripe_env in {'prod', 'production', 'live'}:
        return True
    if stripe_env in {'dev', 'development', 'local', 'test'}:
        return False

    # Render is always production for this project.
    if (
        os.getenv('RENDER', '').strip().lower() == 'true'
        or bool(os.getenv('RENDER_EXTERNAL_URL'))
        or bool(os.getenv('RENDER_SERVICE_NAME'))
    ):
        return True

    # Fallback: local DEBUG convention.
    debug_env = os.getenv('DEBUG')
    if debug_env is not None:
        return debug_env.strip().lower() == 'false'

    return False


def _detect_key_mode(key_value, *, key_type):
    key = (key_value or '').strip().lower()
    if not key:
        return 'missing'

    live_prefixes = ('sk_live_', 'rk_live_') if key_type == 'secret' else ('pk_live_',)
    test_prefixes = ('sk_test_', 'rk_test_') if key_type == 'secret' else ('pk_test_',)

    if key.startswith(live_prefixes):
        return 'live'
    if key.startswith(test_prefixes):
        return 'test'
    return 'unknown'


def _validate_stripe_mode():
    expected_mode = 'live' if _is_production_runtime() else 'test'
    runtime_label = 'production' if expected_mode == 'live' else 'local/development'

    secret_mode = _detect_key_mode(STRIPE_SECRET_KEY, key_type='secret')
    publishable_mode = _detect_key_mode(STRIPE_PUBLISHABLE_KEY, key_type='publishable')

    if secret_mode in {'live', 'test'} and publishable_mode in {'live', 'test'} and secret_mode != publishable_mode:
        raise RuntimeError(
            'Stripe mode mismatch: STRIPE_SECRET_KEY and STRIPE_PUBLISHABLE_KEY are not in the same mode.'
        )

    for key_name, key_mode in (
        ('STRIPE_SECRET_KEY', secret_mode),
        ('STRIPE_PUBLISHABLE_KEY', publishable_mode),
    ):
        if key_mode in {'live', 'test'} and key_mode != expected_mode:
            raise RuntimeError(
                f'{key_name} is {key_mode.upper()} but runtime is {runtime_label}. '
                f'Expected {expected_mode.upper()} key. '
                'Fix env vars (.env local vs Render production). '
                'Set STRIPE_DISABLE_MODE_GUARD=true only as a temporary override.'
            )


STRIPE_RUNTIME_MODE = 'live' if _is_production_runtime() else 'test'
if not _is_truthy(os.getenv('STRIPE_DISABLE_MODE_GUARD')):
    _validate_stripe_mode()


def get_stripe_webhook_secrets():
    """Return the configured webhook signing secrets in verification order.

    Order matters only for logs/perf. We prefer the secret matching the current
    runtime mode, then the alternate mode, then the legacy single-secret value.
    """
    if STRIPE_RUNTIME_MODE == 'live':
        ordered_candidates = (
            STRIPE_WEBHOOK_SECRET_LIVE,
            STRIPE_WEBHOOK_SECRET_TEST,
            STRIPE_WEBHOOK_SECRET,
        )
    else:
        ordered_candidates = (
            STRIPE_WEBHOOK_SECRET_TEST,
            STRIPE_WEBHOOK_SECRET_LIVE,
            STRIPE_WEBHOOK_SECRET,
        )

    secrets = []
    for candidate in ordered_candidates:
        secret = (candidate or '').strip()
        if secret and secret not in secrets:
            secrets.append(secret)

    return tuple(secrets)
