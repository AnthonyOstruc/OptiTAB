"""Versements ponctuels pour cours particuliers.

Le professeur envoie un lien, la personne saisit le montant et paie.
Pas de compte, pas d'abonnement, pas d'acces plateforme : un encaissement.

Le montant provient du navigateur : il est donc revalide ici avant toute
creation de session Stripe. Aucune borne cote client ne fait autorite.
"""
import logging
import os
from decimal import Decimal, InvalidOperation

from django.http import JsonResponse
from django.utils import timezone
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle

from stripe_config import CANCEL_URL, FRONTEND_BASE_URL
from .models import LessonPayment
from .stripe_client import stripe, stripe_error

logger = logging.getLogger(__name__)

# Bornes de securite. Un endpoint public qui accepte n'importe quel montant
# invite aux essais de carte volee (petits montants) comme aux erreurs de
# saisie (un zero de trop). Ajustables par variables d'environnement.
MIN_AMOUNT = Decimal(os.getenv('LESSON_PAYMENT_MIN_EUR', '5'))
MAX_AMOUNT = Decimal(os.getenv('LESSON_PAYMENT_MAX_EUR', '500'))

SUCCESS_PATH = '/paiement/merci'


class LessonPaymentThrottle(AnonRateThrottle):
    """Limite les creations de session par IP.

    Un endpoint de paiement ouvert sans authentification est une cible pour
    valider des numeros de carte voles en masse. Les bornes de montant ne
    suffisent pas : c'est le nombre de tentatives qu'il faut brider.

    30/heure et non 10 : une saisie maladroite (montant hors bornes, virgule
    mal placee) consomme un jeton alors qu'elle n'atteint jamais Stripe. Trop
    bas, on bloque un client legitime qui tatonne. Ce qu'on veut arreter, ce
    sont des centaines de tentatives, pas une dizaine.

    Attention : avec LocMemCache, le compteur est par processus. Sous gunicorn
    avec N workers, la limite reelle est de 30 x N. Un cache partage (Redis)
    serait necessaire pour une limite stricte.
    """

    scope = 'lesson_payment'
    rate = '30/hour'


def _demander_recu_stripe(payment_intent_id, email):
    """Declenche l'envoi du recu Stripe au payeur.

    Stripe n'envoie rien tant que `receipt_email` est vide sur le paiement :
    Checkout collecte bien l'adresse, mais ne la reporte pas automatiquement.
    En mode live, renseigner ce champ declenche l'envoi quels que soient les
    reglages du Dashboard. En mode test, Stripe n'ecrit qu'a l'adresse du
    titulaire du compte : ne pas s'inquieter de ne rien recevoir en essai.
    """
    if not payment_intent_id or not email:
        return
    try:
        stripe.PaymentIntent.modify(payment_intent_id, receipt_email=email)
    except stripe_error.StripeError as exc:
        # Le paiement est encaisse : un recu non parti ne doit rien casser.
        logger.warning('Versement cours : envoi du recu impossible (%s) : %s',
                       payment_intent_id, exc)


def _parse_amount(raw):
    """Renvoie (montant, erreur). Le montant est arrondi au centime."""
    if raw is None or str(raw).strip() == '':
        return None, 'Indiquez le montant à régler.'

    normalized = str(raw).strip().replace(',', '.').replace(' ', '')
    try:
        amount = Decimal(normalized)
    except (InvalidOperation, ValueError):
        return None, 'Montant invalide.'

    if not amount.is_finite():
        return None, 'Montant invalide.'

    amount = amount.quantize(Decimal('0.01'))

    if amount < MIN_AMOUNT:
        return None, f'Le montant minimum est de {MIN_AMOUNT:.0f} €.'
    if amount > MAX_AMOUNT:
        return None, f'Le montant maximum est de {MAX_AMOUNT:.0f} €.'

    return amount, None


@api_view(['GET'])
@permission_classes([AllowAny])
def lesson_payment_config(request):
    """Bornes affichees par le formulaire. La verification reste serveur."""
    return Response({
        'min_amount': float(MIN_AMOUNT),
        'max_amount': float(MAX_AMOUNT),
        'currency': 'EUR',
    })


