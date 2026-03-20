import hashlib
import logging
import os
import re
from datetime import datetime
from typing import Any, Dict, Optional

import requests
from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

logger = logging.getLogger(__name__)

_DEFAULT_ENDPOINT = 'https://business-api.tiktok.com/open_api/v1.3/event/track/'
_MAX_STRIPE_METADATA_VALUE_LENGTH = 450
_EVENT_KEY_SANITIZER = re.compile(r'[^a-zA-Z0-9:_-]+')


_STRIPE_METADATA_MAP = {
    'ttclid': 'ttclid',
    'ttp': 'ttp',
    'ip': 'tt_ip',
    'user_agent': 'tt_ua',
    'url': 'tt_url',
    'referrer': 'tt_ref',
}


def _get_setting(name: str, default: Any = '') -> Any:
    if hasattr(settings, name):
        return getattr(settings, name)
    return os.getenv(name, default)


def _get_pixel_id() -> str:
    return str(_get_setting('TIKTOK_PIXEL_ID', '') or '').strip()


def _get_access_token() -> str:
    return str(_get_setting('TIKTOK_EVENTS_API_ACCESS_TOKEN', '') or '').strip()


def _get_endpoint() -> str:
    value = str(_get_setting('TIKTOK_EVENTS_API_URL', _DEFAULT_ENDPOINT) or '').strip()
    return value or _DEFAULT_ENDPOINT


def _get_timeout_seconds() -> float:
    raw_value = _get_setting('TIKTOK_EVENTS_API_TIMEOUT_SECONDS', 3)
    try:
        timeout = float(raw_value)
    except (TypeError, ValueError):
        timeout = 3.0
    return max(0.5, min(timeout, 10.0))


def _get_test_event_code() -> str:
    return str(_get_setting('TIKTOK_TEST_EVENT_CODE', '') or '').strip()


def _get_dedupe_ttl_seconds() -> int:
    raw_value = _get_setting('TIKTOK_EVENTS_DEDUPE_TTL_SECONDS', 7 * 24 * 60 * 60)
    try:
        ttl = int(raw_value)
    except (TypeError, ValueError):
        ttl = 7 * 24 * 60 * 60
    return max(60, min(ttl, 30 * 24 * 60 * 60))


def _clean_text(value: Any, *, limit: int = 500) -> str:
    text = str(value or '').strip()
    if not text:
        return ''
    if len(text) > limit:
        return text[:limit]
    return text


def _sanitize_event_key(value: Any) -> str:
    raw = _clean_text(value, limit=256)
    if not raw:
        return ''
    cleaned = _EVENT_KEY_SANITIZER.sub('-', raw)
    cleaned = re.sub(r'-{2,}', '-', cleaned).strip('-')
    return cleaned[:120]


