"""Courriels du compte et des paiements OptiTAB.

Un seul habillage (`_habiller`) et une fonction par événement. Chaque événement
prévient la personne concernée et, quand c'est utile, l'administration.

Règles :
- aucune fonction ne lève d'exception : un courriel raté ne doit jamais faire
  échouer une inscription ou un paiement (elles renvoient True ou False) ;
- les chiffres internes (nombre d'abonnés...) ne figurent que dans les courriels
  de l'administration ;
- avec la clé Stripe de test (site local), les sujets commencent par « [TEST] ».
"""
import logging

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.utils.html import escape

logger = logging.getLogger(__name__)

SITE_PUBLIC = 'https://www.optitab.net'
ADRESSE_CONTACT = 'contact@optitab.net'
MARINE, ENCRE, ENCRE_DOUCE, GRIS, FOND, FILET = '#1b3c8e', '#121a33', '#2c3550', '#6b7591', '#f1f4fb', '#dfe6f5'
MOIS = ('janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août',
        'septembre', 'octobre', 'novembre', 'décembre')
PERIODES = {'daily': 'par jour', 'weekly': 'par semaine', 'monthly': 'par mois', 'yearly': 'par an'}
ROLES = {'student': 'Élève', 'parent': 'Parent', 'teacher': 'Professeur'}


# ---------------------------------------------------------------- outils
def adresse_admin():
    return getattr(settings, 'ADMIN_NOTIFICATION_EMAIL', '') or ADRESSE_CONTACT


def mode_test():
    from stripe_config import STRIPE_RUNTIME_MODE
    return STRIPE_RUNTIME_MODE != 'live'


def site():
    return (getattr(settings, 'FRONTEND_URL', '') or SITE_PUBLIC).rstrip('/')


def _logo():
    return getattr(settings, 'EMAIL_LOGO_URL', None) or f'{SITE_PUBLIC}/logo-optitab.png'


def prenom(user):
    return (getattr(user, 'first_name', '') or '').strip()


def nom_complet(user):
    nom = f"{getattr(user, 'first_name', '') or ''} {getattr(user, 'last_name', '') or ''}".strip()
    return nom or getattr(user, 'email', '') or 'Compte sans nom'


def classe(niveau):
    if not niveau:
        return ''
    pays = getattr(getattr(niveau, 'pays', None), 'nom', '')
    return f'{niveau.nom} · {pays}' if pays else niveau.nom


def euros(montant):
    return f'{float(montant):.2f}'.replace('.', ',') + ' €'


def date_fr(moment, heure=False):
    if not moment:
        return ''
    local = timezone.localtime(moment) if timezone.is_aware(moment) else moment
    jour = '1er' if local.day == 1 else str(local.day)
    texte = f'{jour} {MOIS[local.month - 1]} {local.year}'
    return f'{texte} à {local:%H} h {local:%M}' if heure else texte


def est_pass(plan):
    return getattr(plan, 'plan_mode', '') == 'one_time'


def prix(plan):
    montant = getattr(plan, 'price', None)
    if not montant:
        return ''
    if est_pass(plan):
        return euros(montant)
    return f"{euros(montant)} {PERIODES.get(getattr(plan, 'billing_period', ''), '')}".strip()


def duree(plan):
    jours = getattr(plan, 'access_days', None)
    return '' if not jours else ('1 jour' if jours == 1 else f'{jours} jours')


def _bonjour(user):
    return f'Bonjour {prenom(user)},' if prenom(user) else 'Bonjour,'


def _lignes(*paires):
    """Garde les lignes dont la valeur n'est pas vide."""
    return [(etiquette, valeur) for etiquette, valeur in paires if valeur not in (None, '')]


