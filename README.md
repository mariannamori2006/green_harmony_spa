# 🌿 Green Harmony Spa · Sistema de Gestión de Spa y Bienestar

Sistema web integral desarrollado en **Django** para la administración, control de citas, valoraciones estéticas de clientes, catálogo visual de servicios con fotografías y gestión financiera de cobros en centros de estética, spas y salones de bienestar.

---

## ✨ Características Principales

* **📸 Catálogo Visual de Servicios con Fotografías:** Carga dinámica de imágenes para cada tratamiento y servicio con almacenamiento multimedia administrado mediante **Pillow**.
* **🎴 Diseño Creativo en Tarjetas (Visual Cards):** En lugar de aburridas tablas monótonas de hoja de cálculo, el sistema presenta la información mediante tarjetas visuales adaptadas a cada entidad:
  * **💆‍♀️ Fichas de Diagnóstico Estético (Valoraciones):** Avatar con monograma de iniciales, etiqueta botánica de *Tipo de Piel*, cuadro de diagnóstico clínico y caja destacada de *Recomendaciones del especialista*.
  * **📅 Agenda de Citas:** Tarjetas con bloque de calendario visual (día y mes), chip de hora (`09:30`), especialista asignado, servicio, precio y distintivo de estado.
  * **💳 Recibos de Pagos:** Fichas de comprobante financiero con monto total destacado, desglose de descuentos, insignia de método de pago y fecha.
  * **👥 Directorio de Clientes y Terapeutas:** Fichas de perfil con avatar degradado y accesos rápidos a teléfono, correo, DNI y dirección.
  * **✨ Áreas y Especialidades:** Tarjetas de bienestar con íconos vectoriales y descripción.
* **🔄 Selector de Vista Interactivo (🎴 Tarjetas / 📋 Tabla):** Conmutador en cabecera para alternar entre vista creativa de tarjetas y tabla tradicional compacta en un solo clic, con memoria automática en el navegador (`localStorage`).
* **🌟 Panel de Inicio con Fotografía y Glassmorphism:** Banner hero con fotografía ambiental de spa, efecto de cristal esmerilado translúcido (*backdrop-filter*), cifras financieras destacadas y saludo dinámico.
* **🧘‍♂️ Experiencia de Acceso con Ken Burns:** Pantallas de Inicio de Sesión y Registro con presentación fotográfica animada en movimiento continuo (*Ken Burns slideshow*).
* **🔍 Buscador y Filtros en Fila:** Buscador horizontal con alineación uniforme y filtros dinámicos responsivos.
* **📊 Reportes e Impresión:** Generación de informes filtrados por fechas y estados, optimizados con estilos de impresión limpia y exportación a PDF.
* **📱 100% Responsivo:** Interfaz adaptable a pantallas de escritorio, tablets y móviles con menú lateral deslizable.
* **🔒 Seguridad y Roles:** Protección CSRF, sesiones seguras, validaciones de integridad y registro controlado por código de invitación.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.10+ / Django 6.x
* **Procesamiento de Imágenes:** Pillow (Python Imaging Library)
* **Base de datos:** MySQL / MariaDB (compatible con XAMPP)
* **Frontend:** HTML5 semántico, CSS3 moderno (CSS Grid, Flexbox, Glassmorphism, animaciones CSS) y JavaScript Vanilla (sin frameworks externos pesados).
* **Archivos estáticos y multimedia:** WhiteNoise (estáticos) y Django FileSystemStorage (multimedia de usuario).

---

## 📦 Requisitos Previos

Asegúrate de contar con lo siguiente instalado en tu equipo:

