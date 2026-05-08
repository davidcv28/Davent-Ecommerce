# Documentación de Serializadores - `app_ecommerce`

Este documento detalla los serializadores utilizados en la aplicación `app_ecommerce` para la API REST. Los serializadores son responsables de convertir objetos complejos, como los querysets y modelos de Django, en tipos de datos nativos de Python que luego pueden ser fácilmente renderizados en `JSON`, `XML` u otros tipos de contenido. También se encargan de la deserialización y validación de datos de entrada.

## Serializadores de Usuario (Administradores)

Estos serializadores están diseñados para ser utilizados por usuarios con permisos de administrador o staff.

### `ReadStafUserSerializer`

*   **Propósito**: Serializador de solo lectura para obtener una vista detallada de los usuarios del sistema.
*   **Modelo**: `django.contrib.auth.models.User`
*   **Campos**:
    *   `id`
    *   `username`
    *   `email`
    *   `first_name`
    *   `last_name`
    *   `is_active`
    *   `is_staff`
    *   `date_joined`
*   **Notas**: Todos los campos son de solo lectura (`read_only`).

### `RegisterStaffUserSerializer`

*   **Propósito**: Permite a los administradores registrar nuevos usuarios con control sobre todos sus atributos.
*   **Modelo**: `django.contrib.auth.models.User`
*   **Campos**:
    *   Todos los campos del modelo `User`.
    *   `password2`: Campo de solo escritura para confirmar la contraseña.
*   **Validaciones**:
    *   `username`: Debe tener al menos 6 caracteres y contener un mínimo de 3 letras.
    *   `email`: El dominio del correo debe ser uno de los permitidos (`@gmail.com`, `@hotmail.com`, `@yahoo.com`, `@outlook.com`).
    *   `password` y `password2` deben coincidir.
*   **Notas**: El campo `password` es de solo escritura y es requerido. El `email` también es requerido.

---

## Serializadores de Usuario (Públicos y Autenticados)

Estos serializadores son para el uso de usuarios finales, ya sea para autenticación, registro o gestión de su propia cuenta.

### `AuthTokenSerializer`

*   **Propósito**: Autenticar a un usuario a través de su `username` y `password` para generar un token de acceso.
*   **Modelo**: No es un `ModelSerializer`.
*   **Campos**:
    *   `username` (solo escritura)
    *   `password` (solo escritura)
    *   `token` (solo lectura)
*   **Validaciones**:
    *   Utiliza la función `authenticate` de Django para verificar las credenciales.
    *   Si la autenticación falla, lanza una `ValidationError` con el mensaje "Esta cuenta no existe".

### `ReadUserSerializer`

*   **Propósito**: Serializador de solo lectura para mostrar información básica y pública de un usuario.
*   **Modelo**: `django.contrib.auth.models.User`
*   **Campos**:
    *   `username`
    *   `first_name`
    *   `last_name`
*   **Notas**: Todos los campos son de solo lectura.

### `RegisterUserSerializer`

*   **Propósito**: Permite a cualquier visitante registrarse como un nuevo usuario en la plataforma.
*   **Modelo**: `django.contrib.auth.models.User`
*   **Campos**:
    *   `username`
    *   `email`
    *   `password` (solo escritura)
    *   `password2` (solo escritura, para confirmación)
*   **Validaciones**:
    *   `email`: Valida que el dominio del correo sea uno de los permitidos.
    *   `password` y `password2` deben coincidir.
*   **Notas**: Sobrescribe el método `create` para usar `User.objects.create_user()`, asegurando que la contraseña se guarde hasheada correctamente.

### `UpdateUserSerializer`

*   **Propósito**: Permite a un usuario autenticado actualizar su propia información personal.
*   **Modelo**: `django.contrib.auth.models.User`
*   **Campos**:
    *   `username` (solo lectura)
    *   `first_name`
    *   `last_name`
    *   `email`
*   **Validaciones**:
    *   `email`: Valida que el dominio del correo sea uno de los permitidos.
*   **Notas**: El `username` no puede ser modificado a través de este serializador.

---

## Serializadores de Productos

Estos serializadores gestionan la representación de los productos del e-commerce.

### `ProductsSerializer`

*   **Propósito**: Serializador de solo lectura para listar y ver los detalles de los productos.
*   **Modelo**: `app_ecommerce.models.Products`
*   **Campos**:
    *   `id`
    *   `name_product`
    *   `price_product`
    *   `stock_product`
    *   `img_product`
    *   `brand_product` (representado como string)
    *   `category_product` (representado como string)
*   **Notas**: Utiliza `StringRelatedField` para mostrar los nombres de la marca y la categoría en lugar de sus IDs.

### `EditproductSerializer`

*   **Propósito**: Permite la creación y actualización de productos. Diseñado para usuarios con permisos de staff.
*   **Modelo**: `app_ecommerce.models.Products`
*   **Campos**:
    *   Todos los campos del modelo `Products`.
    *   `brand_product` y `category_product` son campos de solo escritura que aceptan el ID de la marca/categoría.
*   **Validaciones**:
    *   `name_product`: Longitud entre 4 y 50 caracteres, con al menos 3 letras. Debe ser único.
    *   `price_product`: Debe ser un valor válido entre 1 y 999,999,999.
    *   `stock_product`: Debe ser un valor válido entre 1 y 9999.
    *   `img_product`: Si se proporciona, debe ser de tipo `image/png` y no superar los 5MB.
*   **Notas**: Este serializador es más completo y está pensado para la gestión interna de productos.
