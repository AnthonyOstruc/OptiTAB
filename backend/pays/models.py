"""
MODÈLES ULTRA SIMPLES - Version finale CLEAN
Un seul fichier, code minimal, facile à comprendre
"""
from django.db import models
from core.models import BaseSimple  # Simple model without description


class Pays(BaseSimple):
    """Un pays avec son système éducatif"""
    code_iso = models.CharField(max_length=3, unique=True)
    drapeau_emoji = models.CharField(max_length=10, blank=True, null=True)
    # Inherits: nom, ordre, est_actif, timestamps

    class Meta:
        ordering = ['ordre', 'nom']
        verbose_name = "Pays"
        verbose_name_plural = "Pays"

    def __str__(self):
        return f"{self.drapeau_emoji} {self.nom}" if self.drapeau_emoji else self.nom


class Niveau(BaseSimple):
    """Un niveau scolaire dans un pays (ex: 6ème France, Grade 6 Canada)"""
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, related_name='niveaux')
    couleur = models.CharField(max_length=7, default='#3b82f6')
    # Options de filtre d'exercices spécifiques à ce niveau (ex: "Type bac", "Problème")
    exercice_filter_options = models.JSONField(default=list, blank=True)
    exercice_filter_default = models.CharField(max_length=120, default='Tous', blank=True)
    # Chapitre démo : notion + exercices débloqués pour les non-abonnés
    demo_notion = models.ForeignKey(
        'curriculum.Notion', on_delete=models.SET_NULL,
        null=True, blank=True, related_name='+',
        verbose_name="Chapitre démo",
        help_text="Notion (chapitre) débloquée gratuitement pour ce niveau"
    )
    demo_exercices = models.ManyToManyField(
        'curriculum.Exercice', blank=True, related_name='+',
        verbose_name="Exercices démo",
        help_text="Exercices débloqués gratuitement (du chapitre démo)"
    )
    # Inherits: nom, ordre, est_actif, timestamps

    class Meta:
        unique_together = [['pays', 'nom']]
        ordering = ['pays', 'ordre', 'nom']
        verbose_name_plural = "Niveaux par pays"

    def __str__(self):
        return f"{self.pays.nom} - {self.nom}"