@api_view(['POST'])
@permission_classes([AllowAny])
@throttle_classes([LessonPaymentThrottle])
def lesson_payment_create_session(request):
    """Cree une session Stripe Checkout au montant saisi."""
    amount, error = _parse_amount(request.data.get('amount'))
    if error:
        return JsonResponse({'error': error}, status=400)

    label = str(request.data.get('label') or '').strip()[:140]
    payer_name = str(request.data.get('payer_name') or '').strip()[:120]

    # Sur la page Stripe, le nom du produit s'affiche au-dessus du montant et
    # la description en dessous. Mettre la saisie du client en nom donnait
    # « esssss » en titre et un texte generique en sous-titre : on inverse.
    product_name = 'Cours particulier — OptiTAB'

    try:
        session = stripe.checkout.Session.create(
            mode='payment',
            payment_method_types=['card'],
            line_items=[{
                'quantity': 1,
                'price_data': {
                    'currency': 'eur',
                    # Stripe raisonne en centimes : un arrondi flottant ici
                    # ferait payer un centime de trop ou de moins.
                    'unit_amount': int(amount * 100),
                    'product_data': {
                        'name': product_name,
                        # Pas de description generique quand le client n'a rien
                        # precise : mieux vaut rien qu'une ligne sans contenu.
                        **({'description': label} if label else {}),
                    },
                },
            }],
            success_url=(
                f'{FRONTEND_BASE_URL}{SUCCESS_PATH}?session_id={{CHECKOUT_SESSION_ID}}'
            ),
            cancel_url=CANCEL_URL,
            locale='fr',
            # Le bouton affiche « Payer » plutot que le libelle par defaut.
            submit_type='pay',
            metadata={
                # Marqueur lu par le webhook pour ne pas confondre ce
                # versement avec l'achat d'un pass ou d'un abonnement.
                'kind': 'lesson_payment',
                'label': product_name,
                'payer_name': payer_name,
            },
            custom_text={
                'submit': {'message': 'Un reçu vous sera envoyé par email.'}
            },
        )
    except stripe_error.StripeError as exc:
        logger.error('Versement cours : creation de session refusee par Stripe : %s', exc)
        return JsonResponse(
            {'error': "Le paiement n'a pas pu être initialisé. Réessayez dans un instant."},
            status=502,
        )

    LessonPayment.objects.create(
        amount=amount,
        label=label,
        payer_name=payer_name,
        stripe_session_id=session.id,
    )

    return JsonResponse({'url': session.url, 'session_id': session.id})


@api_view(['GET'])
@permission_classes([AllowAny])
def lesson_payment_status(request):
    """Etat d'un versement, pour la page de confirmation.

    On interroge Stripe plutot que de se fier a notre base : le webhook peut
    n'etre pas encore arrive quand le client revient de la page de paiement.
    """
    session_id = str(request.GET.get('session_id') or '').strip()
    if not session_id:
        return JsonResponse({'error': 'Session manquante.'}, status=400)

    try:
        payment = LessonPayment.objects.get(stripe_session_id=session_id)
    except LessonPayment.DoesNotExist:
        return JsonResponse({'error': 'Versement introuvable.'}, status=404)

    if payment.status != 'paid':
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            if session.get('payment_status') == 'paid':
                details = session.get('customer_details') or {}
                if payment.mark_paid(
                    payment_intent_id=session.get('payment_intent'),
                    payer_email=details.get('email') or '',
                    payer_name=details.get('name') or '',
                ):
                    _demander_recu_stripe(
                        payment.stripe_payment_intent_id, payment.payer_email
                    )
        except stripe_error.StripeError as exc:
            logger.warning('Versement cours : statut Stripe illisible (%s) : %s', session_id, exc)

    return JsonResponse({
        'status': payment.status,
        'paid': payment.status == 'paid',
        'amount': float(payment.amount),
        'label': payment.label,
        'payer_name': payment.payer_name,
    })


def handle_lesson_payment_completed(session):
    """Appele par le webhook sur checkout.session.completed."""
    session_id = session.get('id')
    if not session_id:
        return

    try:
        payment = LessonPayment.objects.get(stripe_session_id=session_id)
    except LessonPayment.DoesNotExist:
        logger.warning('Versement cours : session %s inconnue en base.', session_id)
        return

    details = session.get('customer_details') or {}
    if payment.mark_paid(
        payment_intent_id=session.get('payment_intent'),
        payer_email=details.get('email') or '',
        payer_name=details.get('name') or '',
    ):
        _demander_recu_stripe(payment.stripe_payment_intent_id, payment.payer_email)
        logger.info('Versement cours confirme : %s€ (%s)', payment.amount, session_id)


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_lesson_payments(request):
    """Liste des versements, pour le suivi cote administration."""
    queryset = LessonPayment.objects.all()[:200]

    total_paid = sum(
        (p.amount for p in LessonPayment.objects.filter(status='paid')),
        Decimal('0'),
    )

    return Response({
        'total_paid': float(total_paid),
        'payments': [
            {
                'id': p.id,
                'amount': float(p.amount),
                'label': p.label,
                'payer_name': p.payer_name,
                'payer_email': p.payer_email,
                'status': p.status,
                'status_display': p.get_status_display(),
                'created_at': p.created_at.isoformat(),
                'paid_at': p.paid_at.isoformat() if p.paid_at else None,
            }
            for p in queryset
        ],
    })
