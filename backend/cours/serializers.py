"""
Serializers for courses and course images.
"""
from rest_framework import serializers

from .models import Cours, CoursImage
from .utils import build_course_image_payload, resolve_course_title


class CoursSerializer(serializers.ModelSerializer):
    images = serializers.SerializerMethodField(read_only=True)
    pdf_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cours
        fields = "__all__"

    def get_images(self, obj):
        qs = getattr(obj, "images", None)
        if qs is None:
            return []

        request = self.context.get("request") if hasattr(self, "context") else None
        course_title = resolve_course_title(obj)
        return [
            build_course_image_payload(img, request=request, course_title=course_title)
            for img in qs.all().order_by("position", "id")
        ]

    def get_pdf_url(self, obj):
        try:
            pdf = getattr(obj, "pdf_file", None)
            if not pdf:
                return ""
            url = getattr(pdf, "url", "")
            request = self.context.get("request") if hasattr(self, "context") else None
            if url and not str(url).startswith(("http://", "https://")) and request:
                return request.build_absolute_uri(url)
            return url
        except Exception:
            return ""


class CoursImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoursImage
        fields = "__all__"
        extra_kwargs = {
            "legende": {"required": False, "allow_blank": True},
            "position": {"required": False},
            "alt_text": {"required": False, "allow_blank": True},
            "title_text": {"required": False, "allow_blank": True},
            "width": {"required": False},
            "height": {"required": False},
        }

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get("request") if hasattr(self, "context") else None
        course_title = resolve_course_title(getattr(instance, "cours", None))
        payload = build_course_image_payload(instance, request=request, course_title=course_title)

        data["image"] = payload["image"]
        data["legende"] = payload["legende"]
        data["caption"] = payload["caption"]
        data["alt_text_resolved"] = payload["alt_text_resolved"]
        data["title_text_resolved"] = payload["title_text_resolved"]
        data["width"] = payload["width"]
        data["height"] = payload["height"]
        return data
