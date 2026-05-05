from django.contrib import admin

from base.models import Comentario, Equipo, Perfil, Proyecto, Tarea

admin.site.register(Tarea)
admin.site.register(Equipo)
admin.site.register(Comentario)
admin.site.register(Proyecto)
admin.site.register(Perfil)