def _sha256(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def _normalize_email(value: Any) -> str:
    return _clean_text(value, limit=320).lower()


def _normalize_phone(value: Any) -> str:
    raw = _clean_text(value, limit=64)
    if not raw:
        return ''
    normalized = re.sub(r'[^0-9+]', '', raw)
    if normalized.startswith('00'):
        normalized = f'+{normalized[2:]}'
    return normalized


def _to_timestamp_seconds(event_time: Optional[Any]) -> int:
    if event_time is None:
        return int(timezone.now().timestamp())

    if isinstance(event_time, (int, float)):
        return int(event_time)

    if isinstance(event_time, datetime):
        dt = event_time
        if timezone.is_naive(dt):
            dt = timezone.make_aware(dt, timezone.get_current_timezone())
        return int(dt.timestamp())

    return int(timezone.now().timestamp())


def _extract_client_ip(request) -> str:
    if request is None:
        return ''

    forwarded_for = _clean_text(request.META.get('HTTP_X_FORWARDED_FOR'), limit=256)
    if forwarded_for:
        first_hop = forwarded_for.split(',')[0].strip()
        if first_hop:
            return first_hop

    return (
        _clean_text(request.META.get('HTTP_X_REAL_IP'), limit=64)
        or _clean_text(request.META.get('REMOTE_ADDR'), limit=64)
    )


def extract_tiktok_context_from_request(request) -> Dict[str, str]:
    if request is None:
        return {}

    ttclid = (
        _clean_text(request.META.get('HTTP_X_TTCLID'), limit=200)
        or _clean_text(request.GET.get('ttclid'), limit=200)
    )

    ttp = (
        _clean_text(request.META.get('HTTP_X_TTP'), limit=200)
        or _clean_text(request.COOKIES.get('_ttp'), limit=200)
        or _clean_text(request.COOKIES.get('ttp'), limit=200)
    )

    page_url = _clean_text(request.META.get('HTTP_X_PAGE_URL'), limit=500)
    if not page_url:
        try:
            page_url = _clean_text(request.build_absolute_uri(), limit=500)
        except Exception:
            page_url = ''

    referrer = (
        _clean_text(request.META.get('HTTP_X_PAGE_REFERRER'), limit=500)
        or _clean_text(request.META.get('HTTP_REFERER'), limit=500)
    )

    context = {
        'ttclid': ttclid,
        'ttp': ttp,
        'ip': _extract_client_ip(request),
        'user_agent': _clean_text(request.META.get('HTTP_USER_AGENT'), limit=500),
        'url': page_url,
        'referrer': referrer,
    }

    user = getattr(request, 'user', None)
    if user is not None and getattr(user, 'is_authenticated', False):
        context['external_id'] = _clean_text(getattr(user, 'id', ''), limit=64)

    return {key: value for key, value in context.items() if value}


def merge_tiktok_context_into_stripe_metadata(
    metadata: Optional[Dict[str, Any]],
    *,
    request=None,
    context: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    merged_metadata: Dict[str, Any] = {}
    if isinstance(metadata, dict):
        merged_metadata.update(metadata)

    merged_context: Dict[str, Any] = {}
    if request is not None:
        merged_context.update(extract_tiktok_context_from_request(request))
    if isinstance(context, dict):
        merged_context.update({k: v for k, v in context.items() if v is not None})

    for context_key, metadata_key in _STRIPE_METADATA_MAP.items():
        value = _clean_text(merged_context.get(context_key), limit=_MAX_STRIPE_METADATA_VALUE_LENGTH)
        if value:
            merged_metadata[metadata_key] = value

    return merged_metadata


def extract_tiktok_context_from_metadata(metadata: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not isinstance(metadata, dict):
        return {}

    extracted: Dict[str, str] = {}
    for context_key, metadata_key in _STRIPE_METADATA_MAP.items():
        value = _clean_text(metadata.get(metadata_key), limit=500)
        if value:
            extracted[context_key] = value

    return extracted


def build_complete_registration_event_id(user_id: Any) -> str:
    return _sanitize_event_key(user_id) or 'unknown'


def build_start_trial_event_id(subscription_id: Any) -> str:
    return f"st:{_sanitize_event_key(subscription_id) or 'unknown'}"


def build_subscribe_event_id(subscription_id: Any) -> str:
    return f"sb:{_sanitize_event_key(subscription_id) or 'unknown'}"


def build_purchase_event_id(transaction_reference: Any) -> str:
    return _sanitize_event_key(transaction_reference) or 'unknown'


def _build_event_dedupe_cache_key(event_name: str, event_id: str) -> str:
    digest = hashlib.sha1(f'{event_name}:{event_id}'.encode('utf-8')).hexdigest()
    return f'tiktok:event:{digest}'


def _build_user_payload(user=None, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    context = context or {}

    email_raw = context.get('email')
    if not email_raw and user is not None:
        email_raw = getattr(user, 'email', None)

    phone_raw = context.get('phone')
    if not phone_raw and user is not None:
        phone_raw = getattr(user, 'telephone', None)

    external_id_raw = context.get('external_id')
    if not external_id_raw and user is not None:
        external_id_raw = getattr(user, 'id', None)

    payload: Dict[str, Any] = {}

    normalized_email = _normalize_email(email_raw)
    if normalized_email:
        payload['email'] = _sha256(normalized_email)

    normalized_phone = _normalize_phone(phone_raw)
    if normalized_phone:
        payload['phone'] = _sha256(normalized_phone)

    external_id_value = _clean_text(external_id_raw, limit=128)
    if external_id_value:
        payload['external_id'] = _sha256(external_id_value)

    for field_name, limit in (
        ('ttclid', 200),
        ('ttp', 200),
        ('ip', 64),
        ('user_agent', 500),
    ):
        value = _clean_text(context.get(field_name), limit=limit)
        if value:
            payload[field_name] = value

    return payload


def _build_properties_payload(
    *,
    value: Optional[Any] = None,
    currency: Optional[str] = None,
    content_id: Optional[Any] = None,
    content_name: Optional[str] = None,
) -> Dict[str, Any]:
    properties: Dict[str, Any] = {}

    if value is not None:
        try:
            numeric = float(value)
            if numeric > 0:
                properties['value'] = round(numeric, 2)
        except (TypeError, ValueError):
            pass

    normalized_currency = _clean_text(currency, limit=8).upper()
    if normalized_currency:
        properties['currency'] = normalized_currency

    content_item: Dict[str, Any] = {}
    normalized_content_id = _clean_text(content_id, limit=128)
    if normalized_content_id:
        content_item['content_id'] = normalized_content_id

    normalized_content_name = _clean_text(content_name, limit=200)
    if normalized_content_name:
        content_item['content_name'] = normalized_content_name

    if content_item:
        properties['contents'] = [content_item]

    return properties


def send_tiktok_web_event(
    event_name: str,
    *,
    event_id: str,
    user=None,
    request=None,
    context: Optional[Dict[str, Any]] = None,
    event_time: Optional[Any] = None,
    value: Optional[Any] = None,
    currency: Optional[str] = None,
    content_id: Optional[Any] = None,
    content_name: Optional[str] = None,
) -> bool:
    pixel_id = _get_pixel_id()
    access_token = _get_access_token()

    if not pixel_id or not access_token:
        return False

    normalized_event_name = _clean_text(event_name, limit=64)
    normalized_event_id = _clean_text(event_id, limit=128)
    if not normalized_event_name or not normalized_event_id:
        return False

    dedupe_cache_key = _build_event_dedupe_cache_key(normalized_event_name, normalized_event_id)
    dedupe_lock_acquired = False
    try:
        dedupe_lock_acquired = bool(cache.add(dedupe_cache_key, 'pending', timeout=120))
        if not dedupe_lock_acquired:
            cached_status = cache.get(dedupe_cache_key)
            if cached_status in ('pending', 'sent'):
                return True
            dedupe_lock_acquired = bool(cache.add(dedupe_cache_key, 'pending', timeout=120))
            if not dedupe_lock_acquired:
                return True
    except Exception:
        dedupe_lock_acquired = False

    merged_context: Dict[str, Any] = {}
    if request is not None:
        merged_context.update(extract_tiktok_context_from_request(request))
    if isinstance(context, dict):
        merged_context.update({key: value for key, value in context.items() if value is not None})

    user_payload = _build_user_payload(user=user, context=merged_context)
    properties_payload = _build_properties_payload(
        value=value,
        currency=currency,
        content_id=content_id,
        content_name=content_name,
    )

    event_payload: Dict[str, Any] = {
        'event': normalized_event_name,
        'event_time': _to_timestamp_seconds(event_time),
        'event_id': normalized_event_id,
    }

    if user_payload:
        event_payload['user'] = user_payload

    if properties_payload:
        event_payload['properties'] = properties_payload

    page_url = _clean_text(merged_context.get('url'), limit=500)
    referrer = _clean_text(merged_context.get('referrer'), limit=500)
    if page_url or referrer:
        event_payload['page'] = {
            'url': page_url,
            'referrer': referrer,
        }

    payload: Dict[str, Any] = {
        'event_source': 'web',
        'event_source_id': pixel_id,
        'data': [event_payload],
    }

    test_event_code = _get_test_event_code()
    if test_event_code:
        payload['test_event_code'] = test_event_code

    headers = {
        'Access-Token': access_token,
        'Content-Type': 'application/json',
    }

    try:
        response = requests.post(
            _get_endpoint(),
            json=payload,
            headers=headers,
            timeout=_get_timeout_seconds(),
        )
    except requests.RequestException as exc:
        if dedupe_lock_acquired:
            try:
                cache.delete(dedupe_cache_key)
            except Exception:
                pass
        logger.warning('TikTok Events API request failed for %s (%s): %s', normalized_event_name, normalized_event_id, exc)
        return False

    if response.status_code >= 400:
        if dedupe_lock_acquired:
            try:
                cache.delete(dedupe_cache_key)
            except Exception:
                pass
        logger.warning(
            'TikTok Events API HTTP %s for %s (%s)',
            response.status_code,
            normalized_event_name,
            normalized_event_id,
        )
        return False

    try:
        response_data = response.json()
    except ValueError:
        if dedupe_lock_acquired:
            try:
                cache.set(dedupe_cache_key, 'sent', timeout=_get_dedupe_ttl_seconds())
            except Exception:
                pass
        return True

    if isinstance(response_data, dict):
        response_code = response_data.get('code')
        if response_code not in (0, '0', None):
            if dedupe_lock_acquired:
                try:
                    cache.delete(dedupe_cache_key)
                except Exception:
                    pass
            logger.warning(
                'TikTok Events API rejected %s (%s): code=%s message=%s',
                normalized_event_name,
                normalized_event_id,
                response_code,
                response_data.get('message') or response_data.get('msg') or '',
            )
            return False

    if dedupe_lock_acquired:
        try:
            cache.set(dedupe_cache_key, 'sent', timeout=_get_dedupe_ttl_seconds())
        except Exception:
            pass

    return True


def send_complete_registration_event(
    *,
    event_id: str,
    user=None,
    request=None,
    context: Optional[Dict[str, Any]] = None,
    event_time: Optional[Any] = None,
) -> bool:
    return send_tiktok_web_event(
        'CompleteRegistration',
        event_id=event_id,
        user=user,
        request=request,
        context=context,
        event_time=event_time,
    )


def send_start_trial_event(
    *,
    event_id: str,
    user=None,
    request=None,
    context: Optional[Dict[str, Any]] = None,
    event_time: Optional[Any] = None,
    value: Optional[Any] = None,
    currency: Optional[str] = None,
    content_id: Optional[Any] = None,
    content_name: Optional[str] = None,
) -> bool:
    return send_tiktok_web_event(
        'StartTrial',
        event_id=event_id,
        user=user,
        request=request,
        context=context,
        event_time=event_time,
        value=value,
        currency=currency,
        content_id=content_id,
        content_name=content_name,
    )


def send_subscribe_event(
    *,
    event_id: str,
    user=None,
    request=None,
    context: Optional[Dict[str, Any]] = None,
    event_time: Optional[Any] = None,
    value: Optional[Any] = None,
    currency: Optional[str] = None,
    content_id: Optional[Any] = None,
    content_name: Optional[str] = None,
) -> bool:
    return send_tiktok_web_event(
        'Subscribe',
        event_id=event_id,
        user=user,
        request=request,
        context=context,
        event_time=event_time,
        value=value,
        currency=currency,
        content_id=content_id,
        content_name=content_name,
    )


def send_purchase_event(
    *,
    event_id: str,
    user=None,
    request=None,
    context: Optional[Dict[str, Any]] = None,
    event_time: Optional[Any] = None,
    value: Optional[Any] = None,
    currency: Optional[str] = None,
    content_id: Optional[Any] = None,
    content_name: Optional[str] = None,
) -> bool:
    return send_tiktok_web_event(
        'Purchase',
        event_id=event_id,
        user=user,
        request=request,
        context=context,
        event_time=event_time,
        value=value,
        currency=currency,
        content_id=content_id,
        content_name=content_name,
    )
