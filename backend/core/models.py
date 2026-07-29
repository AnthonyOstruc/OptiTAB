"""
Modèles de base ultra-simplifiés avec gestionnaires optimisés
"""
from django.db import models
from django.utils import timezone
import uuid
from .services import BaseManager


class BaseModel(models.Model):
    """Modèle de base avec timestamps et statut actif"""
    est_actif = models.BooleanField(default=True, verbose_name="Actif")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")
    date_modification = models.DateTimeField(auto_now=True, verbose_name="Modifié le")
    
    objects = BaseManager()
    
    class Meta:
        abstract = True


class BaseContent(BaseModel):
    """Pour le contenu avec titre et ordre"""
    titre = models.CharField(max_length=200, verbose_name="Titre")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        abstract = True
        ordering = ['ordre', 'titre']
    
    def __str__(self):
        return self.titre


class BaseSimple(BaseModel):
    """Pour le contenu simple - nom et ordre seulement"""
    nom = models.CharField(max_length=100, verbose_name="Nom")
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre")
    
    class Meta:
        abstract = True
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom


class BaseEducational(BaseContent):
    """Pour le contenu éducatif (cours, exercices, quiz)"""
    DIFFICULTY_CHOICES = [
        ('easy', 'Facile'),
        ('medium', 'Moyen'), 
        ('hard', 'Difficile'),
    ]
    
    contenu = models.TextField(verbose_name="Contenu")
    difficulty = models.CharField(
        max_length=10, 
        choices=DIFFICULTY_CHOICES, 
        default='medium',
        verbose_name="Difficulté"
    )
    
    class Meta:
        abstract = True


class BaseOrganizational(BaseContent):
    """Pour l'organisation (matières, thèmes, chapitres)"""
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    couleur = models.CharField(max_length=7, default='#3b82f6', verbose_name="Couleur")
    svg_icon = models.TextField(blank=True, null=True, verbose_name="Icône SVG")
    
    class Meta:
        abstract = True


class NewsletterSubscriber(BaseModel):
    """Abonnés à la newsletter avec lien de désinscription.

    - Utilise `est_actif` hérité pour l'état d'abonnement (True = abonné)
    - Conserve un `unsubscribe_token` unique pour les liens dans les emails
    - Garde des métadonnées utiles (source, IP, timestamps)
    """

    email = models.EmailField(unique=True, verbose_name="Email")
    first_name = models.CharField(max_length=120, blank=True, default="", verbose_name="Prénom")
    last_name = models.CharField(max_length=120, blank=True, default="", verbose_name="Nom")
    source = models.CharField(max_length=50, default='website', verbose_name="Source")
    unsubscribe_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, verbose_name="Jeton de désinscription")
    unsubscribed_at = models.DateTimeField(null=True, blank=True, verbose_name="Désabonné le")
    last_email_sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Dernier email envoyé")
    consent_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP de consentement")

    objects = BaseManager()

    class Meta:
        verbose_name = "Abonné newsletter"
        verbose_name_plural = "Abonnés newsletter"
        ordering = ['-date_creation']

    def __str__(self):
        return self.email

    # Helpers
    def mark_unsubscribed(self, save=True):
        self.est_actif = False
        self.unsubscribed_at = timezone.now()
        if save:
            self.save(update_fields=['est_actif', 'unsubscribed_at', 'date_modification'])

    def reactivate(self, save=True):
        self.est_actif = True
        self.unsubscribed_at = None
        if save:
            self.save(update_fields=['est_actif', 'unsubscribed_at', 'date_modification'])


