# Simulador Ecommerce "Davent"

Desarrollé esta aplicación web utilizando Django para simular un ecosistema completo de e-commerce. Mi objetivo fue crear una plataforma robusta donde los usuarios puedan explorar productos, gestionar un carrito dinámico en tiempo real y completar procesos de compra simulados, todo bajo una arquitectura escalable y segura.

## Características Principales

*   **Catálogo de Productos:** Implementé una visualización detallada con gestión de imágenes y valoraciones.
*   **Filtros Avanzados:** Diseñé un sistema de búsqueda y filtrado interactivo por categorías, marcas y rangos de precio.
*   **Sistema de Autenticación:** Configuré un flujo de registro y login con validaciones personalizadas y seguridad avanzada.
*   **Gestión de Perfil:** Permití a los usuarios personalizar su experiencia, incluyendo la actualización de datos y fotos de perfil.
*   **Carrito de Compras Dinámico:** Esta es una de las partes clave; utilicé **HTMX** para lograr actualizaciones en tiempo real sin recargar la página, optimizando la experiencia de usuario (UX).
*   **Simulación de Pedidos:** Desarrollé la lógica para registrar ventas y detalles de compra vinculados a cada usuario.
*   **Valoraciones y Comentarios:** Creé un sistema de feedback social que permite calificar con estrellas y comentar productos.
*   **Panel de Administración Propio:** Además del admin de Django, construí una interfaz personalizada para la gestión interna del inventario y usuarios.

## Tecnologías Utilizadas

### Backend
*   Python 3.12.2
*   Django 5.0.2
*   psycopg2-binary (para conexión con PostgreSQL)
*   Pillow (para procesamiento de imágenes)

### Frontend
*   HTML5
*   CSS3
*   JavaScript
*   **HTMX:** Para interacciones dinámicas y actualizaciones parciales de la página (ej. carrito de compras).
*   **Bootstrap 5.3:** Para componentes y layout responsivo.
*   **Font Awesome:** Para la iconografía.

### Base de Datos
*   PostgreSQL

## Estructura de la Base de Datos (Modelos Principales)

*   **User & Perfil:** Extensión del modelo de autenticación nativo para incluir saldos y multimedia.
*   **Products, Category & Brand:** Estructura relacional para la gestión del catálogo.
*   **Sales & Detail_Sale:** Lógica transaccional para el registro histórico de pedidos.
*   **Comments & Valoration:** Modelos para la interacción y analítica de satisfacción del cliente.

## Mi Proceso de Desarrollo

Durante la creación de "Davent", puse especial énfasis en la validación de datos tanto en el frontend como en el backend, asegurando que el stock y los precios se manejen con precisión decimal. La integración de HTMX fue un reto técnico que elegí para demostrar cómo mejorar la interactividad sin la complejidad de un framework de JS pesado.

---
## Guía de Configuración Local

Sigue estos pasos para configurar y ejecutar el proyecto en tu máquina local:

1.  **Clonar el Repositorio:**
    ```bash
    git clone https://github.com/davidcv28/Davent-Ecommerce.git
    cd Davent-Ecommerce
    ```

2.  **Crear y Activar el Entorno Virtual:**
    ```bash
    # Crear el entorno
    python -m venv venv

    # Activar en Windows (PowerShell):
    .\venv\Scripts\Activate.ps1

    # Activar en Linux/macOS:
    source venv/bin/activate
    ```

3.  **Instalar Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configuración de la Base de Datos (PostgreSQL):**
    *   Crea una base de datos PostgreSQL vacía (ej. `davent_db`).
    *   En el archivo `sistema_ecommerce/settings.py`, localiza la sección `DATABASES` y actualiza las credenciales (`NAME`, `USER`, `PASSWORD`, `HOST`, `PORT`).
    *   **Recomendación:** Utiliza variables de entorno para mantener seguras tus credenciales. Puedes usar un archivo `.env` y una librería como `python-dotenv`.

5.  **Aplicar Migraciones:**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6.  **Crear un Superusuario:**
    Este usuario tendrá acceso al panel de administración de Django (`/admin`) y a las vistas de administración personalizadas.
    ```bash
    python manage.py createsuperuser
    ```

7.  **Ejecutar el Servidor de Desarrollo:**
    ```bash
    python manage.py runserver
    ```
    La aplicación estará disponible en `http://127.0.0.1:8000/`.

## Uso de la Aplicación

*   **Explorar Productos:** Navega por la página principal o la sección "Productos" para ver el catálogo.
*   **Aplicar Filtros:** En la página de productos, utiliza la barra lateral para buscar y filtrar por categoría, marca o precio.
*   **Crear Cuenta:** Regístrate para poder comprar, comentar y gestionar tu perfil.
*   **Añadir al Carrito:** Desde la página de detalle de un producto, puedes seleccionar la cantidad y añadirlo al carrito.
*   **Gestionar Perfil:** Accede a tu cuenta desde el menú de usuario para actualizar tu información personal y foto.
*   **Realizar Pedido:** Ve a tu carrito de compras y confirma la compra para simular un pedido.

---

## Contacto

Si tienes preguntas o comentarios, puedes contactarme en:

*   **Email:** davidcv28@outlook.com
*   **LinkedIn:** David Cervantes
*   **GitHub:** davidcv28