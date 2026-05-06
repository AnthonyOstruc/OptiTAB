from django.contrib import admin
from .models import MathRunScore


@admin.register(MathRunScore)
class MathRunScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'category', 'score', 'created_at')
    list_filter = ('category',)
    ordering = ('-score',)