class DiagnosticLead(BaseModel):
    """Lead capturé sur la landing /diagnostic-maths-gratuit.

    - Stocke les réponses du formulaire (prénom, email, niveau, difficulté)
    - Garde la trace du consentement RGPD (case opt-in marketing, IP, timestamp)
    - Conserve le contexte d'acquisition (UTM, gclid, referrer, landing_path)
    - Peut être lié à un NewsletterSubscriber si l'opt-in marketing a été coché
    """

    LEVEL_CHOICES = [
        ('college', 'Collège'),
        ('seconde', 'Seconde'),
        ('premiere', 'Première'),
        ('terminale', 'Terminale'),
        ('prepa', 'Prépa'),
        ('bts', 'BTS'),
        ('parent', 'Parent'),
    ]

    DIFFICULTY_CHOICES = [
        ('cours_vs_exercices', 'Comprend le cours mais pas les exercices'),
        ('organisation', 'Organisation / révision'),
        ('methode', 'Pas de méthode claire'),
        ('bac', 'Préparation Bac'),
        ('motivation', 'Motivation'),
        ('autre', 'Autre (texte libre)'),
    ]

    FORM_LOCATION_CHOICES = [
        ('hero', 'Hero'),
        ('main', 'Formulaire principal'),
        ('final', 'CTA final'),
    ]

    # Champs formulaire
    email = models.EmailField(db_index=True, verbose_name="Email")
    first_name = models.CharField(max_length=120, blank=True, default="", verbose_name="Prénom")
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, db_index=True, verbose_name="Niveau")
    difficulty = models.CharField(max_length=30, choices=DIFFICULTY_CHOICES, db_index=True, verbose_name="Difficulté principale")
    difficulty_other = models.TextField(max_length=1000, blank=True, default="", verbose_name="Difficulté précisée (texte libre)")

    # Consentement RGPD
    consent_email_marketing = models.BooleanField(default=False, verbose_name="Consentement marketing email")
    consent_timestamp = models.DateTimeField(null=True, blank=True, verbose_name="Timestamp de consentement")
    consent_ip = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP de consentement")

    # Contexte
    form_location = models.CharField(max_length=20, choices=FORM_LOCATION_CHOICES, default='main', verbose_name="Emplacement formulaire")
    lead_magnet = models.CharField(max_length=60, default='diagnostic_maths', verbose_name="Lead magnet")
    landing_path = models.CharField(max_length=255, blank=True, default="", verbose_name="Page d'atterrissage")
    referrer = models.URLField(max_length=500, blank=True, default="", verbose_name="Referrer")

    # Attribution
    utm_source = models.CharField(max_length=100, blank=True, default="", verbose_name="utm_source")
    utm_medium = models.CharField(max_length=100, blank=True, default="", verbose_name="utm_medium")
    utm_campaign = models.CharField(max_length=100, blank=True, default="", verbose_name="utm_campaign")
    utm_content = models.CharField(max_length=100, blank=True, default="", verbose_name="utm_content")
    utm_term = models.CharField(max_length=100, blank=True, default="", verbose_name="utm_term")
    gclid = models.CharField(max_length=255, blank=True, default="", verbose_name="gclid")
    fbclid = models.CharField(max_length=255, blank=True, default="", verbose_name="fbclid")
    ttclid = models.CharField(max_length=255, blank=True, default="", verbose_name="ttclid")
    msclkid = models.CharField(max_length=255, blank=True, default="", verbose_name="msclkid")

    # Lien optionnel vers l'abonné newsletter (si opt-in marketing coché)
    linked_subscriber = models.ForeignKey(
        NewsletterSubscriber,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='diagnostic_leads',
        verbose_name="Abonné newsletter associé"
    )

    # État de délivrance du diagnostic
    diagnostic_sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Diagnostic envoyé le")

    objects = BaseManager()

    class Meta:
        verbose_name = "Lead diagnostic"
        verbose_name_plural = "Leads diagnostic"
        ordering = ['-date_creation']
        indexes = [
            models.Index(fields=['email', '-date_creation']),
            models.Index(fields=['level', 'difficulty']),
            models.Index(fields=['utm_source', 'utm_campaign']),
        ]

    def __str__(self):
        return f"{self.email} ({self.get_level_display()})"

    def mark_diagnostic_sent(self, save=True):
        self.diagnostic_sent_at = timezone.now()
        if save:
            self.save(update_fields=['diagnostic_sent_at', 'date_modification'])


def testimonial_image_upload_to(instance, filename):
    """Range les captures par annee/mois, comme les images du blog."""
    return timezone.now().strftime('temoignages/%Y/%m/') + filename