# ---------------------------------------------------------------- habillage
def _habiller(titre, paragraphes, details=(), bouton=None, liens=(), note=None, admin=False):
    """Renvoie (texte, html) : logo, titre, texte court, tableau, un bouton, liens, note."""
    texte = [titre, '']
    texte += [p for p in paragraphes] + ([''] if paragraphes else [])
    texte += [f'{e} : {v}' for e, v in details] + ([''] if details else [])
    if bouton:
        texte += [f'{bouton[0]} : {bouton[1]}', '']
    texte += [f'{e} : {u}' for e, u in liens] + ([''] if liens else [])
    if note:
        texte += [note, '']
    texte += ['OptiTAB — notification interne' if admin else "L'équipe OptiTAB", f'{ADRESSE_CONTACT} · www.optitab.net']

    p_style = f'margin:0 0 14px;font-size:15px;line-height:1.6;color:{ENCRE_DOUCE};'
    html = [
        f'<div style="margin:0;padding:24px 12px;background:{FOND};font-family:-apple-system,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif;">',
        '<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="max-width:560px;margin:0 auto;">',
        f'<tr><td style="padding:0 4px 16px;"><a href="{SITE_PUBLIC}" style="text-decoration:none;">'
        f'<img src="{_logo()}" alt="OptiTAB" width="127" height="40" style="display:block;border:0;"></a></td></tr>',
        f'<tr><td style="background:#ffffff;border:1px solid {FILET};border-radius:14px;padding:28px 24px;">',
    ]
    if admin:
        html.append(f'<p style="margin:0 0 8px;font-size:11px;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:{MARINE};">'
                    f'Administration{" · mode test" if mode_test() else ""}</p>')
    html.append(f'<h1 style="margin:0 0 14px;font-size:21px;line-height:1.3;color:{ENCRE};">{escape(titre)}</h1>')
    html += [f'<p style="{p_style}">{escape(p)}</p>' for p in paragraphes]
    if details:
        html.append(f'<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="margin:6px 0 18px;border-top:1px solid {FILET};">')
        for etiquette, valeur in details:
            html.append(
                f'<tr><td style="padding:9px 12px 9px 0;border-bottom:1px solid {FILET};font-size:14px;color:{GRIS};width:42%;vertical-align:top;">{escape(str(etiquette))}</td>'
                f'<td style="padding:9px 0;border-bottom:1px solid {FILET};font-size:14px;font-weight:600;color:{ENCRE};vertical-align:top;">{escape(str(valeur))}</td></tr>')
        html.append('</table>')
    if bouton:
        html.append(f'<p style="margin:4px 0 16px;"><a href="{escape(bouton[1])}" style="display:inline-block;background:{MARINE};color:#ffffff;'
                    f'text-decoration:none;font-weight:600;font-size:15px;padding:12px 22px;border-radius:10px;">{escape(bouton[0])}</a></p>')
    if liens:
        html.append('<p style="margin:0 0 14px;font-size:14px;line-height:1.9;">' + '<br>'.join(
            f'<a href="{escape(u)}" style="color:{MARINE};font-weight:600;text-decoration:none;">{escape(e)} →</a>' for e, u in liens) + '</p>')
    if note:
        html.append(f'<p style="margin:0;font-size:13px;line-height:1.6;color:{GRIS};">{escape(note)}</p>')
    html += [
        '</td></tr>',
        f'<tr><td style="padding:16px 4px 0;font-size:12px;line-height:1.7;color:{GRIS};">OptiTAB · cours de maths et de physique-chimie<br>'
        f'<a href="mailto:{ADRESSE_CONTACT}" style="color:{GRIS};">{ADRESSE_CONTACT}</a> · '
        f'<a href="{SITE_PUBLIC}" style="color:{GRIS};">www.optitab.net</a></td></tr>',
        '</table></div>',
    ]
    return '\n'.join(texte), '\n'.join(html)


def envoyer(a, sujet, titre=None, paragraphes=(), details=(), bouton=None, liens=(), note=None, admin=False):
    """Envoie un courriel habillé. Ne lève jamais d'exception."""
    destinataires = [x for x in ([a] if isinstance(a, str) else list(a or [])) if x]
    if not destinataires:
        return False
    try:
        texte, html = _habiller(titre or sujet, list(paragraphes), list(details), bouton, list(liens), note, admin)
        if mode_test():
            sujet = f'[TEST] {sujet}'
        message = EmailMultiAlternatives(subject=sujet, body=texte, from_email=settings.DEFAULT_FROM_EMAIL, to=destinataires)
        message.attach_alternative(html, 'text/html')
        message.send(fail_silently=False)
        return True
    except Exception:
        logger.exception('Courriel non envoyé : %s', sujet)
        return False


