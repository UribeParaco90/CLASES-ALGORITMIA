# Guía práctica: CRUD de productos con Django y MongoDB

**Objetivo:** construir una aplicación web sencilla que permita registrar, consultar, editar y eliminar productos utilizando Django, Python y MongoDB Atlas.

Esta práctica continúa el trabajo realizado con Django y PostgreSQL. Los aprendices ya conocen las vistas, las URL, los formularios HTML y las operaciones CRUD. Ahora aprenderán a trabajar con una base de datos documental utilizando MongoDB.

## ¿Qué vamos a construir?

Una aplicación web de inventario con tres datos por producto:

- Nombre.
- Precio.
- Cantidad disponible.

Las operaciones serán:

- **Crear:** registrar productos nuevos.
- **Consultar:** mostrar los productos registrados.
- **Editar:** modificar los datos de un producto.
- **Eliminar:** borrar un producto.

## 1. Comprender las tecnologías

| Tecnología | Función |
|---|---|
| Python | Lenguaje de programación. |
| Django | Gestiona las URL, las vistas y las plantillas HTML. |
| PyMongo | Permite que Python se comunique con MongoDB. |
| MongoDB Atlas | Aloja la base de datos en la nube. |
| HTML | Presenta los formularios y el inventario en el navegador. |

El funcionamiento será:

**Navegador → Django (URL, vista y validación) → PyMongo → MongoDB Atlas**

**Diferencia con PostgreSQL:** en la práctica anterior se trabajó con tablas y modelos del ORM de Django. En esta práctica se utilizarán documentos y colecciones de MongoDB mediante PyMongo. Por eso no necesitamos crear un modelo Django para los productos ni ejecutar migraciones para ellos.

## 2. Preparar el entorno de trabajo

Necesitamos:

- Python instalado.
- Visual Studio Code.
- Un navegador web.
- Una cuenta de MongoDB Atlas.

No necesitamos Docker, una API REST ni Django REST Framework.

### 2.1. Crear la carpeta del proyecto

Abre Visual Studio Code, selecciona **Terminal → Nueva terminal** y ejecuta estos comandos en Windows:

```powershell
mkdir django_mongo
cd django_mongo
```

### 2.2. Crear y activar el entorno virtual

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Si utilizas CMD en lugar de PowerShell, activa el entorno con:

```bat
venv\Scripts\activate.bat
```

Un entorno virtual permite instalar las dependencias de este proyecto sin mezclarlas con las de otros proyectos de Python. Cuando esté activo, normalmente aparecerá `(venv)` al comienzo de la línea de la terminal.

Si Windows bloquea la activación en PowerShell, puedes seleccionar CMD como terminal de VS Code y utilizar el segundo comando.

### 2.3. Instalar las dependencias

```powershell
python -m pip install django pymongo dnspython python-dotenv
py -m pip install django pymongo dnspython python-dotenv
```

- `django`: permite desarrollar la aplicación web.
- `pymongo`: conecta Python con MongoDB.
- `dnspython`: permite resolver los registros DNS utilizados por conexiones `mongodb+srv://`.
- `python-dotenv`: permite leer variables de configuración desde el archivo `.env`.

Comprueba que Django esté instalado:

```powershell
python -m django --version
```

## 3. Crear el proyecto Django

Ejecuta:

```powershell
django-admin startproject config .
python manage.py startapp productos
```

El primer comando crea la configuración general de Django. El segundo crea la aplicación que administrará los productos.

La estructura inicial será parecida a esta:

```text
django_productos/
├── venv/
├── manage.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
└── productos/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── tests.py
    └── views.py
```

No es necesario modificar todos los archivos. Trabajaremos solamente con los que necesitamos para el CRUD.

## 4. Crear la base de datos en MongoDB Atlas

Utilizaremos MongoDB Atlas para que los aprendices no tengan que instalar y configurar un servidor de base de datos en sus computadores.

### 4.1. Crear la cuenta y el clúster

