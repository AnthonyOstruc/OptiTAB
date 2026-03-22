import re

from django import forms
from django.contrib import admin, messages
from django.contrib.admin.utils import unquote
from django.core.exceptions import PermissionDenied
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path, reverse
from django.utils.html import format_html

from .models import Cours, CoursImage
from .services import CoursePdfGenerationError, build_course_pdf_filename, render_course_pdf_bytes
from .utils import resolve_course_image_alt, resolve_course_image_title, resolve_course_title


class CoursAdminForm(forms.ModelForm):
    import_html_file = forms.FileField(
        required=False,
        label="Importer un fichier HTML/TXT",
        help_text=(
            "Importe directement le fichier dans le champ contenu. "
            "Formats acceptes: .html, .htm, .txt, .md"
        ),
    )

    class Meta:
        model = Cours
        fields = "__all__"

    def clean_import_html_file(self):
        upload = self.cleaned_data.get("import_html_file")
        if not upload:
            return upload

        filename = str(getattr(upload, "name", "") or "").lower()
        allowed = (".html", ".htm", ".txt", ".md")
        if not filename.endswith(allowed):
            raise forms.ValidationError("Extension invalide. Utilisez .html, .htm, .txt ou .md.")

        size = int(getattr(upload, "size", 0) or 0)
        if size > 5 * 1024 * 1024:
            raise forms.ValidationError("Le fichier depasse 5 Mo.")

        return upload


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
    form = CoursAdminForm
    change_form_template = "admin/cours/cours/change_form.html"
    list_display = [
        "titre",
        "notion",
        "access_scope",
        "est_actif",
        "pdf_preview_action",
        "pdf_download_action",
        "pdf_link",
    ]
    list_filter = ["access_scope", "est_actif"]
    search_fields = ["titre", "notion__titre"]
    ordering = ["notion"]
    list_editable = ["est_actif", "access_scope"]
    fieldsets = (
        (
            "Informations du cours",
            {
                "fields": (
                    "notion",
                    "titre",
                    "difficulty",
                    "access_scope",
                    "est_actif",
                )
            },
        ),
        (
            "Contenu source",
            {
                "description": (
                    "Collez le HTML du cours dans 'contenu' ou importez un fichier HTML/TXT. "
                    "Le rendu PDF normalise les styles inline vers des classes print reutilisables."
                ),
                "fields": (
                    "import_html_file",
                    "contenu",
                    "video_url",
                ),
            },
        ),
        (
            "PDF natif",
            {
                "description": (
                    "Workflow: Previsualiser puis telecharger. "
                    "Le PDF est genere en texte natif (selectionnable/recherchable)."
                ),
                "fields": (
                    "pdf_actions",
                    "pdf_file",
                ),
            },
        ),
        (
            "Metadonnees",
            {
                "fields": (
                    "date_creation",
                    "date_modification",
                ),
                "classes": ("collapse",),
            },
        ),
    )
    readonly_fields = ("date_creation", "date_modification", "pdf_actions")
    inlines = [CoursImageInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if "contenu" in form.base_fields:
            from django.forms import Textarea

            form.base_fields["contenu"].widget = Textarea(
                attrs={
                    "rows": 32,
                    "cols": 80,
                    "style": "white-space: pre-wrap; font-family: monospace; line-height: 1.45;",
                    "placeholder": "<h2>Titre section</h2>\\n<p>Votre contenu HTML...</p>",
                }
            )
            form.base_fields["contenu"].help_text = (
                "HTML source du cours. Les styles inline sont normalises automatiquement "
                "pour le rendu PDF."
            )
        return form

    def get_urls(self):
        base_urls = super().get_urls()
        custom_urls = [
            path(
                "<path:object_id>/pdf-preview/",
                self.admin_site.admin_view(self.pdf_preview_view),
                name="cours_cours_pdf_preview",
            ),
            path(
                "<path:object_id>/pdf-download/",
                self.admin_site.admin_view(self.pdf_download_view),
                name="cours_cours_pdf_download",
            ),
        ]
        return custom_urls + base_urls

    def changeform_view(self, request, object_id=None, form_url="", extra_context=None):
        extra_context = extra_context or {}
        if object_id:
            safe_object_id = unquote(object_id)
            extra_context["pdf_preview_url"] = reverse(
                "admin:cours_cours_pdf_preview",
                args=[safe_object_id],
            )
            extra_context["pdf_download_url"] = reverse(
                "admin:cours_cours_pdf_download",
                args=[safe_object_id],
            )
        return super().changeform_view(request, object_id, form_url, extra_context)

    def _decode_uploaded_html(self, uploaded_file):
        if not uploaded_file:
            return ""
        raw_bytes = uploaded_file.read()
        if not raw_bytes:
            return ""

        for encoding in ("utf-8-sig", "utf-8", "latin-1"):
            try:
                return raw_bytes.decode(encoding)
            except UnicodeDecodeError:
                continue

        return raw_bytes.decode("utf-8", errors="ignore")

    def save_model(self, request, obj, form, change):
        import_file = form.cleaned_data.get("import_html_file")
        if import_file:
            imported_content = self._decode_uploaded_html(import_file)
            if imported_content:
                obj.contenu = imported_content
                self.message_user(
                    request,
                    f"Fichier '{import_file.name}' importe dans le contenu du cours.",
                    level=messages.SUCCESS,
                )

        has_html_markup = bool(re.search(r"<[a-zA-Z!/][^>]*>", obj.contenu or ""))

        if obj.contenu and not has_html_markup:
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

    def _get_course_or_raise(self, request, object_id):
        obj = self.get_object(request, unquote(object_id))
        if obj is None:
            raise PermissionDenied("Cours introuvable.")
        if not self.has_view_or_change_permission(request, obj):
            raise PermissionDenied
        return obj

    def pdf_preview_view(self, request, object_id):
        cours = self._get_course_or_raise(request, object_id)
        context = {
            **self.admin_site.each_context(request),
            "opts": self.model._meta,
            "original": cours,
            "title": f"Apercu PDF - {cours}",
            "inline_pdf_url": (
                reverse("admin:cours_cours_pdf_download", args=[cours.pk])
                + "?disposition=inline&persist=0"
            ),
            "download_pdf_url": reverse("admin:cours_cours_pdf_download", args=[cours.pk]),
            "refresh_preview_url": reverse("admin:cours_cours_pdf_preview", args=[cours.pk]),
            "change_url": reverse("admin:cours_cours_change", args=[cours.pk]),
        }
        return TemplateResponse(request, "admin/cours/cours/pdf_preview.html", context)

    def pdf_download_view(self, request, object_id):
        cours = self._get_course_or_raise(request, object_id)

        disposition_param = str(request.GET.get("disposition", "") or "").lower()
        disposition = "inline" if disposition_param == "inline" else "attachment"
        persist = str(request.GET.get("persist", "1")) == "1"

        try:
            pdf_bytes = render_course_pdf_bytes(cours, request=request)
        except CoursePdfGenerationError as exc:
            error_message = f"Erreur generation PDF: {exc}"
            if disposition == "inline":
                return HttpResponse(error_message, content_type="text/plain; charset=utf-8", status=500)

            self.message_user(request, error_message, level=messages.ERROR)
            return HttpResponseRedirect(reverse("admin:cours_cours_change", args=[cours.pk]))

        filename = build_course_pdf_filename(cours)

        if persist and disposition == "attachment":
            try:
                cours.pdf_file.save(filename, ContentFile(pdf_bytes), save=True)
            except Exception as exc:  # pragma: no cover - storage backends may vary
                self.message_user(
                    request,
                    f"PDF genere, mais sauvegarde dans pdf_file impossible: {exc}",
                    level=messages.WARNING,
                )

        response = HttpResponse(pdf_bytes, content_type="application/pdf")
        response["Content-Disposition"] = f'{disposition}; filename="{filename}"'
        response["Cache-Control"] = "no-store"
        if disposition == "inline":
            response["X-Frame-Options"] = "SAMEORIGIN"
        return response

    def pdf_actions(self, obj):
        if not getattr(obj, "pk", None):
            return "Enregistrez d'abord le cours pour activer les actions PDF."

        preview_url = reverse("admin:cours_cours_pdf_preview", args=[obj.pk])
        download_url = reverse("admin:cours_cours_pdf_download", args=[obj.pk])
        return format_html(
            '<a class="button" href="{}" target="_blank">Previsualiser le PDF</a>&nbsp;'
            '<a class="button" href="{}" target="_blank">Telecharger le PDF</a>',
            preview_url,
            download_url,
        )

    pdf_actions.short_description = "Actions PDF"

    def pdf_preview_action(self, obj):
        if not getattr(obj, "pk", None):
            return "-"
        url = reverse("admin:cours_cours_pdf_preview", args=[obj.pk])
        return format_html('<a href="{}" target="_blank">Previsualiser</a>', url)

    pdf_preview_action.short_description = "Preview PDF"

    def pdf_download_action(self, obj):
        if not getattr(obj, "pk", None):
            return "-"
        url = reverse("admin:cours_cours_pdf_download", args=[obj.pk])
        return format_html('<a href="{}" target="_blank">Telecharger</a>', url)

    pdf_download_action.short_description = "Download PDF"

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
