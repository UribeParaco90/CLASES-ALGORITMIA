from django.test import TestCase
from django.urls import reverse

from registro_asistencia.models import RegistroAsistencia


class RegistroAsistenciaCrudTests(TestCase):
    def test_create_update_and_delete_registration(self):
        create_url = reverse("registro_asistencia_create")
        detail_url = reverse("registro_asistencia_detail", args=[1])
        update_url = reverse("registro_asistencia_update", args=[1])
        delete_url = reverse("registro_asistencia_delete", args=[1])

        response = self.client.post(
            create_url,
            {
                "tipo_documento": "CC",
                "documento": "123456789",
                "nombres": "Ana",
                "apellidos": "García López",
                "whatsapp": "3001234567",
                "fecha": "2026-10-07",
                "asistio": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        registro = RegistroAsistencia.objects.get()
        self.assertTrue(registro.asistio)
        self.assertEqual(registro.documento, "123456789")

        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ana García López")

        response = self.client.post(
            update_url,
            {
                "tipo_documento": "CC",
                "documento": "123456789",
                "nombres": "Ana",
                "apellidos": "García Ramírez",
                "whatsapp": "3009876543",
                "fecha": "2026-10-07",
                "asistio": "",
            },
        )
        self.assertEqual(response.status_code, 302)
        registro.refresh_from_db()
        self.assertEqual(registro.apellidos, "García Ramírez")
        self.assertFalse(registro.asistio)

        response = self.client.post(delete_url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(RegistroAsistencia.objects.exists())

    def test_duplicate_document_is_rejected(self):
        RegistroAsistencia.objects.create(
            tipo_documento="CC",
            documento="123456789",
            nombres="Ana",
            apellidos="García López",
            whatsapp="3001234567",
            fecha="2026-10-07",
            asistio=True,
        )

        form = self.client.post(
            reverse("registro_asistencia_create"),
            {
                "tipo_documento": "CC",
                "documento": "123456789",
                "nombres": "Otro",
                "apellidos": "Usuario",
                "whatsapp": "3000000000",
                "fecha": "2026-10-08",
                "asistio": "on",
            },
        )

        self.assertEqual(form.status_code, 200)
        self.assertTrue(
            any(
                "Ya existe un registro" in message
                for message in form.context["form"].errors["__all__"]
            )
        )
        self.assertEqual(RegistroAsistencia.objects.count(), 1)