1. Ingresa a [MongoDB Atlas](https://www.mongodb.com/atlas).
2. Crea una cuenta o inicia sesión.
3. Crea un clúster del nivel gratuito disponible.
4. Crea un usuario de base de datos con contraseña.
5. En el acceso a la red, autoriza la dirección IP pública desde la cual trabajarás.
6. En el clúster, pulsa **Connect** y selecciona la opción de conexión para una aplicación.

No es necesario crear manualmente una colección. MongoDB podrá crearla cuando guardemos el primer producto.

### 4.2. Obtener la cadena de conexión

Atlas proporcionará una dirección parecida a esta:

```text
mongodb+srv://usuario:contraseña@cluster0.xxxxx.mongodb.net/
```

La dirección real tendrá el nombre de tu clúster. Utiliza la cadena que entrega Atlas, no copies literalmente el ejemplo.

**Importante:** no compartas la contraseña ni publiques la cadena de conexión en GitHub. Si la contraseña contiene caracteres especiales, puede ser necesario codificarlos correctamente en la URL.

## 5. Guardar la conexión de forma segura

Una buena práctica es separar las credenciales de la base de datos del código fuente.

### 5.1. Crear el archivo `.env`

En la raíz del proyecto, al mismo nivel que `manage.py`, crea un archivo llamado `.env`:

```text
django_productos/
├── .env
├── manage.py
├── config/
└── productos/
```

Dentro de `.env`, escribe:

```dotenv
MONGO_URI="PEGA_AQUI_LA_CADENA_DE_ATLAS"
MONGO_DB="t"
```

Reemplaza el valor de `MONGO_URI` por tu cadena real de conexión.

### 5.2. Proteger las credenciales

Crea un archivo `.gitignore` en la raíz del proyecto:

```gitignore
venv/
__pycache__/
*.py[cod]
.env
db.sqlite3
```

Esto evita incluir las credenciales en los cambios que se suban al repositorio Git.

## 6. Configurar Django

Abre `config/settings.py`.

Al principio del archivo, agrega estos imports. Si `Path` ya está importado, no lo dupliques:

```python
import os
from pathlib import Path
from dotenv import load_dotenv
```

Busca la línea que define `BASE_DIR`:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

Inmediatamente después, agrega:

```python
load_dotenv(BASE_DIR / ".env")
```

Al final de `settings.py`, agrega:

```python
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB", "tienda")
```

Registra también la aplicación. Busca `INSTALLED_APPS` y agrega `"productos"` sin eliminar las aplicaciones que Django creó automáticamente:

```python
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "productos",
]
```

## 7. Crear la conexión con MongoDB

Dentro de la carpeta `productos`, crea el archivo `db.py`.

Ruta: `productos/db.py`

```python
from django.conf import settings
from pymongo import MongoClient


if not settings.MONGO_URI:
    raise RuntimeError(
        "Falta configurar MONGO_URI en el archivo .env"
    )


cliente = MongoClient(
    settings.MONGO_URI,
    serverSelectionTimeoutMS=5000
)

db = cliente[settings.MONGO_DB]

coleccion_productos = db["productos"]
```

### ¿Qué hace este código?

- `MongoClient()` crea el cliente de conexión.
- `settings.MONGO_URI` obtiene la dirección configurada.
- `settings.MONGO_DB` indica qué base de datos utilizaremos.
- `db["productos"]` selecciona la colección que guardará los productos.

El tiempo de espera de cinco segundos evita que algunas operaciones queden esperando demasiado ante problemas de conexión. `MongoClient` puede reutilizarse; no necesitamos crear un cliente nuevo para cada producto.

## 8. Comprender cómo se almacenan los productos

En PostgreSQL, el CRUD anterior utilizaba tablas y filas. En MongoDB, trabajaremos con una colección de documentos.

Un producto podría almacenarse así:

```json
{
  "_id": "identificador generado por MongoDB",
  "nombre": "Teclado",
  "precio": 85000.0,
  "cantidad": 10
}
```

El campo `_id` identifica de manera única el documento. MongoDB normalmente genera un `ObjectId` automáticamente.

| Campo | Tipo | Ejemplo |
|---|---|---|
| `nombre` | Texto | Teclado |
| `precio` | Número | 85000 |
| `cantidad` | Entero | 10 |

No vamos a crear un modelo de Django para representar los productos. PyMongo trabajará directamente con los documentos de la colección.

## 9. Crear las vistas del CRUD

Abre `productos/views.py` y reemplaza su contenido por este código. Incluye validación en el servidor, mensajes para el usuario, identificación de documentos y manejo de errores de MongoDB.

```python
import math

from bson import ObjectId
from bson.errors import InvalidId

from django.contrib import messages
from django.shortcuts import render, redirect

from pymongo.errors import PyMongoError

from .db import coleccion_productos


def validar_producto(datos):
    """Valida los datos recibidos del formulario."""

    nombre = datos.get("nombre", "").strip()
    precio_texto = datos.get("precio", "").strip()
    cantidad_texto = datos.get("cantidad", "").strip()

    errores = []

    if not nombre:
        errores.append("El nombre es obligatorio.")
    elif len(nombre) > 100:
        errores.append("El nombre no puede superar 100 caracteres.")

    try:
        precio = float(precio_texto)

        if not math.isfinite(precio) or precio < 0:
            errores.append(
                "El precio debe ser un número válido y no negativo."
            )
    except ValueError:
        precio = None
        errores.append("Ingresa un precio válido.")

    try:
        cantidad = int(cantidad_texto)

        if cantidad < 0:
            errores.append("La cantidad no puede ser negativa.")
    except ValueError:
        cantidad = None
        errores.append("La cantidad debe ser un número entero.")

    producto = {
        "nombre": nombre,
        "precio": precio,
        "cantidad": cantidad,
    }

    return producto, errores


def listar(request):
    """Consulta y muestra los productos."""

    try:
        datos = list(
            coleccion_productos.find().sort("nombre", 1)
        )

        return render(
            request,
            "productos/lista.html",
            {"productos": datos},
        )

    except PyMongoError:
        messages.error(
            request,
            "No fue posible consultar los productos. "
            "Verifica la conexión con MongoDB."
        )

        return render(
            request,
            "productos/lista.html",
            {"productos": []},
        )


def crear(request):
    """Registra un producto."""

    if request.method == "POST":
        producto, errores = validar_producto(request.POST)

        if errores:
            for error in errores:
                messages.error(request, error)

            return render(
                request,
                "productos/formulario.html",
                {"producto": producto},
            )

        try:
            coleccion_productos.insert_one(producto)

            messages.success(
                request,
                "Producto registrado correctamente."
            )

            return redirect("productos:listar")

        except PyMongoError:
            messages.error(
                request,
                "No fue posible guardar el producto."
            )

            return render(
                request,
                "productos/formulario.html",
                {"producto": producto},
            )

    return render(request, "productos/formulario.html")


def editar(request, id):
    """Actualiza un producto existente."""

    try:
        identificador = ObjectId(id)
    except (InvalidId, TypeError):
        messages.error(request, "El identificador no es válido.")
        return redirect("productos:listar")

    try:
        producto_actual = coleccion_productos.find_one(
            {"_id": identificador}
        )

        if producto_actual is None:
            messages.error(request, "El producto no existe.")
            return redirect("productos:listar")

        if request.method == "POST":
            producto, errores = validar_producto(request.POST)

            if errores:
                for error in errores:
                    messages.error(request, error)

                producto["_id"] = identificador

                return render(
                    request,
                    "productos/formulario.html",
                    {"producto": producto},
                )

            resultado = coleccion_productos.update_one(
                {"_id": identificador},
                {"$set": producto},
            )

            if resultado.matched_count == 0:
                messages.error(request, "El producto ya no existe.")
            else:
                messages.success(
                    request,
                    "Producto actualizado correctamente."
                )

            return redirect("productos:listar")

        return render(
            request,
            "productos/formulario.html",
            {"producto": producto_actual},
        )

    except PyMongoError:
        messages.error(
            request,
            "No fue posible consultar o actualizar el producto."
        )

        return redirect("productos:listar")


def eliminar(request, id):
    """Elimina un producto mediante POST."""

    if request.method != "POST":
        messages.error(
            request,
            "La eliminación requiere enviar el formulario."
        )
        return redirect("productos:listar")

    try:
        identificador = ObjectId(id)
    except (InvalidId, TypeError):
        messages.error(request, "El identificador no es válido.")
        return redirect("productos:listar")

    try:
        resultado = coleccion_productos.delete_one(
            {"_id": identificador}
        )

        if resultado.deleted_count == 1:
            messages.success(
                request,
                "Producto eliminado correctamente."
            )
        else:
            messages.error(
                request,
                "El producto no existe o ya fue eliminado."
            )

    except PyMongoError:
        messages.error(
            request,
            "No fue posible eliminar el producto."
        )

    return redirect("productos:listar")
```

### 9.1. Comprender las vistas

La función `validar_producto()` centraliza la validación de los datos. Así evitamos duplicar las mismas comprobaciones al crear y editar.

| Operación | Instrucción | Significado |
|---|---|---|
| Crear | `insert_one(producto)` | Inserta un documento. |
| Consultar | `find()` | Recupera documentos. |
| Editar | `update_one(filtro, cambios)` | Modifica un documento. |
| Eliminar | `delete_one(filtro)` | Borra un documento. |

En las operaciones de edición y eliminación, el filtro utiliza `_id`. Así actuamos sobre un producto específico, en lugar de modificar o borrar toda la colección.

## 10. Crear las URL de la aplicación

Crea `productos/urls.py`:

```python
from django.urls import path
from . import views


app_name = "productos"

urlpatterns = [
    path("", views.listar, name="listar"),
    path("crear/", views.crear, name="crear"),
    path("editar/<str:id>/", views.editar, name="editar"),
    path("eliminar/<str:id>/", views.eliminar, name="eliminar"),
]
```

Ahora abre `config/urls.py` y reemplaza su contenido por:

```python
from django.contrib import admin
from django.urls import include, path


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("productos.urls")),
]
```

Las URL indican qué vista debe ejecutarse cuando el usuario visita una dirección o envía un formulario.

## 11. Crear el formulario HTML

El mismo formulario servirá para crear y editar productos, evitando mantener dos archivos casi iguales.

Crea las carpetas siguientes dentro de `productos`:

```text
productos/
├── templates/
│   └── productos/
│       ├── formulario.html
│       └── lista.html
├── db.py
├── urls.py
└── views.py
```

Abre `productos/templates/productos/formulario.html` y copia:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Formulario de productos</title>
</head>
<body>

    <h1>
        {% if producto %}
            Editar producto
        {% else %}
            Registrar producto
        {% endif %}
    </h1>

    {% if messages %}
        {% for message in messages %}
            <p>{{ message }}</p>
        {% endfor %}
    {% endif %}

    <form method="POST">
        {% csrf_token %}

        <p>
            <label for="nombre">Nombre del producto:</label><br>
            <input
                id="nombre"
                type="text"
                name="nombre"
                maxlength="100"
                value="{{ producto.nombre|default:'' }}"
                required
            >
        </p>

        <p>
            <label for="precio">Precio:</label><br>
            <input
                id="precio"
                type="number"
                name="precio"
                min="0"
                step="0.01"
                value="{{ producto.precio|default:'' }}"
                required
            >
        </p>

        <p>
            <label for="cantidad">Cantidad disponible:</label><br>
            <input
                id="cantidad"
                type="number"
                name="cantidad"
                min="0"
                step="1"
                value="{{ producto.cantidad|default:'' }}"
                required
            >
        </p>

        <button type="submit">Guardar producto</button>
    </form>

    <p>
        <a href="{% url 'productos:listar' %}">
            Volver al inventario
        </a>
    </p>

</body>
</html>
```

### 11.1. Comprender el formulario

- `method="POST"` envía los datos al servidor.
- `{% csrf_token %}` incorpora la protección CSRF de Django.
- `value="{{ producto.nombre|default:'' }}"` muestra el valor actual al editar y deja el campo vacío al crear.
- `required`, `min` y `step` ayudan al usuario, pero no reemplazan la validación en Python.

## 12. Crear la lista de productos

Abre `productos/templates/productos/lista.html` y copia:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventario de productos</title>
</head>
<body>

    <h1>Inventario de productos</h1>

    {% if messages %}
        {% for message in messages %}
            <p>{{ message }}</p>
        {% endfor %}
    {% endif %}

    <p>
        <a href="{% url 'productos:crear' %}">
            Registrar nuevo producto
        </a>
    </p>

    <hr>

    {% for producto in productos %}

        <h2>{{ producto.nombre }}</h2>

        <p>
            <strong>Precio:</strong>
            ${{ producto.precio }}
        </p>

        <p>
            <strong>Cantidad disponible:</strong>
            {{ producto.cantidad }}
        </p>

        <p>
            <a href="{% url 'productos:editar' producto._id %}">
                Editar
            </a>
        </p>

        <form
            method="POST"
            action="{% url 'productos:eliminar' producto._id %}"
        >
            {% csrf_token %}

            <button
                type="submit"
                onclick="return confirm('¿Deseas eliminar este producto?')"
            >
                Eliminar
            </button>
        </form>

        <hr>

    {% empty %}

        <p>No hay productos registrados.</p>

    {% endfor %}

</body>
</html>
```

**Importante:** utilizamos `producto._id` en los enlaces de edición y eliminación porque PyMongo devuelve el identificador de MongoDB con ese nombre. No debemos usar `producto.id`.

## 13. Ejecutar las migraciones de Django

Aunque los productos se guardarán en MongoDB, Django conserva su configuración predeterminada de SQLite para sus propios componentes, como las sesiones.

Ejecuta:

```powershell
python manage.py migrate
```

Este comando crea las tablas de los componentes internos de Django. **No crea la colección de productos en MongoDB.** La colección aparecerá cuando se inserte el primer documento.

No necesitas ejecutar `makemigrations`, porque no hemos creado modelos Django para los productos.

## 14. Comprobar la configuración y ejecutar

Desde la carpeta del proyecto, activa el entorno virtual en PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

Si prefieres no activarlo, ejecuta Python directamente desde el entorno virtual:

```powershell
.\venv\Scripts\python.exe manage.py check
.\venv\Scripts\python.exe manage.py runserver
```

Usar esta ruta evita depender del comando global `python` de Windows. Si
PowerShell indica que no encuentra `.\venv\Scripts\python.exe`, comprueba que
la terminal esté ubicada en la carpeta raíz del proyecto y que el entorno
virtual se haya creado.

Si activaste el entorno virtual, también puedes usar el comando `python`:

```powershell
python manage.py check
python manage.py runserver
```

Abre el navegador en:

http://127.0.0.1:8000/

La página mostrará el inventario, que inicialmente estará vacío.

## 15. Probar las cuatro operaciones CRUD

### Crear

Registra un producto con estos datos:

- Nombre: Teclado.
- Precio: 85000.
- Cantidad: 10.

Guarda el formulario y comprueba que aparezca en el inventario.

### Consultar

Verifica que el producto registrado se muestre con su precio y cantidad.

### Editar

Pulsa **Editar**, cambia la cantidad de 10 a 15 y guarda los cambios.

Comprueba que el inventario muestre la nueva cantidad.

### Eliminar

Pulsa **Eliminar** y confirma la acción si el navegador lo solicita.

Comprueba que el producto desaparezca de la lista.

### Validar

Intenta registrar un precio negativo o una cantidad decimal. La aplicación debe rechazar los datos que no cumplan las reglas de validación.

### Verificar persistencia

Detén el servidor con `Ctrl + C`, vuelve a iniciarlo y comprueba que los productos que no eliminaste sigan guardados.

## 16. Verificar los datos en MongoDB Atlas

Después de registrar un producto:

1. Ingresa a MongoDB Atlas.
2. Abre tu clúster.
3. Entra a **Browse Collections** o al explorador de datos.
4. Busca la base de datos `tienda`.
5. Abre la colección `productos`.

Deberás encontrar documentos con una estructura similar a esta:

```json
{
  "_id": "ObjectId generado por MongoDB",
  "nombre": "Teclado",
  "precio": 85000.0,
  "cantidad": 10
}
```

El valor de `_id` que aparece en Atlas será un identificador real de tipo `ObjectId`, no el texto ilustrativo del ejemplo.

## 17. Buenas prácticas aplicadas

| Buena práctica | ¿Por qué importa? |
|---|---|
| Entorno virtual | Aísla las dependencias. |
| Archivo `.env` | Separa las credenciales del código. |
| `.gitignore` | Evita subir secretos al repositorio. |
| Validación en el servidor | Impide aceptar datos inválidos enviados directamente al servidor. |
| Función `validar_producto()` | Evita duplicar las reglas de validación. |
| Archivo `db.py` | Centraliza la conexión con MongoDB. |
| Identificación mediante `_id` | Permite seleccionar el documento correcto. |
| Protección CSRF | Protege los formularios POST de Django. |
| Manejo de errores | Permite responder a fallos comunes de conexión. |
| Consultas con filtros | Limita las actualizaciones y eliminaciones al documento correspondiente. |

Esta aplicación es adecuada como práctica académica. Para producción todavía habría que reforzar la gestión de errores, la autenticación, los permisos, las pruebas y la configuración de despliegue.

## 18. Reto para los aprendices

Una vez que el CRUD funcione, realiza estos cambios:

1. Agrega un campo `categoria` para clasificar los productos.
2. Muestra la categoría en el inventario.
3. Permite modificarla desde el formulario.
4. Comprueba que también se guarde en MongoDB.

**Condición:** el nuevo campo debe funcionar al crear, consultar y editar productos. No basta con agregarlo al HTML; también debe incorporarse en la validación del servidor.

## 19. ¿Qué aprendimos?

En la práctica anterior, con PostgreSQL, trabajamos con tablas y modelos de Django. En esta práctica utilizamos MongoDB directamente a través de PyMongo.

Las operaciones esenciales son:

```python
# Crear
coleccion_productos.insert_one(producto)

# Consultar
coleccion_productos.find()

# Editar
coleccion_productos.update_one(
    {"_id": identificador},
    {"$set": producto}
)

# Eliminar
coleccion_productos.delete_one(
    {"_id": identificador}
)
```

La idea principal es que **Django sigue gestionando la aplicación web, pero PyMongo permite trabajar con documentos almacenados en MongoDB en lugar de utilizar el ORM de Django para los productos**.

Esta comparación permite comprender que se puede conservar buena parte de la estructura de una aplicación web y cambiar la forma en que se almacenan y consultan los datos.
