# TaskFlow

**Gestión inteligente de tareas, proyectos y equipos**  
con roles, permisos estrictos, invitaciones seguras y comentarios en tiempo real.

[![GitHub top language](https://img.shields.io/github/languages/top/MauRyze22/Task_Flow)](https://github.com/MauRyze22/Task_Flow)
[![GitHub stars](https://img.shields.io/github/stars/MauRyze22/Task_Flow?style=social)](https://github.com/MauRyze22/Task_Flow)
[![GitHub last commit](https://img.shields.io/github/last-commit/MauRyze22/Task_Flow)](https://github.com/MauRyze22/Task_Flow)

## 📸 Vistas previas

<p align="center">
  <img src="screenshots/dashboard.png" alt="Dashboard principal" width="45%">
  <img src="screenshots/teams.png" alt="Todos los proyectos en tiempo real" width="45%">
</p>
<p align="center">
  <img src="screenshots/task-comments.png" alt="Comentarios en tiempo real" width="45%">
  <img src="screenshots/profile-user.png" alt="Sistema de logueo de usuario" width="45%">
</p>

## 📖 Sobre el proyecto

TaskFlow es una aplicación web completa para **gestionar tareas, proyectos y equipos** de forma segura.  
Nace para resolver el problema típico de herramientas gratuitas: o son demasiado simples (y caóticas) o demasiado caras y complejas.

Aquí cada usuario solo ve y edita **lo que le corresponde** según su rol.

## ✨ Características principales

- ✅ Creación y gestión de proyectos y tareas
- ✅ Sistema de roles y permisos granular (Administrador, Jefe de equipo, Miembro, Invitado)
- ✅ Invitaciones seguras por email (solo jefes pueden invitar)
- ✅ Comentarios en tiempo real en cada tarea
- ✅ Panel personal con mis tareas pendientes
- ✅ Edición de perfil de usuario: actualización de datos personales y foto de perfil
- ✅ Autenticación segura con Django (login, registro, cambio de contraseña)
- ✅ Soporte completo para PostgreSQL (fácil de deployar)

## 🛠️ Tecnologías utilizadas

- **Backend**: Python 3.10+ • Django
- **Frontend**: HTML5 • CSS3 • JavaScript • Bootstrap
- **Base de datos**: PostgreSQL (producción) + SQLite (pruebas rápidas)
- **Autenticación**: Django contrib.auth (built-in)
- **Otros**: python-dotenv (para variables de entorno)

## 🚀 Instalación rápida (desarrollo)

### Requisitos previos

- Python 3.10+  
- PostgreSQL (o usa SQLite para pruebas rápidas)  
- Git

### Pasos

```bash
# 1. Clonar el repositorio
git clone https://github.com/MauRyze22/Task_Flow.git
cd Task_Flow

# 2. Crear y activar entorno virtual
python -m venv venv
source venv/bin/activate    # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp .env.example .env
# Edita .env con tus datos (SECRET_KEY, DATABASE, etc.)

# 5. Aplicar migraciones y crear superusuario
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

# 6. Correr el servidor
python manage.py runserver

```
## 🤝 Contribuir

Este es un proyecto personal de portafolio mientras aprendo Django.  
Por ahora no acepto contribuciones externas, pero ¡cualquier sugerencia o feedback es súper bienvenido!  
Abre un issue con ideas, bugs o mejoras que veas. Gracias por el interés 🚀

## ✉️ Sobre mí / Contacto

Hola, soy **Amaury Monteagudo** — desarrollador backend en formación, enfocado en Python, Django, APIs seguras y bases de datos.

Este proyecto (TaskFlow) forma parte de mi portafolio personal para demostrar habilidades en:

- Autenticación y autorización (RBAC con roles y permisos granulares)
- Gestión de usuarios y equipos colaborativos
- Invitaciones seguras y control de acceso
- Buenas prácticas de Django (migraciones, entornos, PostgreSQL)

Estoy aprendiendo y mejorando constantemente, así que cualquier feedback, sugerencia o issue es **muy bienvenido** — ¡me ayuda a crecer!

📧 Email: amaurymonteagudop22@gmail.com  
🔗 GitHub: [@MauRyze22](https://github.com/MauRyze22)  
🔗 LinkedIn: [linkedin.com/in/amaury-monteagudo](https://www.linkedin.com/in/amaury-monteagudo-40375b3a5)

¡Gracias por tomarte el tiempo de ver mi proyecto! 🚀 Cualquier comentario suma muchísimo. 💙

## 📄 Licencia

[MIT License](LICENSE) — puedes usar, modificar y distribuir el código libremente (con el aviso de copyright).
