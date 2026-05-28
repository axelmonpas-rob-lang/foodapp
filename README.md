# FoodApp - Documentación Técnica 🍳

¡Bienvenido a **FoodApp**! Una aplicación web desarrollada con **Django** que funciona como un catálogo interactivo de recetas de cocina. Este proyecto fue desarrollado para la materia *Implementa Bases de Datos Relacionales en Sistemas de Información* del **CBTIS No. 116**.

---

## 👥 Integrantes del Equipo (Equipo 4)
* **Docente:** José Christian Romero Hernández
* **Integrantes:**
    * Roblero Sánchez Kevin
    * Perez Rivera Kevin Salvador
    * Monrroy Pastrana Axel Aron
    * Serrano Aviña Kyara Zoe
    * Robles Arballo Luis Humberto
* **Fecha de entrega:** 28 de mayo de 2026

---

## 📌 1. Introducción
El objetivo principal de **FoodApp** es ofrecer a los usuarios una plataforma interactiva donde puedan explorar recetas de distintos países, filtrarlas por categoría y guardarlas en una lista de favoritos. 

La aplicación organiza las recetas por nivel de dificultad (fácil, medio, difícil), tipo de platillo (comida, postre, bebida) y origen. Integra:
* Autenticación de usuarios y control de roles (Usuario normal y Vendedor).
* Operaciones CRUD completas para la gestión de recetas.
* Base de datos relacional administrada mediante el ORM de Django.

---

## 🗄️ 2. Desarrollo y Arquitectura

### 2.1 Modelos (Base de Datos)
El proyecto implementa una base de datos **SQLite** con 5 modelos principales:

1.  **Usuario (Custom User):** Extiende el modelo por defecto agregando el rol `is_seller` (booleano) para identificar administradores de contenido.
2.  **Categorías:** Contiene el nombre (`Name`) y descripción opcional de los tipos de platillos.
3.  **Recetas:** Almacena la información del platillo (nombre, descripción, dificultad, ingredientes, imagen, fecha de creación) y se conecta con el dueño (`Owner`) y sus categorías.
4.  **Favorito:** Lista de favoritos perteneciente a cada usuario.
5.  **RecetaF:** Tabla intermedia para la relación de favoritos, garantizando recetas únicas por lista (`unique_together`).

> **Nota técnica:** Todos los modelos utilizan `UUIDField` como llave primaria (PK) en lugar de IDs incrementales tradicionales para mayor seguridad.

### 2.2 Relaciones entre Modelos
* **Usuario ➡️ Recetas:** ($1 \rightarrow N$) Un usuario vendedor puede registrar muchas recetas.
* **Recetas ↔️ Categorías:** ($N \leftrightarrow M$) Una receta puede tener varias categorías y una categoría albergar muchas recetas.
* **Usuario ➡️ Favorito:** ($1 \rightarrow N$) Cada usuario gestiona su lista de favoritos (controlado mediante `get_or_create`).
* **Favorito ↔️ Recetas:** ($N \leftrightarrow M$ vía `RecetaF`) Una lista tiene muchas recetas y una receta puede estar en muchas listas.

---

## ⚙️ 2.3 Configuración (`settings.py`)
Puntos clave configurados en el entorno de Django:
* **Base de datos:** `django.db.backends.sqlite3` apuntando a `db.sqlite3`.
* **Modelo de usuario:** `AUTH_USER_MODEL = 'recetas_app.Usuario'`
* **Archivos Multimedia:** Rutas `MEDIA_URL = 'media/'` y `MEDIA_ROOT` enlazado al directorio local.

---

## 🗺️ 2.4 Rutas y URLs del Proyecto

| Ruta | Nombre de URL | Función / Vista |
| :--- | :--- | :--- |
| `/` | `home` | Página principal con catálogo de recetas y filtros |
| `/register/` | `register` | Registro de nuevos usuarios |
| `/login/` | `login` | Inicio de sesión |
| `/logout/` | `logout` | Cierre de sesión |
| `/dashboard/` | `dashboard` | Panel del vendedor (Requiere rol `is_seller`) |
| `/products/create/` | `product_create` | Crear nueva receta |
| `/products/<id>/edit/` | `product_update` | Editar receta existente |
| `/products/<id>/delete/` | `product_delete` | Eliminar receta permanentemente |
| `/cart/` | `cart_detail` | Ver lista de favoritos |
| `/cart/add/<id>/` | `add_to_cart` | Agregar receta a favoritos |
| `/cart/remove/<id>/` | `remove_from_cart` | Eliminar receta de favoritos |

---

## 💻 2.5 Vistas Principales (`views.py`)
* **`home`:** Utiliza `select_related` y `prefetch_related` para optimizar consultas a la base de datos. Implementa paginación de 6 elementos por página.
* **Control de Acceso:** Las vistas del CRUD verifican que el usuario esté autenticado y sea el dueño de la receta antes de permitir modificaciones. El `dashboard` bloquea el acceso con un error 403 si el usuario no es vendedor.

---

## 🎨 2.6 Interacción con Templates
La interfaz web utiliza el motor de plantillas de Django bajo una estructura de herencia:
* `base.html`: Muestra la barra de navegación dinámica (cambia según si el usuario inició sesión o si es vendedor).
* `home.html`: Renderiza las tarjetas de las recetas con su respectiva imagen, un buscador (`q`) y los botones dinámicos para añadir a favoritos mediante `{% url 'add_to_cart' product.id %}`.