def _etat_des_ventes():
    """Chiffres internes, pour l'administration seulement."""
    from core.services import EmailService
    from subscriptions.models import AccessPass

    stats = EmailService._count_active_subscriptions_on_stripe()
    lignes = [
        ('Abonnements actifs Stripe', EmailService._format_active_subscribers_for_email(stats)),
        ('Passes actifs', AccessPass.objects.filter(ends_at__gt=timezone.now(), is_revoked=False).count()),
        ('Mode Stripe', stats.get('mode_label', 'UNKNOWN')),
    ]
    if stats.get('error_message'):
        lignes.append(('Erreur Stripe', stats['error_message']))
    return lignes


def prevenir_admin(sujet, details=(), paragraphes=(), titre=None, ventes=False, bouton=None):
    """Courriel interne à l'administration."""
    details = list(details)
    if ventes:
        try:
            details += _etat_des_ventes()
        except Exception:
            logger.exception('État des ventes indisponible')
    return envoyer(adresse_admin(), f'[OptiTAB] {sujet}', titre or sujet.split(' : ')[0], paragraphes, details,
                   bouton=bouton, admin=True)


def _fiche(user, plan=None, niveau=None):
    """Lignes communes des courriels internes."""
    return _lignes(
        ('Compte', nom_complet(user)), ('E-mail', getattr(user, 'email', '')),
        ('Offre', getattr(plan, 'name', '') if plan else ''), ('Prix', prix(plan) if plan else ''),
        ('Classe', classe(niveau)),
    )


def _gerer():
    return ('Gérer mon abonnement', f'{site()}/subscription')


# ================================================================ COMPTE
def verification_adresse(user, lien):
    return envoyer(
        user.email, 'Confirme ton adresse e-mail',
        paragraphes=[_bonjour(user), 'Bienvenue sur OptiTAB ! Pour activer ton compte, confirme ton adresse e-mail.'],
        bouton=('Confirmer mon adresse', lien),
        note="Si tu n'es pas à l'origine de cette inscription, ignore ce message.")


def changement_adresse(user, nouvelle_adresse, lien):
    return envoyer(
        nouvelle_adresse, 'Confirme ta nouvelle adresse e-mail',
        paragraphes=[_bonjour(user), 'Tu as demandé à utiliser cette adresse pour ton compte OptiTAB. Confirme-la pour terminer le changement.'],
        bouton=('Confirmer cette adresse', lien),
        note="Si tu n'as rien demandé, ignore ce message : ton adresse actuelle reste inchangée.")


def mot_de_passe_oublie(user, lien):
    return envoyer(
        user.email, 'Choisis un nouveau mot de passe',
        paragraphes=[_bonjour(user), 'Tu as demandé à changer le mot de passe de ton compte OptiTAB.'],
        bouton=('Choisir un nouveau mot de passe', lien),
        note="Ce lien ne fonctionne qu'une fois et expire dans 24 heures. Si tu n'as rien demandé, ignore ce message : ton mot de passe ne change pas.")


def bienvenue(user):
    """Compte créé sans courriel de vérification (connexion Google)."""
    return envoyer(
        user.email, 'Bienvenue sur OptiTAB',
        paragraphes=[_bonjour(user), 'Ton compte est créé. Tu peux dès maintenant ouvrir ton espace et commencer à réviser.'],
        bouton=('Ouvrir mon espace', f'{site()}/dashboard'))


