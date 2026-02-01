from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import EquipoForm, ProyectoForm, TareaForm, ComentarioForm, RegisterForm, PerfilForm, InvitacionForm
from .models import Equipo, Tarea, Proyecto, Comentario, Perfil, Invitacion
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse
from django.conf import settings
from django.core.mail import send_mail

# Create your views here.


@login_required(login_url='login_user')
def home(request):
    comentarios = Comentario.objects.filter(Q(user=request.user) |
                                            Q(tarea__proyecto__equipo__integrantes=request.user)
                                            ).select_related('user', 'tarea', 'tarea__proyecto', 'tarea__proyecto__equipo')\
        .distinct().order_by('-created')[0:10]
    tareas = Tarea.objects.filter(Q(proyecto__equipo__integrantes=request.user) |
                                  Q(asignado_a=request.user)).select_related('asignado_a', 'proyecto', 'proyecto__equipo').distinct()
    
    invitaciones_pendientes = Invitacion.objects.filter(
        invitado=request.user,
        aceptada=False
    ).distinct()[:5]
    
    context = {'comentarios': comentarios, 'tareas': tareas, 'invitaciones_pendientes':invitaciones_pendientes}
    return render(request, 'base/home.html', context)


def login_user(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if not hasattr(user, 'perfil'):
                Perfil.objects.create(
                    user = user,
                    email = user.email if user.email else ""
                )

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'El usuario o contraseña no son correctos')

    context = {'page': page}
    return render(request, 'base/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)

        if form.is_valid():
            request.session['numero'] = form.cleaned_data.get('numero')
            request.session['pais'] = form.cleaned_data.get('pais')
            
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = request.POST.get('email')
            user.save()
            login(request, user)
            
            if hasattr(user, 'perfil'):
                user.perfil.numero = request.session.get('numero')
                user.perfil.pais = request.session.get('pais')
                user.perfil.save()
            
            del request.session['numero']
            del request.session['pais']     
                  
            return redirect('home')
        else:
            messages.error(request, "Formulario no valido")

    context = {'form': form}
    return render(request, 'base/login.html', context)


@login_required(login_url='login_user')
def mostrar_profiles(request):
    perfiles = Perfil.objects.all()
    context = {'perfiles':perfiles}
    return render(request, 'base/perfiles.html', context)

@login_required(login_url='login_user')
def profile_user(request, pk):
    user = get_object_or_404(User, id=pk)
    equipos_count = Equipo.objects.filter(Q(integrantes=user) |
                                          Q(jefe=user)).distinct().count()
    tareas_realizadas_count = user.tarea_set.filter(estado='realizada').count()
    perfil = get_object_or_404(Perfil.objects.select_related('user'), user=user)

    context = {'user': user, 'perfil': perfil,
               'equipos_count': equipos_count,
               'tareas_realizadas': tareas_realizadas_count}

    return render(request, 'base/profile_user.html', context)


def actualizar_profile(request, pk):
    perfil = get_object_or_404(Perfil, id=pk)
    form = PerfilForm(instance=perfil)

    if request.user != perfil.user:
        return HttpResponseForbidden("No puedes actualizar un perfil de otro usuario")

    if request.method == 'POST':
        form = PerfilForm(request.POST, request.FILES, instance=perfil)
        if form.is_valid():
            perfil = form.save(commit=False)
            perfil.user.email = perfil.email
            perfil.user.save()
            perfil.save()
            return redirect('profile_user', request.user.id)

    
    context = {'form': form}
    return render(request, 'base/profile_form.html', context)


def equipo_detail(request, pk):
    equipo = get_object_or_404(Equipo, id=pk)

    if request.user not in equipo.integrantes.all():
        return HttpResponseForbidden("No puedes acceder a esta informacion")

    integrantes = equipo.integrantes.all()
    context = {'equipo': equipo, 'integrantes': integrantes}
    return render(request, 'base/equipo_detail.html', context)


@login_required(login_url='login_user')
def equipo_update(request, pk):
    page = 'update'
    equipo = get_object_or_404(Equipo, id=pk)
    form = EquipoForm(instance=equipo)

    if request.user != equipo.jefe:
        return HttpResponseForbidden("No puedes acceder a esta informacion")

    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('equipos')
        else:
            messages.error(request, 'Los datos no son validos')
    
    if not request.user.is_staff:
        form.fields['integrantes'].queryset = User.objects.filter(
            id=request.user.id)
        form.fields['jefe'].queryset = User.objects.filter(id=request.user.id)
        
    context = {'form': form, 'page': page, 'equipo': equipo}
    return render(request, 'base/equipo_form.html', context)


@login_required(login_url='login_user')
def equipo_delete(request, pk):
    equipo = get_object_or_404(Equipo, id=pk)

    if request.user.id is not equipo.jefe.id:
        return HttpResponseForbidden("No puedes acceder a esta informacion")

    if request.method == 'POST':
        equipo.delete()
        return redirect('equipos')

    context = {'equipo': equipo}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login_user')
def create_equipo(request):
    form = EquipoForm()

    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save(commit=False)

            jefe = form.cleaned_data.get('jefe')
            integrantes = form.cleaned_data.get('integrantes', [])

            if request.user not in integrantes and request.user != jefe:
                messages.error(
                    request, 'No puede crear un equipo donde no participe')
                return redirect('create_equipo')

            equipo.save()

            form.save_m2m()

            if jefe not in list(integrantes):
                equipo.integrantes.add(jefe)

            messages.success(request, 'Equipo creado correctamente')
            return redirect('equipos')
        else:
            messages.error(request, 'Los datos son erroneos')

    if not request.user.is_staff:
        form.fields['integrantes'].queryset = User.objects.filter(
            id=request.user.id)
        form.fields['jefe'].queryset = User.objects.filter(id=request.user.id)

    context = {'form': form}
    return render(request, 'base/equipo_form.html', context)


@login_required(login_url='login_user')
def equipos(request):
    if request.user.is_staff:
        equipos = Equipo.objects.all()
    else:
        equipos = Equipo.objects.filter(Q(jefe=request.user) |
                                        Q(integrantes=request.user)).select_related('jefe').distinct()
    context = {'equipos': equipos}
    return render(request, 'base/equipos.html', context)


@login_required(login_url='login_user')
def proyectos(request):
    if request.user.is_staff:
        proyectos = Proyecto.objects.all()
    else:
        proyectos = Proyecto.objects.filter(Q(tutor=request.user) |
                                            Q(equipo__integrantes=request.user)
                                            ).select_related('tutor', 'equipo').distinct()
    context = {'proyectos': proyectos}
    return render(request, 'base/proyectos.html', context)


@login_required(login_url='login_user')
def create_proyecto(request):
    page = 'crear'
    form = ProyectoForm()

    if request.method == 'POST':
        form = ProyectoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('proyectos')
        else:
            messages.error(request, 'Los datos son erroneos')

    if not request.user.is_staff:
        form.fields['equipo'].queryset = Equipo.objects.filter(
            jefe=request.user).select_related('jefe')
        form.fields['tutor'].queryset = User.objects.filter(id=request.user.id)

    context = {'form': form, 'page': page}
    return render(request, 'base/proyecto_form.html', context)


def proyecto_detail(request, pk):
    proyecto = get_object_or_404(Proyecto, id=pk)

    if request.user not in proyecto.equipo.integrantes.all() and request.user != proyecto.tutor:
        return HttpResponseForbidden("No puedes acceder a esta informacion")

    context = {'proyecto': proyecto}
    return render(request, 'base/proyecto_detail.html', context)


@login_required(login_url='login_user')
def proyecto_update(request, pk):
    proyecto = get_object_or_404(Proyecto, id=pk)
    form = ProyectoForm(instance=proyecto)

    if request.user != proyecto.tutor:
        return HttpResponseForbidden("No puedes acceder a esta informacion")

    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('proyectos')
        
    if not request.user.is_staff:
        form.fields['equipo'].queryset = Equipo.objects.filter(
            jefe=request.user).select_related('jefe')
        form.fields['tutor'].queryset = User.objects.filter(id=request.user.id)

    context = {'form': form, 'proyecto': proyecto}
    return render(request, 'base/proyecto_form.html', context)


@login_required(login_url='login_user')
def proyecto_delete(request, pk):
    proyecto = get_object_or_404(Proyecto, id=pk)
    context = {'proyecto': proyecto}

    if request.user != proyecto.tutor:
        return HttpResponseForbidden('No tienes permiso para eliminar el proyecto')

    if request.method == 'POST':
        proyecto.delete()
        return redirect('proyectos')

    return render(request, 'base/delete.html', context)


@login_required(login_url='login_user')
def tareas(request):
    if request.user.is_staff:
        tareas_pendientes = Tarea.objects.filter(estado='pendiente')
        tareas_en_progreso = Tarea.objects.filter(estado='en_progreso')
        tareas_completadas = Tarea.objects.filter(estado='completada')
        tareas_pausadas = Tarea.objects.filter(estado='pausada')

    else:

        tareas_pendientes = Tarea.objects.filter((Q(asignado_a=request.user) |
                                                  Q(proyecto__equipo__integrantes=request.user)) &
                                                 (Q(estado='pendiente') |
                                                 Q(estado='Pendiente'))
                                                 ).select_related('proyecto', 'proyecto__equipo', 'asignado_a', 'proyecto__tutor'
                                                                  ).distinct()
        tareas_completadas = Tarea.objects.filter((Q(asignado_a=request.user) |
                                                   Q(proyecto__equipo__integrantes=request.user)) &
                                                  (Q(estado='completada') |
                                                   Q(estado='Completada'))
                                                  ).select_related('proyecto', 'proyecto__equipo', 'asignado_a', 'proyecto__tutor'
                                                                   ).distinct()

        tareas_en_progreso = Tarea.objects.filter((Q(asignado_a=request.user) |
                                                   Q(proyecto__equipo__integrantes=request.user)) &
                                                  (Q(estado='en_progreso') |
                                                   Q(estado='En_progreso'))
                                                  ).select_related('proyecto', 'proyecto__equipo', 'asignado_a', 'proyecto__tutor'
                                                                   ).distinct()

        tareas_pausadas = Tarea.objects.filter((Q(asignado_a=request.user) |
                                                Q(proyecto__equipo__integrantes=request.user)) &
                                               (Q(estado='pausada') |
                                                Q(estado='Pausada'))
                                               ).select_related('proyecto', 'proyecto__equipo', 'asignado_a', 'proyecto__tutor'
                                                                ).distinct()

    context = {'tareas_pendientes': tareas_pendientes,
               'tareas_completadas': tareas_completadas,
               'tareas_en_progreso': tareas_en_progreso,
               'tareas_pausadas': tareas_pausadas}
    return render(request, 'base/tareas.html', context)


@login_required(login_url='login_user')
def create_tarea(request):
    page = 'crear'
    form = TareaForm()

    if request.method == 'POST':
        form = TareaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tareas')
        else:
            messages.error(request, 'Los datos son erroneos')

    if not request.user.is_staff:
        form.fields['asignado_a'].queryset = User.objects.filter(
            id=request.user.id)
        form.fields['proyecto'].queryset = Proyecto.objects.filter(Q(tutor=request.user) |
                                                                   Q(equipo__integrantes=request.user)
                                                                   ).select_related('tutor', 'equipo').distinct()
    context = {'form': form, 'page': page}
    return render(request, 'base/tarea_form.html', context)


def tarea_detail(request, pk):
    tarea = get_object_or_404(Tarea, id=pk)

    if request.user not in tarea.proyecto.equipo.integrantes.all() and request.user != tarea.asignado_a:
        return HttpResponseForbidden("No puedes acceder a esta informacion")

    context = {'tarea': tarea}
    return render(request, 'base/tarea_detail.html', context)


@login_required(login_url='login_user')
def tarea_update(request, pk):
    tarea = get_object_or_404(Tarea, id=pk)
    form = TareaForm(instance=tarea)

    if request.user != tarea.asignado_a or not request.user.is_staff:
        if request.user != tarea.proyecto.tutor:
            return HttpResponseForbidden('No puedes acceder a esta informacion')

    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('tareas')
        
    if not request.user.is_staff:
        form.fields['asignado_a'].queryset = User.objects.filter(
            id=request.user.id)
        form.fields['proyecto'].queryset = Proyecto.objects.filter(Q(tutor=request.user) |
                                                                   Q(equipo__integrantes=request.user)
                                                                   ).select_related('tutor', 'equipo').distinct()

    context = {'form': form, 'tarea': tarea, 'proyecto': tarea.proyecto}
    return render(request, 'base/proyecto_form.html', context)


@login_required(login_url='login_user')
def tarea_delete(request, pk):
    tarea = get_object_or_404(Tarea, id=pk)

    if request.user != tarea.proyecto.tutor and not request.user.is_staff:
        return HttpResponseForbidden('No puedes acceder a esta informacion')

    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas')

    context = {'tarea': tarea}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login_user')
def comentarios(request):
    if request.user.is_staff:
        comentarios = Comentario.objects.all()
    else:
        comentarios = Comentario.objects.filter(Q(user=request.user) |
                                                Q(tarea__proyecto__equipo__integrantes=request.user)
                                                ).select_related('user', 'tarea', 'tarea__proyecto',
                                                                 'tarea__proyecto__equipo').distinct()
    context = {'comentarios': comentarios}
    return render(request, 'base/comentarios.html', context)


@login_required(login_url='login_user')
def create_comentario(request):
    form = ComentarioForm()
    page = 'crear'

    if request.method == 'POST':
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.user = request.user
            comentario.save()
            return redirect('comentarios')
        else:
            messages.error(request, 'Los datos son erroneos')

    if not request.user.is_staff:
        form.fields['tarea'].queryset = Tarea.objects.filter(Q(asignado_a=request.user) |
                                                             Q(proyecto__equipo__integrantes=request.user)
                                                             ).select_related('asignado_a', 'proyecto', 'proyecto__equipo').distinct()
    context = {'form': form, 'page': page}
    return render(request, 'base/comentario_form.html', context)


@login_required(login_url='login_user')
def comentario_update(request, pk):
    comentario = get_object_or_404(Comentario, id=pk)
    form = ComentarioForm(instance=comentario)

    if request.user != comentario.user:
        return HttpResponseForbidden('No puedes actualizar este comentario')

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('comentarios')
        
    if not request.user.is_staff:
        form.fields['tarea'].queryset = Tarea.objects.filter(Q(asignado_a=request.user) |
                                                             Q(proyecto__equipo__integrantes=request.user)
                                                             ).select_related('asignado_a', 'proyecto', 'proyecto__equipo').distinct()

    context = {'form': form}
    return render(request, 'base/comentario_form.html', context)


@login_required(login_url='login_user')
def comentario_delete(request, pk):
    comentario = get_object_or_404(Comentario, id=pk)

    if request.user != comentario.user:
        return HttpResponseForbidden("No puedes eliminar este comentario")

    if request.method == 'POST':
        comentario.delete()
        return redirect('comentarios')

    context = {'comentario': comentario}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login_user')
def enviar_invitacion(request, pk):
    invitado = get_object_or_404(User, id = pk)
    form = InvitacionForm()
    mis_equipos = Equipo.objects.filter(jefe = request.user).select_related('jefe')
    
    if not mis_equipos.exists():
        messages.error(request, 'No tienes equipos donde seas jefe')
        return redirect('profile_user', pk = pk)
    
    if request.method == 'POST':
        equipo_id = request.POST.get('equipo')
        form = InvitacionForm(request.POST)
        if form.is_valid():
        
            if not equipo_id:
                messages.error(request, 'Debe seleccionar un equipo')
                return redirect('enviar_invitacion', pk = pk)
            
            try:
                equipo = get_object_or_404(Equipo, id = equipo_id, jefe = request.user)
            except Equipo.DoesNotExist:
                messages.error(request, 'Este equipo no existe')
                return redirect('enviar_invitacion', pk = pk)        

            if invitado in equipo.integrantes.all():
                messages.error(request, 'Este usuario ya esta en el equipo')
                return redirect('profile_user', pk = pk)
            
            if request.user != equipo.jefe:
                messages.error(request, 'No eres jefe de este equipo')
                return redirect('profile_user', pk = pk)
                
            invitacion = form.save(commit = False)
            invitacion.invitado = invitado
            invitacion.equipo = equipo 
            invitacion.save()
            accept_url = request.build_absolute_uri(reverse('aceptar_invitacion', kwargs={'token': invitacion.token}))
                
            if invitado.email:
                subject = f'Hola {invitado.username}'
                message =(
                        f'Hola {invitado.username},\n\n'
                        f'Usted ha sido invitado al equipo {equipo.numero} por {request.user.username}.\n\n'
                        f'Si desea aceptar, haga clic en el siguiente enlace:\n'
                        f'{accept_url}\n\n'
                        f'Saludos,\n'
                        f'TaskFlow'
                        )
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [invitado.email], fail_silently=False,)
                    
                messages.success(request, 'Invitacion enviada correctamente')
                return redirect('profile_user', pk = pk)
            
            else:
                messages.warning(request, f'{invitado.username} no tiene email registrado')
        else:
            messages.error(request, 'Formulario no valido')
            
    if not request.user.is_staff:       
        form.fields['equipo'].queryset = Equipo.objects.filter(jefe = request.user)
    context = {'form':form}
    return render(request, 'base/enviar_invitacion.html', context)


def aceptar_invitacion(request, token):
    invitacion = get_object_or_404(Invitacion, token=token, aceptada=False)
    
    if request.user != invitacion.invitado:
        return HttpResponseForbidden("No te corresponde esta invitacion")
    
    if request.method == 'POST':
        invitacion.equipo.integrantes.add(invitacion.invitado)
        invitacion.aceptada = True
        invitacion.save()
        
        messages.success(request, f'Te has unido al equipo {invitacion.equipo.numero} de {invitacion.equipo.jefe.username}')
        return redirect('equipos')
    
    context = {'invitacion':invitacion, 'equipo':invitacion.equipo}
    return render(request, 'base/aceptar_invitacion.html', context)
        