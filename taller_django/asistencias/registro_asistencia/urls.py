from django.urls import path

from . import views

urlpatterns = [
    path("", views.lista_registros, name="registro_asistencia_lista"),
    path("nuevo/", views.crear_registro, name="registro_asistencia_create"),
    path("<int:pk>/", views.detalle_registro, name="registro_asistencia_detail"),
    path("<int:pk>/editar/", views.actualizar_registro, name="registro_asistencia_update"),
    path("<int:pk>/eliminar/", views.eliminar_registro, name="registro_asistencia_delete"),
]
