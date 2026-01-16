from django.urls import path
from . import views

urlpatterns = [
    # vista principal
    path('', views.home, name = 'home'),
    
    # url para usuario
    path('login-user/', views.login_user, name = 'login_user'),
    path('logout-user/', views.logout_user, name = 'logout_user'),
    path('register-user/', views.register_user, name = 'register_user'),
    path('profile-user/<int:pk>/', views.profile_user, name = 'profile_user'),
    path('actualizar_profile/<int:pk>/', views.actualizar_profile, name = 'actualizar_profile'),
    path('mostrar_profiles/', views.mostrar_profiles, name = 'mostrar_profiles'),
    
    # url para proyectos
    path('proyectos/', views.proyectos, name = 'proyectos'),
    path('create-proyecto/', views.create_proyecto, name = 'create_proyecto'),
    path('proyecto-detail/<int:pk>/', views.proyecto_detail, name = 'proyecto_detail'),
    path('proyecto-update/<int:pk>/', views.proyecto_update, name = 'proyecto_update'),
    path('proyecto-delete/<int:pk>', views.proyecto_delete, name = 'proyecto_delete'),    
    
    # url para tareas
    path('tareas/', views.tareas, name = 'tareas'),
    path('create-tarea/', views.create_tarea, name = 'create_tarea'),
    path('tarea-detail/<int:pk>/', views.tarea_detail, name = 'tarea_detail'),
    path('tarea-update/<int:pk>/', views.tarea_update, name = 'tarea_update'),
    path('tarea-delete/<int:pk>', views.tarea_delete, name = 'tarea_delete'),    
    
    
    #url para comentarios
    path('comentarios/', views.comentarios, name = 'comentarios'),
    path('create_comentario/', views.create_comentario, name = 'create_comentario'),
    path('comentario-update/<int:pk>/', views.comentario_update, name = 'comentario_update'),
    path('comentario-delete/<int:pk>', views.comentario_delete, name = 'comentario_delete'),
    
    # url para equipos
    path('equipos/', views.equipos, name = 'equipos'),
    path('create-equipo/', views.create_equipo, name = 'create_equipo'),
    path('equipo-detail/<int:pk>/', views.equipo_detail, name = 'equipo_detail'),
    path('equipo-update/<int:pk>/', views.equipo_update, name = 'equipo_update'),
    path('equipo-delete/<int:pk>', views.equipo_delete, name = 'equipo_delete'),
    
    # url para invitaciones:
    path('enviar_invitacion/<int:pk>/', views.enviar_invitacion, name = 'enviar_invitacion'),
    path('aceptar_invitacion/<uuid:token>/', views.aceptar_invitacion, name = 'aceptar_invitacion'),
    
]