1. **Python 3.10 o superior** ([python.org](https://www.python.org/))
2. **Servidor MySQL o MariaDB** (puedes usar el módulo MySQL de [XAMPP](https://www.apachefriends.org/))
3. **Git** ([git-scm.com](https://git-scm.com/))

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para clonar y ejecutar el proyecto en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone https://github.com/TU_USUARIO/SalonSpa.git
cd SalonSpa
```

### 2. Crear y activar el entorno virtual

* **En Windows (PowerShell):**
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate
  ```

* **En Linux / macOS:**
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  ```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno
Copia el archivo de plantilla `.env.example` y nómbralo `.env`:

* **En Windows (PowerShell):**
  ```powershell
  Copy-Item .env.example .env
  ```
* **En Linux / macOS:**
  ```bash
  cp .env.example .env
  ```

Abre el archivo `.env` y configura tus credenciales de base de datos:
```ini
DJANGO_DEBUG=1
DJANGO_SECRET_KEY=clave-secreta-de-desarrollo
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DJANGO_CSRF_TRUSTED_ORIGINS=

DB_NAME=green_harmony_spa_db
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3308   # Usa 3306 o 3308 según la configuración de tu MySQL/XAMPP
```

### 5. Crear la base de datos en MySQL
En tu gestor de base de datos (phpMyAdmin o MySQL CLI), crea la base de datos:
```sql
CREATE DATABASE green_harmony_spa_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 6. Ejecutar migraciones
Aplica las tablas del sistema (incluyendo el soporte de fotografías para servicios):
```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Crear el usuario Administrador
Crea las credenciales de acceso inicial:
```bash
python manage.py createsuperuser
```

### 8. Iniciar el servidor de desarrollo
```bash
python manage.py runserver
```

Abre tu navegador en: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)

---

## 🖼️ Manejo de Archivos Multimedia (Imágenes de Servicios)

* Las imágenes cargadas por los usuarios se almacenan en la carpeta local `media/servicios/`.
* Durante el modo de desarrollo (`DEBUG=True`), Django sirve automáticamente estos archivos a través de la ruta `/media/`.
* Esta carpeta está protegida e ignorada en el archivo `.gitignore` para no subir archivos de prueba o datos privados al repositorio de Git.

---

## 🌐 Pruebas remotas (Túnel con Cloudflare)

Para probar la aplicación en tu teléfono móvil o permitir que otros clientes o colegas la revisen a distancia sin necesidad de desplegar en producción:

```powershell
cloudflared tunnel --url http://localhost:8000
```
Copia la URL pública generada (`https://....trycloudflare.com`) y ábrela en cualquier navegador móvil o de escritorio.

---

## 📁 Estructura del Proyecto

```text
SalonSpa/
├── apps/                        # Aplicación principal de Django
│   ├── models/                  # Modelos de datos (Citas, Clientes, Pagos, Servicios, etc.)
│   ├── templates/control/       # Plantillas HTML (base, inicio, listados, formularios, login)
│   ├── static/control/          # Recursos estáticos
│   │   ├── css/styles.css       # Estilos CSS generales, tarjetas creativas y temas
│   │   ├── js/app.js            # Lógica JS (selector de vistas, modales, alertas)
│   │   └── img/                 # Logotipo, favicon e imágenes ambientales de spa
│   ├── views.py                 # Vistas, consultas optimizadas y controladores
│   ├── forms.py                 # Formularios y validaciones de datos
│   └── urls.py                  # Rutas internas de la aplicación
├── config/                      # Configuración global del proyecto Django
│   ├── settings.py              # Ajustes, base de datos, STORAGES, media y seguridad
│   ├── urls.py                  # Enrutador principal y servicio de media
│   └── wsgi.py                  # Punto de entrada WSGI
├── media/                       # Archivos multimedia subidos por los usuarios (fotos de servicios)
├── .env.example                 # Plantilla de variables de entorno
├── .gitignore                   # Archivos excluidos del control de versiones
├── manage.py                    # Gestor de comandos de Django
├── requirements.txt             # Librerías y dependencias (Django, Pillow, mysqlclient, etc.)
└── README.md                    # Documentación del proyecto
```

---

## 📄 Licencia

Este proyecto es de uso privado para **Green Harmony Spa**. Todos los derechos reservados.
