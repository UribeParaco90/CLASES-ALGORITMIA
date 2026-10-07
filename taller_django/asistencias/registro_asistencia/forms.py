from django import forms
from django.core.exceptions import ValidationError

from .models import RegistroAsistencia


class RegistroAsistenciaForm(forms.ModelForm):
    class Meta:
        model = RegistroAsistencia
        fields = [
            "tipo_documento",
            "documento",
            "nombres",
            "apellidos",
            "whatsapp",
            "fecha",
            "asistio",
        ]
        widgets = {
            "fecha": forms.DateInput(attrs={"type": "date"}),
            "asistio": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo_documento = cleaned_data.get("tipo_documento")
        documento = cleaned_data.get("documento")

        if tipo_documento and documento:
            self.instance.pk = self.instance.pk
            duplicate = RegistroAsistencia.objects.filter(
                tipo_documento=tipo_documento,
                documento=documento,
            ).exclude(pk=self.instance.pk)
            if duplicate.exists():
                raise ValidationError(
                    "Ya existe un registro con este tipo de documento y número."
                )

        return cleaned_data
