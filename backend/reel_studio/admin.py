from django.contrib import admin

from .models import ReelProject, ReelSlide


class ReelSlideInline(admin.TabularInline):
    model = ReelSlide
    extra = 0


@admin.register(ReelProject)
class ReelProjectAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'level', 'format_type', 'slide_count', 'status', 'updated_at')
    list_filter = ('status', 'level', 'format_type')
    search_fields = ('title', 'theme', 'level', 'format_type')
    inlines = [ReelSlideInline]


@admin.register(ReelSlide)
class ReelSlideAdmin(admin.ModelAdmin):
    list_display = ('id', 'reel_project', 'order', 'slide_type', 'layout_status', 'duration_seconds', 'updated_at')
    list_filter = ('slide_type', 'layout_status')
    search_fields = ('title', 'screen_text', 'voice_script', 'katex')
