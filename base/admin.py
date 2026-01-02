from django.contrib import admin
from .models import Equipo, Tarea, Proyecto, Comentario, Perfil

# Register your models here.

admin.site.register(Tarea)
admin.site.register(Equipo)
admin.site.register(Comentario)
admin.site.register(Proyecto)
admin.site.register(Perfil)