def bienvenue_apres_achat(user, lien):
    """Compte créé par un achat sans connexion : il reste à choisir un mot de passe."""
    return envoyer(
        user.email, 'Bienvenue sur OptiTAB : choisis ton mot de passe',
        titre='Bienvenue sur OptiTAB',
        paragraphes=[_bonjour(user), f'Ton paiement est confirmé et ton compte est créé avec l’adresse {user.email}.',
                     'Il te reste à choisir ton mot de passe pour te connecter.'],
        bouton=('Choisir mon mot de passe', lien),
        note="Ce lien ne fonctionne qu'une fois et expire dans 24 heures.")


def compte_enfant_cree(enfant, mot_de_passe, parent):
    return envoyer(
        enfant.email, 'Ton compte OptiTAB est créé',
        paragraphes=[_bonjour(enfant), f'{nom_complet(parent)} t’a créé un compte OptiTAB pour t’aider dans tes révisions.'],
        details=[('Adresse e-mail', enfant.email), ('Mot de passe provisoire', mot_de_passe)],
        bouton=('Me connecter', f'{site()}/dashboard'),
        note='Change ton mot de passe après ta première connexion, dans « Mon compte ».')


def nouveau_compte_admin(user):
    from django.contrib.auth import get_user_model
    return prevenir_admin(
        f'Nouveau compte : {nom_complet(user)}',
        _lignes(('Compte', nom_complet(user)), ('E-mail', user.email),
                ('Rôle', ROLES.get(getattr(user, 'role', ''), getattr(user, 'role', ''))),
                ('Classe', classe(getattr(user, 'niveau_pays', None))),
                ('Créé le', date_fr(getattr(user, 'date_joined', None), heure=True)),
                ('Nombre de comptes', get_user_model().objects.count())))


# ================================================================ ACHAT
def achat(user, plan, niveau=None, lien_facture=None):
    """Abonnement ou pass acheté pour soi."""
    un_pass = est_pass(plan)
    liens = ([('Télécharger ma facture', lien_facture)] if lien_facture else []) + [_gerer()]
    return envoyer(
        user.email, f"Ton {'pass' if un_pass else 'abonnement'} OptiTAB est activé",
        paragraphes=[_bonjour(user), 'Merci pour ta confiance ! Ton accès est ouvert dès maintenant.'],
        details=_lignes(('Offre', plan.name), ('Classe', classe(niveau)), ('Montant', prix(plan)),
                        ('Durée', duree(plan) if un_pass else ''),
                        ('Renouvellement', '' if un_pass else 'automatique, résiliable à tout moment')),
        bouton=('Ouvrir mon espace', f'{site()}/dashboard'), liens=liens)


def cadeau_recu(beneficiaire, payeur, plan, niveau=None):
    return envoyer(
        beneficiaire.email, 'Tu as reçu un accès OptiTAB',
        paragraphes=[_bonjour(beneficiaire), f'{nom_complet(payeur)} t’offre un accès à OptiTAB. Il est déjà ouvert : tu peux commencer tout de suite.'],
        details=_lignes(('Offre', plan.name), ('Classe', classe(niveau)), ('Durée', duree(plan) if est_pass(plan) else '')),
        bouton=('Ouvrir mon espace', f'{site()}/dashboard'))


def cadeau_confirme(payeur, beneficiaire, plan, niveau=None, lien_facture=None):
    liens = ([('Télécharger ma facture', lien_facture)] if lien_facture else []) + [_gerer()]
    return envoyer(
        payeur.email, 'Ton cadeau OptiTAB est activé',
        paragraphes=[_bonjour(payeur), f'Merci ! L’accès offert à {nom_complet(beneficiaire)} est ouvert dès maintenant.'],
        details=_lignes(('Pour', nom_complet(beneficiaire)), ('Offre', plan.name), ('Classe', classe(niveau)),
                        ('Montant', prix(plan)), ('Durée', duree(plan) if est_pass(plan) else ''),
                        ('Renouvellement', '' if est_pass(plan) else 'automatique, résiliable à tout moment')),
        liens=liens)


