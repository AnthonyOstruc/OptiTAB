"""
Vue pour l'authentification Google One Tap
Gère la connexion et l'inscription automatique via Google
"""

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.google.provider import GoogleProvider
from django.contrib.auth import get_user_model
from django.conf import settings
import logging
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import requests

from core.services import ResponseService

User = get_user_model()
logger = logging.getLogger(__name__)


class GoogleLoginView(APIView):
    """
    Auth One Tap/ID Token: reçoit un `access_token` (id_token JWT Google),
    vérifie sa validité côté Google, crée l'utilisateur si nécessaire,
    puis renvoie des tokens JWT applicatifs (access/refresh).
    """

    permission_classes = [AllowAny]
    authentication_classes = []  # Pas d'auth/CSRF pour ce POST public

    def post(self, request):
        try:
            id_token_from_client = request.data.get('access_token') or request.data.get('id_token')
            if not id_token_from_client:
                return ResponseService.error(
                    message="Token Google manquant",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            client_id = settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
            # Vérifier le token auprès de Google
            idinfo = id_token.verify_oauth2_token(
                id_token_from_client,
                google_requests.Request(),
                client_id
            )

            # idinfo contient: email, email_verified, given_name, family_name, sub (user id), picture, ...
            if not idinfo.get('email_verified', True):
                return ResponseService.error(
                    message="Email Google non vérifié",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            email = idinfo.get('email')
            first_name = idinfo.get('given_name') or ''
            last_name = idinfo.get('family_name') or ''
            google_uid = idinfo.get('sub')

            # Créer ou récupérer l'utilisateur
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True,
                }
            )

            # S'assurer qu'un SocialAccount existe (liaison Google)
            # Lier un SocialAccount léger, sans passer par le flow complet allauth
            SocialAccount.objects.get_or_create(
                user=user,
                provider=GoogleProvider.id,
                uid=google_uid,
                defaults={'extra_data': idinfo}
            )

            # Générer tokens JWT applicatifs
            refresh = RefreshToken.for_user(user)

            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': getattr(user, 'role', 'student'),
                'is_active': user.is_active,
            }

            logger.info(f"Connexion Google réussie: {user.email} (created={created})")

            return ResponseService.success(
                message="Connexion Google réussie",
                data={
                    'user': user_data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            )

        except ValueError:
            return ResponseService.error(
                message="Token Google invalide",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f"Erreur lors de la connexion Google: {e}")
            return ResponseService.error(
                message="Erreur lors de la connexion Google",
                status_code=status.HTTP_400_BAD_REQUEST
            )


class GoogleOAuthCodeExchangeView(APIView):
    """
    Echange un `authorization code` Google OAuth 2.0 (GSI Code Flow) contre un id_token,
    puis connecte/crée l'utilisateur et renvoie des JWT applicatifs.

    Utilisé comme fallback en navigation privée/incognito lorsque FedCM échoue.
    """

    permission_classes = [AllowAny]
    authentication_classes = []

    def post(self, request):
        try:
            code = request.data.get('code')
            if not code:
                return ResponseService.error(
                    message="Code OAuth manquant",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            # Utiliser le client_id fourni par le front si présent, sinon celui de la config
            client_id = request.data.get('client_id') or settings.SOCIALACCOUNT_PROVIDERS['google']['APP']['client_id']
            client_secret = settings.SOCIALACCOUNT_PROVIDERS['google']['APP'].get('secret')

            token_endpoint = 'https://oauth2.googleapis.com/token'
            payload = {
                'code': code,
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'authorization_code',
                # Avec GSI Code Flow en popup, l'URI est toujours 'postmessage'
                'redirect_uri': 'postmessage',
            }

            resp = requests.post(token_endpoint, data=payload, timeout=10)
            if resp.status_code != 200:
                # Certains environnements (apps GSI sans secret côté front) acceptent l'échange sans client_secret
                # Tenter un second essai sans le secret si le premier échoue
                payload_no_secret = payload.copy()
                payload_no_secret.pop('client_secret', None)
                resp2 = requests.post(token_endpoint, data=payload_no_secret, timeout=10)
                if resp2.status_code != 200:
                    # Retourner un message plus verbeux au client pour debug
                    detail = None
                    try:
                        detail = resp2.json()
                    except Exception:
                        detail = resp2.text or resp.text
                    logging.error(f"Google token exchange failed: {resp.status_code}/{resp2.status_code} {detail}")
                    return ResponseService.error(
                        message="Échec de l'échange du code Google",
                        status_code=status.HTTP_400_BAD_REQUEST,
                        extra={ 'google_error': detail }
                    )
                resp = resp2

            token_data = resp.json()
            google_id_token = token_data.get('id_token')
            if not google_id_token:
                # Retourner un message plus explicite côté client pour debug
                return ResponseService.error(
                    message="id_token manquant après l'échange. Vérifiez client_id/secret et l'activation de l'API OAuth.",
                    status_code=status.HTTP_400_BAD_REQUEST,
                    extra={ 'token_data': token_data }
                )

            # Vérifier le id_token
            idinfo = id_token.verify_oauth2_token(
                google_id_token,
                google_requests.Request(),
                client_id
            )

            if not idinfo.get('email_verified', True):
                return ResponseService.error(
                    message="Email Google non vérifié",
                    status_code=status.HTTP_400_BAD_REQUEST
                )

            email = idinfo.get('email')
            first_name = idinfo.get('given_name') or ''
            last_name = idinfo.get('family_name') or ''
            google_uid = idinfo.get('sub')

            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'first_name': first_name,
                    'last_name': last_name,
                    'is_active': True,
                }
            )

            SocialAccount.objects.get_or_create(
                user=user,
                provider=GoogleProvider.id,
                uid=google_uid,
                defaults={'extra_data': idinfo}
            )

            refresh = RefreshToken.for_user(user)
            user_data = {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': getattr(user, 'role', 'student'),
                'is_active': user.is_active,
            }

            return ResponseService.success(
                message="Connexion Google réussie",
                data={
                    'user': user_data,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            )

        except Exception as e:
            logger.error(f"Erreur lors de l'échange du code Google: {e}")
            return ResponseService.error(
                message="Erreur lors de la connexion Google",
                status_code=status.HTTP_400_BAD_REQUEST
            )