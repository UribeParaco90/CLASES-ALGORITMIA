from unittest.mock import Mock, patch

from bson import ObjectId
from django.test import TestCase


class ProductoViewsTests(TestCase):
    @patch("productos.views.coleccion_productos")
    def test_lista_productos(self, coleccion):
        coleccion.find.return_value.sort.return_value = [
            {
                "_id": ObjectId(),
                "nombre": "Teclado",
                "categoria": "Periféricos",
                "precio": 85000.0,
                "cantidad": 10,
            }
        ]

        respuesta = self.client.get("/")

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "Teclado")
        self.assertContains(respuesta, "Periféricos")

    @patch("productos.views.coleccion_productos")
    def test_crear_producto(self, coleccion):
        respuesta = self.client.post(
            "/crear/",
            {
                "nombre": "Teclado",
                "categoria": "Periféricos",
                "precio": "85000",
                "cantidad": "10",
            },
        )

        self.assertRedirects(respuesta, "/")
        coleccion.insert_one.assert_called_once_with(
            {
                "nombre": "Teclado",
                "categoria": "Periféricos",
                "precio": 85000.0,
                "cantidad": 10,
            }
        )

    @patch("productos.views.coleccion_productos")
    def test_rechaza_precio_negativo_y_cantidad_decimal(self, coleccion):
        respuesta = self.client.post(
            "/crear/",
            {
                "nombre": "Teclado",
                "categoria": "Periféricos",
                "precio": "-1",
                "cantidad": "1.5",
            },
        )

        self.assertEqual(respuesta.status_code, 200)
        self.assertContains(respuesta, "no negativo")
        self.assertContains(respuesta, "número entero")
        coleccion.insert_one.assert_not_called()

    @patch("productos.views.coleccion_productos")
    def test_editar_producto_incluye_categoria(self, coleccion):
        identificador = ObjectId()
        coleccion.find_one.return_value = {
            "_id": identificador,
            "nombre": "Teclado",
            "categoria": "Periféricos",
            "precio": 85000.0,
            "cantidad": 10,
        }

        respuesta = self.client.post(
            f"/editar/{identificador}/",
            {
                "nombre": "Teclado",
                "categoria": "Accesorios",
                "precio": "85000",
                "cantidad": "15",
            },
        )

        self.assertRedirects(respuesta, "/")
        coleccion.update_one.assert_called_once_with(
            {"_id": identificador},
            {
                "$set": {
                    "nombre": "Teclado",
                    "categoria": "Accesorios",
                    "precio": 85000.0,
                    "cantidad": 15,
                }
            },
        )

    @patch("productos.views.coleccion_productos")
    def test_eliminar_producto(self, coleccion):
        coleccion.delete_one.return_value = Mock(deleted_count=1)
        identificador = ObjectId()

        respuesta = self.client.post(f"/eliminar/{identificador}/")

        self.assertRedirects(respuesta, "/")
        coleccion.delete_one.assert_called_once_with(
            {"_id": identificador}
        )

    @patch("productos.views.coleccion_productos")
    def test_get_no_elimina_producto(self, coleccion):
        identificador = ObjectId()

        respuesta = self.client.get(f"/eliminar/{identificador}/")

        self.assertRedirects(respuesta, "/")
        coleccion.delete_one.assert_not_called()