def achat_admin(user, plan, niveau=None, cadeau=False, payeur=None):
    from subscriptions.models import UserSubscription
    if est_pass(plan):
        genre = 'Achat de pass'
    elif niveau and UserSubscription.objects.filter(user=user, niveau_pays=niveau, status='canceled').exists():
        genre = 'Réabonnement'
    else:
        genre = 'Nouvel abonnement'
    details = _fiche(user, plan, niveau)
    if cadeau and payeur:
        details += [('Cadeau offert par', f'{nom_complet(payeur)} ({payeur.email})')]
    return prevenir_admin(f'{genre} : {nom_complet(user)} – {plan.name}', details, ventes=True)


def renouvellement(user, plan, niveau=None, lien_facture=None, paiement=None):
    liens = ([('Télécharger ma facture', lien_facture)] if lien_facture else []) + [_gerer()]
    montant = euros(paiement.amount) if paiement is not None and getattr(paiement, 'amount', None) else prix(plan)
    return envoyer(
        user.email, 'Ton abonnement OptiTAB a été renouvelé',
        paragraphes=[_bonjour(user), 'Ton abonnement a été renouvelé : ton accès continue sans interruption.'],
        details=_lignes(('Offre', plan.name), ('Classe', classe(niveau)), ('Montant payé', montant),
                        ('Prochaine échéance', date_fr(getattr(paiement, 'period_end', None)))),
        liens=liens)


def renouvellement_admin(user, plan, niveau=None, paiement=None):
    details = _fiche(user, plan, niveau)
    if paiement is not None and getattr(paiement, 'amount', None):
        details += [('Montant encaissé', euros(paiement.amount))]
    return prevenir_admin(f'Renouvellement : {nom_complet(user)} – {plan.name}', details, ventes=True)


def facture(user, paiement, lien):
    return envoyer(
        user.email, 'Ta facture OptiTAB',
        paragraphes=[_bonjour(user), 'Voici la facture de ton paiement.'],
        details=_lignes(('Montant', euros(paiement.amount) if getattr(paiement, 'amount', None) else ''),
                        ('Date', date_fr(getattr(paiement, 'created_at', None)))),
        bouton=('Télécharger ma facture', lien), liens=[_gerer()])


# ================================================================ VIE DE L'ABONNEMENT
def paiement_refuse(abonnement, facture_stripe):
    """Carte refusée au renouvellement : le payeur et l'administration sont prévenus."""
    payeur = (facture_stripe.get('customer_email') or '').strip() or abonnement.user.email
    montant = euros((facture_stripe.get('amount_due') or 0) / 100)
    lien = facture_stripe.get('hosted_invoice_url') or f'{site()}/subscription'
    offre = getattr(abonnement.plan, 'name', 'OptiTAB')
    client = envoyer(
        payeur, 'Ton paiement OptiTAB n’est pas passé',
        paragraphes=['Bonjour,', f'Le prélèvement de {montant} pour ton abonnement OptiTAB a été refusé par la banque.',
                     'Pour garder ton accès, règle la facture avec une autre carte.'],
        details=_lignes(('Offre', offre), ('Classe', classe(abonnement.niveau_pays)), ('Montant', montant)),
        bouton=('Régler ma facture', lien),
        note='Ton accès reste ouvert 3 jours, le temps de régler. Sans règlement, l’abonnement s’arrêtera après quelques nouvelles tentatives.')
    prevenir_admin(f'Carte refusée : {nom_complet(abonnement.user)} – {offre}',
                   _fiche(abonnement.user, abonnement.plan, abonnement.niveau_pays) + [('Montant refusé', montant), ('Payeur', payeur)],
                   paragraphes=['Le client a reçu le lien pour régler. Stripe refera quelques tentatives avant d’arrêter l’abonnement.'])
    return client


