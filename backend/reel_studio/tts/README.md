# Reel Studio TTS

Generic text-to-speech dispatcher used by Reel Studio. Supports two
providers, with **Google Cloud Text-to-Speech as the default** so the
project benefits from Google's free monthly quota. **ElevenLabs is kept
as a premium option** and is fully untouched.

```
reel_studio/tts/
├── __init__.py        # public API: generate_speech, list_providers_payload, ...
├── base.py            # exceptions + TTSResult dataclass + provider constants
├── dispatch.py        # routing + caching layer
└── google.py          # Google Cloud TTS provider (REST + google-auth)
```

ElevenLabs lives in `reel_studio/elevenlabs.py` and is invoked via the
dispatcher when `provider="elevenlabs"` is requested.

## Enabling Google Cloud TTS

1. **Create a service account** in Google Cloud and grant it the role
   `Cloud Text-to-Speech API User` (or any role containing
   `texttospeech.synthesize`).
2. **Download the JSON key file** for that service account. **Never commit
   this file to git.** Suggested location:
   ```
   backend/secrets/google-tts-service-account.json
   ```
   The `backend/secrets/` folder is git-ignored.
3. **Set environment variables** in `backend/.env`:
   ```dotenv
   # Make Google TTS the default provider (already the default in code).
   REEL_TTS_DEFAULT_PROVIDER=google

   # Absolute or BASE_DIR-relative path to the JSON key file.
   GOOGLE_APPLICATION_CREDENTIALS=secrets/google-tts-service-account.json

   # French voice, kept inside Google's monthly free character quotas.
   # Default stays on Standard (4M free chars/month). Other listed Google
   # families may have lower limits and are grayed out locally at 90%.
   GOOGLE_TTS_DEFAULT_VOICE=fr-FR-Standard-F
   GOOGLE_TTS_DEFAULT_LANGUAGE=fr-FR

   # Optional safety limits.
   GOOGLE_TTS_TIMEOUT_SECONDS=60
   GOOGLE_TTS_MAX_TEXT_CHARS=4500
   GOOGLE_TTS_QUOTA_DISABLE_RATIO=0.90
   ```
4. Restart Django. The admin UI's "Voice provider" dropdown will now show
   Google Cloud TTS as configured.

The required Python package (`google-auth==2.29.0`) is already in
`requirements.txt`. The official `google-cloud-texttospeech` SDK is **not
needed** — the provider talks to `texttospeech.googleapis.com` over plain
HTTPS using a service-account-signed bearer token.

## Adding or removing voices

Voices are listed in `google.py` as `DEFAULT_FRENCH_VOICES`. The Google
dropdown includes French voices that have a monthly free character quota:

- Standard and Wavenet: 4M free characters/month.
- Chirp3 HD, Neural2, and Studio: 1M free characters/month.

Reel Studio keeps a local monthly counter in Django's cache for characters
actually sent to Google by this app. Once a voice family reaches
`GOOGLE_TTS_QUOTA_DISABLE_RATIO` (default `0.90`), voices in that family are
returned with `api_usable: false`, so the frontend grays them out and the
backend returns HTTP 429 for new upstream calls.

This is a local safety guard, not a live Google Billing API reading. If other
apps use the same Google project, check Google Cloud billing/usage for the
authoritative total.

ElevenLabs voices are still discovered dynamically via
`/v1/voices` on each `/api/admin/reel-studio/voices/` request — no code
changes are needed when you add a new voice on your ElevenLabs account.

## How the cache works

A short cache layer lives in `dispatch.py`:

- The cache key is `sha256(provider + voice_id + text)`.
- A cache hit returns the previously generated MP3 immediately, with no
  upstream call. The response sets `cached: true` and the X-TTS-Cached
  header on the test endpoint.
- The audio bytes themselves are stored under
  `<storage>/reel_studio/tts_cache/<provider>/<voice>/<hash>.mp3`. If S3
  is enabled (`AWS_*` env vars), the cache lives on S3; otherwise it goes
  to the local media folder.
- A short index entry is also written to Django's cache (defaults to the
  filebased backend in production, locmem in dev) so that the existence
  check is fast. The cache layer self-heals: if Django's cache forgets a
  key, `dispatch.py` falls back to probing the storage directly and
  repopulates the index.

To clear the cache, simply delete the
`reel_studio/tts_cache/` folder in your storage backend.

## Endpoints reference

| Method | URL                                            | Purpose                                        |
| ------ | ---------------------------------------------- | ---------------------------------------------- |
| GET    | `/api/admin/reel-studio/voices/`               | List providers + voices for the admin UI       |
| GET    | `/api/admin/reel-studio/voices/?provider=elevenlabs` | Legacy ElevenLabs-only payload          |
| POST   | `/api/admin/reel-studio/test-voice/`           | Synthesize a short preview (returns audio/mpeg)|
| POST   | `.../generate-speech/`                         | Generate the full project voice                |
| POST   | `.../generate-slide-speeches/`                 | Generate one MP3 per slide                     |
| POST   | `.../slides/<id>/generate-speech/`             | Re-generate a single slide's MP3               |

All speech generation endpoints accept the new optional fields:

```json
{
  "provider": "google",                  // or "elevenlabs"; falls back to REEL_TTS_DEFAULT_PROVIDER
  "voice_id": "fr-FR-Standard-F",        // falls back to provider default
  "model_id": "",
  "output_format": "mp3"
}
```

The response payload now also includes:

```json
{
  "speech": {
    "provider": "google",
    "character_count": 1234,
    "cached_count": 2,        // batch endpoints only
    ...
  }
}
```

## Security notes

- `GOOGLE_APPLICATION_CREDENTIALS` is read on the **backend only**. The
  service account JSON never leaves the Django process.
- The frontend never receives any Google credentials — it only knows the
  list of voice IDs.
- API keys/credentials are **never logged**. The `reel_studio.tts`
  logger emits `provider=…  voice=…  chars=…  cached=…` lines but no
  secrets.
- Voice generation is never triggered automatically. The frontend always
  requires an explicit user click on either the "Tester la voix" or
  "Generer les MP3 slides" button.
