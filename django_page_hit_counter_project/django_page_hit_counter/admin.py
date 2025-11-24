from django.contrib import admin
from .models import Hit
@admin.register(Hit)
class HitAdmin(admin.ModelAdmin):
    list_display = ("path", "content_type", "object_id", "hits", "last_hit")
    search_fields = ("path",)
    readonly_fields = ("last_hit",)
