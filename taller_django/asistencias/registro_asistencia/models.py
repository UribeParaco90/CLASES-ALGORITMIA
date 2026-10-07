from django.db import models


class RegistroAsistencia(models.Model):
    """Registro de la asistencia de una persona."""

    tipo_documento = models.CharField(max_length=30)
    documento = models.CharField(max_length=30)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    whatsapp = models.CharField(max_length=20)
    fecha = models.DateField()
    asistio = models.BooleanField(default=False)

    class Meta:
        ordering = ["-fecha", "apellidos", "nombres"]
        constraints = [
            models.UniqueConstraint(
                fields=["tipo_documento", "documento"],
                name="unique_registro_asistencia_documento",
            )
        ]

    def __str__(self):
        return f"{self.nombres} {self.apellidos} - {self.fecha}"