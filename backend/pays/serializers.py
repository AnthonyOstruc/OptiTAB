"""
SÉRIALISEURS ULTRA SIMPLES - Version CLEAN
"""
from rest_framework import serializers
from .models import Pays, Niveau


class PaysSerializer(serializers.ModelSerializer):
    """Sérialiseur simple pour les pays"""
    nombre_niveaux = serializers.IntegerField(read_only=True)
    nombre_utilisateurs = serializers.IntegerField(read_only=True)

    class Meta:
        model = Pays
        fields = ['id', 'nom', 'code_iso', 'drapeau_emoji', 'est_actif', 'ordre', 'nombre_niveaux', 'nombre_utilisateurs']


class NiveauSerializer(serializers.ModelSerializer):
    """Sérialiseur simple pour les niveaux"""
    pays_nom = serializers.CharField(source='pays.nom', read_only=True)
    pays_drapeau = serializers.CharField(source='pays.drapeau_emoji', read_only=True)
    statistiques = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = Niveau
        fields = ['id', 'nom', 'pays', 'ordre', 'couleur', 'est_actif', 'pays_nom', 'pays_drapeau', 'statistiques']

    def get_statistiques(self, obj):
        # Importer localement pour éviter les imports circulaires
        try:
            from curriculum.models import MatiereContexte, Theme, Notion, Chapitre, Exercice
            from cours.models import Cours
            from quiz.models import Quiz
        except Exception:
            return {}

        # Comptages basés sur le contexte
        matiere_ids = (
            MatiereContexte.objects.filter(niveau=obj, est_actif=True)
            .values_list('matiere_id', flat=True)
            .distinct()
        )
        themes_count = Theme.objects.filter(contexte__niveau=obj, est_actif=True).count()
        notions_count = Notion.objects.filter(theme__contexte__niveau=obj, est_actif=True).count()
        chapitres_count = Chapitre.objects.filter(notion__theme__contexte__niveau=obj, est_actif=True).count()
        exercices_count = Exercice.objects.filter(chapitre__notion__theme__contexte__niveau=obj, est_actif=True).count()
        cours_count = Cours.objects.filter(chapitre__notion__theme__contexte__niveau=obj).count()
        quiz_count = Quiz.objects.filter(chapitre__notion__theme__contexte__niveau=obj).count()

        return {
            'matieres': len(matiere_ids),
            'themes': themes_count,
            'notions': notions_count,
            'chapitres': chapitres_count,
            'exercices': exercices_count,
            'cours': cours_count,
            'quiz': quiz_count,
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        include_stats = self.context.get('include_stats', False)
        if not include_stats:
            data.pop('statistiques', None)
        return data