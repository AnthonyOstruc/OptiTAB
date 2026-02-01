"""
MODÈLES EXERCICES - ULTRA CLEAN et SIMPLE
Structure: Pays -> Niveau -> Matière -> Thème -> Notion -> Chapitre -> Exercice
"""
from django.db import models
from core.models import BaseSimple, BaseContent, BaseEducational, BaseOrganizational


class Matiere(BaseOrganizational):
    """Une matière scolaire (Maths, Français, etc.)"""
    show_on_home = models.BooleanField(default=True, verbose_name="Afficher sur la page d'accueil")
    
    class Meta:
        ordering = ['ordre', 'titre']
        verbose_name = "Matière"
        verbose_name_plural = "Matières"

    def __str__(self):
        return self.titre
    
    # Associations supprimées au profit de MatiereContexte


class MatiereContexte(BaseOrganizational):
    """Contexte pédagogique: une matière pour un niveau précis (pays implicite via niveau)

    Exemple: Mathématiques (France, 5ème)
    Toute la hiérarchie (thèmes, notions, chapitres, exercices, cours, quiz)
    se rattache à ce contexte pour éviter de propager pays/niveau partout.
    """
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='contextes')
    niveau = models.ForeignKey('pays.Niveau', on_delete=models.CASCADE, related_name='matieres_contexte')

    class Meta:
        unique_together = [['matiere', 'niveau']]
        ordering = ['matiere', 'niveau__pays', 'niveau__ordre']
        verbose_name = "Contexte Matière"
        verbose_name_plural = "Contextes Matière"

    def __str__(self):
        try:
            return f"{self.matiere.titre} ({self.niveau.pays.nom}, {self.niveau.nom})"
        except Exception:
            return f"{self.matiere.titre} (niveau {self.niveau_id})"

    @property
    def pays(self):
        return getattr(self.niveau, 'pays', None)


class Theme(BaseOrganizational):
    """Un thème dans une matière"""
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='themes')
    # Nouveau rattachement simple: un thème appartient à un contexte matière+niveau
    contexte = models.ForeignKey('curriculum.MatiereContexte', on_delete=models.CASCADE, related_name='themes', null=True, blank=True)
    # Ancien champ supprimé: niveaux M2M
    
    class Meta:
        unique_together = [['contexte', 'titre']]
        ordering = ['matiere', 'ordre', 'titre']
        verbose_name = "Thème"
        verbose_name_plural = "Thèmes"

    def __str__(self):
        return f"{self.matiere.titre} - {self.titre}"


class Notion(BaseOrganizational):
    """Une notion dans un thème"""
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE, related_name='notions')
    # Ancienne association niveaux supprimée; le contexte est porté par le thème
    
    class Meta:
        unique_together = [['theme', 'titre']]
        ordering = ['theme', 'ordre', 'titre']
        verbose_name = "Notion"
        verbose_name_plural = "Notions"

    def __str__(self):
        return f"{self.theme.titre} - {self.titre}"


class Exercice(BaseEducational):
    """Un exercice dans une notion"""
    notion = models.ForeignKey(Notion, on_delete=models.CASCADE, related_name='exercices', null=True)  # Temporaire pour migration
    question = models.TextField()
    reponse_correcte = models.TextField()
    etapes = models.TextField(blank=True, null=True, verbose_name="Étapes de résolution")
    ordre = None
    ACCESS_SCOPE_PAID = 'paid'
    ACCESS_SCOPE_FREE = 'free'
    ACCESS_SCOPE_BOTH = 'both'
    ACCESS_SCOPE_CHOICES = [
        (ACCESS_SCOPE_PAID, 'Abonnés uniquement'),
        (ACCESS_SCOPE_FREE, 'Gratuit (découverte)'),
        (ACCESS_SCOPE_BOTH, 'Gratuit + Abonnés'),
    ]
    access_scope = models.CharField(
        max_length=10,
        choices=ACCESS_SCOPE_CHOICES,
        default=ACCESS_SCOPE_PAID,
        help_text="Définit si ce contenu est gratuit, payant ou visible dans les deux parcours."
    )
    
    class Meta:
        unique_together = [['notion', 'titre']]
        ordering = ['notion', 'titre', 'id']
        verbose_name = "Exercice"
        verbose_name_plural = "Exercices"

    def __str__(self):
        return f"{self.notion.titre} - {self.titre}"


class ExerciceImage(models.Model):
    """Image associee a un exercice (enonce ou solution)"""
    exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='exercice_images/')
    position = models.PositiveIntegerField(null=True, blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['exercice', 'position', 'id']
        verbose_name = "Image d'exercice"
        verbose_name_plural = "Images d'exercice"
        indexes = [
            models.Index(fields=['exercice', 'position']),
        ]

    def __str__(self):
        return f"Image {self.id} - Exercice {self.exercice_id}"

