# 🌿 Green Harmony Spa · Sistema de Gestión de Spa y Bienestar

Sistema web integral desarrollado en **Django** para la administración, control de citas, valoraciones de clientes, catálogo de servicios y gestión de pagos en centros de estética, spas y salones de bienestar.

---

## ✨ Características Principales

* **📅 Control de Citas:** Programación, asignación de terapeutas, servicios y seguimiento de estados (*Pendiente, Confirmada, Atendida, Cancelada*).
* **💆‍♀️ Valoraciones Clínicas:** Registro del tipo de piel, diagnóstico y recomendaciones personalizadas por cliente.
* **💳 Gestión de Pagos:** Control de cobros, métodos de pago (Efectivo, Tarjeta, Transferencia, Yape/Plin), descuentos y estados (*Pagado, Anulado*).
* **📋 Catálogo de Servicios y Especialidades:** Definición de tiempos de duración, precios y áreas de especialidad del personal.
* **👥 Directorio de Personas:** Registro detallado de clientes y terapeutas.
* **📊 Reportes Avanzados e Impresión:** Filtrado dinámico por rangos de fecha y estados con vista optimizada para imprimir o guardar en PDF.
* **📱 Diseño 100% Responsivo:** Interfaz moderna y adaptable a computadoras, tablets y teléfonos móviles con barra de navegación lateral e iconos vectoriales.
* **🔒 Seguridad y Roles:** Autenticación con protección CSRF, sesiones protegidas y opción de registro controlado mediante código de invitación.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.10+ / Django 6.x
* **Base de datos:** MySQL / MariaDB (compatible con XAMPP)
* **Frontend:** HTML5 semántico, CSS3 moderno (Grid, Flexbox, variables CSS) y JavaScript Vanilla (sin frameworks pesados).
* **Archivos estáticos:** WhiteNoise

---

## 🚀 Requisitos Previos

Asegúrate de contar con lo siguiente instalado en tu sistema:

1. **Python 3.10 o superior** ([python.org](https://www.python.org/))
2. **Servidor MySQL o MariaDB** (puedes usar el módulo MySQL de [XAMPP](https://www.apachefriends.org/))
3. **Git** ([git-scm.com](https://git-scm.com/))

---

## 📦 Instalación y Puesta en Marcha

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
Aplica las tablas del sistema:
```bash
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

## 🌐 Pruebas remotas (Túnel con Cloudflare)

Para probar la aplicación en tu teléfono móvil o permitir que otros clientes/colegas la prueben a distancia sin desplegar a producción:

```powershell
cloudflared tunnel --url http://localhost:8000
```
Copia la URL pública generada (`https://....trycloudflare.com`) y ábrela en cualquier navegador.

---

## 📁 Estructura del Proyecto

```text
SalonSpa/
├── apps/                        # Aplicación principal de Django
│   ├── models/                  # Modelos de datos (Citas, Clientes, Pagos, etc.)
│   ├── templates/control/       # Plantillas HTML (base, inicio, reportes, etc.)
│   ├── static/control/          # Estilos CSS, scripts JS, iconos e imágenes
│   ├── views.py                 # Lógica de controladores y vistas
│   ├── forms.py                 # Formularios de validación
│   └── urls.py                  # Rutas internas de la aplicación
├── config/                      # Configuración global del proyecto Django
│   ├── settings.py              # Ajustes, base de datos y middleware
│   ├── urls.py                  # Enrutador principal
│   └── wsgi.py                  # Punto de entrada WSGI
├── .env.example                 # Plantilla de variables de entorno
├── .gitignore                   # Archivos excluidos de Git
├── manage.py                    # Gestor de comandos de Django
├── requirements.txt             # Librerías y dependencias del proyecto
└── README.md                    # Documentación del proyecto
```

---

## 📄 Licencia

Este proyecto es de uso privado para **Green Harmony Spa**. Todos los derechos reservados.

