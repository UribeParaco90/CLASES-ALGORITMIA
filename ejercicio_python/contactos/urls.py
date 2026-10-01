from django.urls import path
from . import views

app_name = "contactos"

urlpatterns = [
    path("", views.crear, name="crear"),
    path("lista/", views.listar, name="lista"),
    path("detalle/<int:id>/", views.detalle, name="detalle"),
    path("editar/<int:id>/", views.editar, name="editar"),
    path("eliminar/<int:id>/", views.eliminar, name="eliminar"),
]