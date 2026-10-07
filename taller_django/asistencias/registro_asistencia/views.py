from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import RegistroAsistenciaForm
from .models import RegistroAsistencia


def lista_registros(request):
    registros = RegistroAsistencia.objects.all()
    return render(request, "lista.html", {"registros": registros})


def crear_registro(request):
    if request.method == "POST":
        form = RegistroAsistenciaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("registro_asistencia_lista")
    else:
        form = RegistroAsistenciaForm()

    return render(request, "formulario.html", {"form": form, "titulo": "Nuevo registro"})


def detalle_registro(request, pk):
    registro = get_object_or_404(RegistroAsistencia, pk=pk)
    return render(request, "detalles.html", {"registro": registro})


def actualizar_registro(request, pk):
    registro = get_object_or_404(RegistroAsistencia, pk=pk)
    if request.method == "POST":
        form = RegistroAsistenciaForm(request.POST, instance=registro)
        if form.is_valid():
            form.save()
            return redirect("registro_asistencia_lista")
    else:
        form = RegistroAsistenciaForm(instance=registro)

    return render(request, "formulario.html", {"form": form, "titulo": "Editar registro"})


@require_POST
def eliminar_registro(request, pk):
    registro = get_object_or_404(RegistroAsistencia, pk=pk)
    registro.delete()
    return redirect("registro_asistencia_lista")