def resiliation(user, plan, niveau=None, fin=None, programmee=True, beneficiaire=None):
    offre = getattr(plan, 'name', 'OptiTAB')
    pour = f' offert à {nom_complet(beneficiaire)}' if beneficiaire else ''
    if programmee:
        return envoyer(
            user.email, 'Ta résiliation est enregistrée',
            paragraphes=[_bonjour(user), f'L’abonnement {offre}{pour} ne sera pas renouvelé.',
                         (f'L’accès reste ouvert jusqu’au {date_fr(fin)}.' if fin else 'L’accès reste ouvert jusqu’à la fin de la période payée.')
                         + ' Tu changes d’avis ? Tu peux le réactiver d’ici là.'],
            details=_lignes(('Offre', offre), ('Classe', classe(niveau)), ('Fin de l’accès', date_fr(fin))),
            bouton=_gerer())
    return envoyer(
        user.email, 'Ton abonnement OptiTAB est terminé',
        paragraphes=[_bonjour(user), f'L’abonnement {offre}{pour} est terminé. Aucun nouveau prélèvement ne sera fait.',
                     'Tu peux reprendre un accès quand tu veux.'],
        details=_lignes(('Offre', offre), ('Classe', classe(niveau)), ('Terminé le', date_fr(fin or timezone.now()))),
        bouton=('Voir les offres', f'{site()}/tarifs'))


def resiliation_admin(user, plan, niveau=None, fin=None, programmee=True, beneficiaire=None):
    genre = 'Résiliation programmée' if programmee else 'Abonnement terminé'
    details = _fiche(user, plan, niveau) + _lignes(('Fin de l’accès', date_fr(fin)))
    if beneficiaire:
        details += [('Bénéficiaire (cadeau)', f'{nom_complet(beneficiaire)} ({beneficiaire.email})')]
    return prevenir_admin(f"{genre} : {nom_complet(user)} – {getattr(plan, 'name', '')}", details, ventes=True)


def reactivation(user, abonnement=None):
    """Résiliation annulée : le client et l'administration sont prévenus."""
    plan = getattr(abonnement, 'plan', None)
    niveau = getattr(abonnement, 'niveau_pays', None)
    fin = getattr(abonnement, 'current_period_end', None)
    client = envoyer(
        user.email, 'Ton abonnement OptiTAB continue',
        paragraphes=[_bonjour(user), 'Ta résiliation est annulée : ton abonnement continue normalement.'],
        details=_lignes(('Offre', getattr(plan, 'name', '')), ('Classe', classe(niveau)), ('Prochain prélèvement', date_fr(fin))),
        bouton=_gerer())
    prevenir_admin(f"Réactivation : {nom_complet(user)} – {getattr(plan, 'name', 'abonnement')}",
                   _fiche(user, plan, niveau) + _lignes(('Prochain prélèvement', date_fr(fin))), ventes=True)
    return client


def changement_offre(user, ancienne, nouvelle, niveau=None, echeance=None):
    client = envoyer(
        user.email, 'Ton abonnement OptiTAB a changé',
        paragraphes=[_bonjour(user), f'Ton abonnement passe de « {ancienne.name} » à « {nouvelle.name} ».',
                     'Le nouveau tarif s’applique à partir de la prochaine échéance.'],
        details=_lignes(('Nouvelle offre', nouvelle.name), ('Nouveau tarif', prix(nouvelle)), ('Classe', classe(niveau)),
                        ('Prochaine échéance', date_fr(echeance))),
        bouton=_gerer())
    prevenir_admin(f'Changement d’offre : {nom_complet(user)} – {nouvelle.name}',
                   _fiche(user, nouvelle, niveau) + [('Ancienne offre', ancienne.name)])
    return client


def pass_expire(user, access_pass, niveau=None):
    return envoyer(
        user.email, 'Ton pass OptiTAB est terminé',
        paragraphes=[_bonjour(user), 'Ton pass est arrivé à son terme. Pour continuer à réviser, tu peux reprendre un pass ou un abonnement.'],
        details=_lignes(('Offre', getattr(access_pass.plan, 'name', '')), ('Classe', classe(niveau)),
                        ('Terminé le', date_fr(access_pass.ends_at, heure=True))),
        bouton=('Voir les offres', f'{site()}/tarifs'))


