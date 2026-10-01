from django.shortcuts import render
from .models import Contacto


# CREAR
def crear(request):

    if request.method == "POST":

        contacto = Contacto(
            nombre=request.POST["nombre"],
            correo=request.POST["correo"],
            telefono=request.POST["telefono"],
            mensaje=request.POST["mensaje"]
        )

        contacto.save()

    return render(request, "contactos/formulario.html")


# LISTAR
def listar(request):

    contactos = Contacto.objects.all()

    return render(
        request,
        "contactos/lista.html",
        {"contactos": contactos}
    )


# VER
def detalle(request, id):

    contacto = Contacto.objects.get(id=id)

    return render(
        request,
        "contactos/detalle.html",
        {"contacto": contacto}
    )


# EDITAR
def editar(request, id):

    contacto = Contacto.objects.get(id=id)

    if request.method == "POST":

        contacto.nombre = request.POST["nombre"]
        contacto.correo = request.POST["correo"]
        contacto.telefono = request.POST["telefono"]
        contacto.mensaje = request.POST["mensaje"]

        contacto.save()

        return render(
            request,
            "contactos/detalle.html",
            {"contacto": contacto}
        )

    return render(
        request,
        "contactos/formulario.html",
        {"contacto": contacto}
    )


# ELIMINAR
def eliminar(request, id):

    contacto = Contacto.objects.get(id=id)

    contacto.delete()

    return render(
        request,
        "contactos/lista.html",
        {"contactos": Contacto.objects.all()}
    )