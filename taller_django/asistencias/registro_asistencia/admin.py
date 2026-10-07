from django.contrib import admin

from .models import RegistroAsistencia


@admin.register(RegistroAsistencia)
class RegistroAsistenciaAdmin(admin.ModelAdmin):
    list_display = ("nombres", "apellidos", "tipo_documento", "documento", "fecha", "asistio")
    list_filter = ("fecha", "asistio")
    search_fields = ("nombres", "apellidos", "documento")
    ordering = ("-fecha",)