class Testimonial(BaseModel):
    """Capture d'un avis recu par WhatsApp ou SMS, affichee sur la page « lien en bio ».

    On ne stocke que de vraies captures : la page ne reconstitue jamais de
    fausse conversation. Le champ `consent_confirmed` est un garde-fou RGPD,
    un message prive reste une donnee personnelle meme anonymisee.
    """

    CHANNEL_WHATSAPP = 'whatsapp'
    CHANNEL_SMS = 'sms'
    CHANNEL_CHOICES = [
        (CHANNEL_WHATSAPP, 'WhatsApp'),
        (CHANNEL_SMS, 'SMS'),
    ]

    # Aucun nom ni prenom n'est stocke : on ne decrit que le profil.
    # Un temoignage sans identite nominative reste parlant (« Maman d'eleve,
    # Terminale ») et ne peut pas trahir une famille par recoupement.
    # Doit rester aligne avec PROFILE_OPTIONS dans AdminTestimonials.vue :
    # DRF valide la valeur recue contre cette liste, accents compris.
    PROFILE_CHOICES = [
        ("Maman d'élève", "Maman d'élève"),
        ("Papa d'élève", "Papa d'élève"),
        ("Parent d'élève", "Parent d'élève"),
        ("Élève", "Élève"),
        ("Étudiant", "Étudiant"),
        ("Étudiante", "Étudiante"),
    ]

    author = models.CharField(
        max_length=80,
        blank=True,
        choices=PROFILE_CHOICES,
        verbose_name="Profil",
        help_text="Qui a ecrit le message. Jamais de nom ni de prenom.",
    )
    role = models.CharField(
        max_length=120,
        blank=True,
        verbose_name="Niveau",
        help_text="Ex. « Terminale », « Prepa MPSI ». Sans prenom d'enfant.",
    )

    # Affichage du prenom : refuse par defaut (protection par defaut, RGPD
    # art. 25). Il faut un accord explicite et distinct de celui qui autorise
    # la publication de la capture : accepter d'etre cite n'est pas la meme
    # chose qu'accepter d'etre nomme.
    name_consent = models.BooleanField(
        default=False,
        verbose_name="Accord pour le prenom",
        help_text="La personne autorise explicitement l'affichage de son prenom.",
    )
    display_name = models.CharField(
        max_length=60,
        blank=True,
        verbose_name="Prenom affiche",
        help_text="Prenom + initiale, ex. « Sandra M. ». Jamais le nom complet.",
    )
    channel = models.CharField(
        max_length=20,
        choices=CHANNEL_CHOICES,
        default=CHANNEL_WHATSAPP,
        verbose_name="Canal",
    )
    image = models.ImageField(
        upload_to=testimonial_image_upload_to,
        verbose_name="Capture",
        help_text="Numero, photo de profil et nom complet doivent etre masques avant l'envoi.",
    )
    alt_text = models.CharField(
        max_length=255,
        blank=True,
        verbose_name="Texte alternatif",
        help_text="Decrit la capture pour l'accessibilite et le referencement.",
    )
    # Champ conserve pour la tracabilite interne (admin Django) mais il ne
    # conditionne plus la publication : choix explicite du proprietaire du site.
    consent_confirmed = models.BooleanField(
        default=False,
        verbose_name="Accord obtenu",
        help_text="Trace interne. Ne bloque pas la publication.",
    )
    is_published = models.BooleanField(default=False, verbose_name="Publie")
    is_featured = models.BooleanField(
        default=False,
        verbose_name="Mis en avant",
        help_text="Affiche aussi dans le hero. Un seul temoignage a la fois.",
    )
    ordre = models.PositiveIntegerField(default=0, verbose_name="Ordre d'affichage")

    objects = BaseManager()

    class Meta:
        verbose_name = "Temoignage"
        verbose_name_plural = "Temoignages"
        ordering = ['ordre', '-date_creation']
        indexes = [
            models.Index(fields=['is_published', 'ordre']),
        ]

    @property
    def public_name(self):
        """Prenom affichable, ou chaine vide si l'accord manque."""
        return self.display_name if (self.name_consent and self.display_name) else ''

    @property
    def display_label(self):
        """Libelle affiche sur la carte, jamais vide."""
        parts = [part for part in (self.public_name or self.author, self.role) if part]
        return ' · '.join(parts) if parts else 'Temoignage'

    def __str__(self):
        return f"{self.display_label} ({self.get_channel_display()})"

    def save(self, *args, **kwargs):
        if not self.is_published:
            self.is_featured = False

        # Pas d'accord nominatif => on n'a aucune raison de conserver le
        # prenom. On l'efface plutot que de le garder « au cas ou » : une
        # donnee qu'on ne stocke pas ne peut pas fuiter.
        if not self.name_consent:
            self.display_name = ''

        super().save(*args, **kwargs)

        # Un seul temoignage en avant : on retire le drapeau des autres.
        if self.is_featured:
            Testimonial.objects.filter(is_featured=True).exclude(pk=self.pk).update(
                is_featured=False,
                date_modification=timezone.now(),
            )


class BioLandingSettings(BaseModel):
    """Reglages de la page « lien en bio » (/avis), pilotes depuis le studio.

    Enregistrement unique (pk=1) : il n'y a qu'une page a piloter, autant
    l'assumer plutot que de bricoler une table de cles/valeurs generique.
    """

    is_published = models.BooleanField(
        default=False,
        verbose_name="Page en ligne",
        help_text="Decoche : seuls les administrateurs voient la page.",
    )

    objects = BaseManager()

    class Meta:
        verbose_name = "Reglages page avis"
        verbose_name_plural = "Reglages page avis"

    def __str__(self):
        return 'Page /avis : en ligne' if self.is_published else 'Page /avis : hors ligne'

    def save(self, *args, **kwargs):
        # Singleton : on force l'identifiant pour qu'aucun second
        # enregistrement ne puisse apparaitre et creer une ambiguite.
        self.pk = 1

        # Forcer le pk sur une instance neuve declencherait un UPDATE avec
        # date_creation a NULL (auto_now_add ne s'applique qu'a l'insertion).
        # On reprend donc la date de la ligne existante.
        if self._state.adding:
            existing = type(self).objects.filter(pk=1).first()
            if existing is not None:
                self.date_creation = existing.date_creation
                self._state.adding = False

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # On ne supprime pas un singleton de configuration.
        pass

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj
