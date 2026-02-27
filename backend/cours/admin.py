from django.contrib import admin
from django.utils.html import format_html

from .models import Cours, CoursImage
from .utils import resolve_course_image_alt, resolve_course_image_title, resolve_course_title


class CoursImageInline(admin.TabularInline):
    model = CoursImage
    extra = 0
    fields = (
        "preview",
        "image",
        "image_type",
        "position",
        "alt_text",
        "title_text",
        "legende",
        "width",
        "height",
    )
    readonly_fields = ("preview", "width", "height")
    can_delete = True

    def preview(self, obj):
        if getattr(obj, "image", None):
            try:
                return format_html(
                    '<img src="{}" style="height: 80px; max-width: 140px; object-fit: cover;" />',
                    obj.image.url,
                )
            except Exception:
                return "(apercu indisponible)"
        return "-"

    preview.short_description = "Apercu"


@admin.register(Cours)
class CoursAdmin(admin.ModelAdmin):
    list_display = ["titre", "notion", "access_scope", "est_actif", "pdf_link"]
    list_filter = ["access_scope", "est_actif"]
    search_fields = ["titre", "notion__titre"]
    ordering = ["notion"]
    list_editable = ["est_actif", "access_scope"]
    fields = (
        "notion",
        "titre",
        "contenu",
        "access_scope",
        "video_url",
        "pdf_file",
        "est_actif",
        "date_creation",
        "date_modification",
    )
    readonly_fields = ("date_creation", "date_modification")
    inlines = [CoursImageInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "contenu" in form.base_fields:
            from django.forms import Textarea

            form.base_fields["contenu"].widget = Textarea(
                attrs={
                    "rows": 15,
                    "cols": 80,
                    "style": "white-space: pre-wrap; font-family: monospace;",
                }
            )
        return form

    def save_model(self, request, obj, form, change):
        if obj.contenu:
            lines = obj.contenu.split("\n")
            cleaned_lines = []
            prev_empty = False

            for line in lines:
                stripped_line = line.rstrip()
                if stripped_line:
                    cleaned_lines.append(stripped_line)
                    prev_empty = False
                elif not prev_empty:
                    cleaned_lines.append("")
                    prev_empty = True

            obj.contenu = "\n".join(cleaned_lines)

        super().save_model(request, obj, form, change)

    def pdf_link(self, obj):
        pdf = getattr(obj, "pdf_file", None)
        if pdf:
            try:
                return format_html('<a href="{}" target="_blank">Telecharger</a>', pdf.url)
            except Exception:
                return "(lien indisponible)"
        return "-"

    pdf_link.short_description = "PDF"


@admin.register(CoursImage)
class CoursImageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "cours",
        "image_type",
        "position",
        "alt_text",
        "title_text",
        "legende",
        "image_link",
    )
    list_filter = ("image_type",)
    search_fields = ("cours__notion__titre", "legende", "alt_text", "title_text", "image")
    ordering = ("cours", "position", "id")
    list_editable = ("position", "alt_text", "title_text", "legende")
    actions = ("auto_fill_alt_from_filename_legend",)

    def image_link(self, obj):
        if getattr(obj, "image", None):
            try:
                return format_html('<a href="{}" target="_blank">Voir</a>', obj.image.url)
            except Exception:
                return "(lien indisponible)"
        return "-"

    image_link.short_description = "Image"

    @admin.action(description="Auto-fill alt from filename/legend")
    def auto_fill_alt_from_filename_legend(self, request, queryset):
        updated_count = 0

        for image_obj in queryset.select_related("cours", "cours__notion"):
            updates = []
            course_title = resolve_course_title(getattr(image_obj, "cours", None))

            if not str(image_obj.alt_text or "").strip():
                image_obj.alt_text = resolve_course_image_alt(image_obj, course_title=course_title)
                updates.append("alt_text")

            if not str(image_obj.title_text or "").strip():
                title_value = resolve_course_image_title(image_obj)
                if title_value:
                    image_obj.title_text = title_value
                    updates.append("title_text")

            if (not image_obj.width or not image_obj.height) and getattr(image_obj, "image", None):
                try:
                    if not image_obj.width:
                        image_obj.width = int(getattr(image_obj.image, "width", 0) or 0) or None
                        updates.append("width")
                    if not image_obj.height:
                        image_obj.height = int(getattr(image_obj.image, "height", 0) or 0) or None
                        updates.append("height")
                except Exception:
                    pass

            if updates:
                image_obj.save(update_fields=updates + ["date_modification"])
                updated_count += 1

        self.message_user(request, f"{updated_count} image(s) mises a jour.")