def pass_expire_admin(user, access_pass, niveau=None):
    return prevenir_admin(f"Pass expiré : {nom_complet(user)} – {getattr(access_pass.plan, 'name', '')}",
                          _fiche(user, access_pass.plan, niveau) + _lignes(('Terminé le', date_fr(access_pass.ends_at, heure=True))),
                          ventes=True)


# ================================================================ ARGENT RENDU
def remboursement(user, montant, libelle='', total=True, acces_ferme=False):
    client = envoyer(
        user.email, 'Ton remboursement OptiTAB',
        paragraphes=[_bonjour(user), f'Nous t’avons remboursé {euros(montant)}. La somme apparaît sur ton compte bancaire sous 5 à 10 jours.']
        + (['L’accès correspondant est maintenant fermé.'] if acces_ferme else []),
        details=_lignes(('Achat', libelle), ('Montant remboursé', euros(montant)),
                        ('Remboursement', 'total' if total else 'partiel')))
    prevenir_admin(f'Remboursement : {nom_complet(user)} – {euros(montant)}',
                   _lignes(('Compte', nom_complet(user)), ('E-mail', user.email), ('Achat', libelle),
                           ('Montant remboursé', euros(montant)), ('Remboursement', 'total' if total else 'partiel'),
                           ('Accès', 'fermé' if acces_ferme else 'inchangé')))
    return client


def achat_en_double(user, plan, niveau=None, reference=''):
    client = envoyer(
        user.email, 'Ton paiement en double a été remboursé',
        paragraphes=[_bonjour(user), f'Tu as déjà accès à cette classe sur OptiTAB. Le paiement que tu viens de faire ({plan.name}) faisait donc double emploi.',
                     'Nous l’avons annulé et remboursé en totalité. La somme apparaît sur ton compte bancaire sous 5 à 10 jours.',
                     'Pour retrouver ton accès, connecte-toi avec cette adresse e-mail.'],
        details=_lignes(('Offre', plan.name), ('Classe', classe(niveau))),
        bouton=('Ouvrir mon espace', f'{site()}/dashboard'))
    prevenir_admin(f'Achat en double remboursé : {nom_complet(user)} – {plan.name}',
                   _fiche(user, plan, niveau) + _lignes(('Paiement', reference)),
                   paragraphes=['Achat fait sans connexion pour une classe déjà ouverte : annulé et remboursé automatiquement.'])
    return client


def litige(montant, motif='', reference='', user=None):
    details = _lignes(('Compte', nom_complet(user) if user else ''), ('E-mail', getattr(user, 'email', '') if user else ''),
                      ('Montant contesté', euros(montant)), ('Motif', motif or 'non précisé'), ('Litige', reference))
    return prevenir_admin(
        f'Litige bancaire : {euros(montant)}', details,
        paragraphes=['Un client a contesté un paiement auprès de sa banque. L’accès correspondant a été coupé automatiquement.',
                     'Réponds au litige dans le tableau de bord Stripe : Paiements > Litiges.'])


def versement_cours(paiement, rembourse=False):
    """Versement pour un cours particulier, reçu ou remboursé (administration)."""
    genre = 'Versement remboursé' if rembourse else 'Versement reçu'
    return prevenir_admin(
        f'{genre} (cours particulier) : {euros(paiement.amount)}',
        _lignes(('Montant', euros(paiement.amount)), ('Libellé', paiement.label), ('Payeur', paiement.payer_name),
                ('E-mail', paiement.payer_email), ('Date', date_fr(paiement.paid_at or paiement.created_at, heure=True))))


def message_stripe_non_traite(type_evenement, identifiant, erreur):
    return prevenir_admin(
        f'Message Stripe non traité : {type_evenement}',
        [('Message', type_evenement), ('Identifiant', identifiant), ('Erreur', str(erreur)[:300])],
        paragraphes=['Stripe va renvoyer ce message automatiquement pendant 3 jours.',
                     'Si l’alerte se répète, regarde les journaux du serveur (Render) et Stripe > Développeurs > Webhooks.'])
