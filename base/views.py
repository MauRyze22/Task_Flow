from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import EquipoForm, ProyectoForm, TareaForm, ComentarioForm, RegisterForm, PerfilForm
from .models import Equipo, Tarea, Proyecto, Comentario, Perfil
from django.contrib.auth.models import User 
from django.db.models import Q

# Create your views here.


@login_required(login_url='login_user')
def home(request):
    comentarios = Comentario.objects.filter(Q(user=request.user) |
                                            Q(tarea__proyecto__equipo__integrantes=request.user)).distinct().order_by('-created')[0:10]
    tareas = Tarea.objects.filter(Q(proyecto__equipo__integrantes=request.user) |
                                  Q(asignado_a=request.user)).distinct()
    context = {'comentarios': comentarios, 'tareas': tareas}
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

            try:
                perfil = Perfil.objects.get(user=user)
            except Perfil.DoesNotExist:
                perfil = Perfil.objects.create(user=user)

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Hay datos erroneos')

    context = {'page': page}
    return render(request, 'base/login.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def register_user(request):
    form = RegisterForm()

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        perfil_form = PerfilForm(request.POST)
        if form.is_valid() and perfil_form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Formulario no valido")

    context = {'form': form}
    return render(request, 'base/login.html', context)


@login_required(login_url='profile_user')
def profile_user(request, pk):
    user = get_object_or_404(User, id=pk)
        
    if request.user != user:
        return HttpResponseForbidden(request, 'No puedes acceder a un perfil de otro usuario')

    equipos_count = Equipo.objects.filter(Q(integrantes=request.user)|
                                          Q(jefe = request.user)).distinct().count()
    tareas_realizadas_count = user.tarea_set.filter(estado='realizada').count()
    perfil = Perfil.objects.get(user=user)
        
    context = {'user': user, 'perfil': perfil,
               'equipos_count': equipos_count,
               'tareas_realizadas': tareas_realizadas_count}
        
    return render(request, 'base/profile_user.html', context)


def actualizar_profile(request, pk):  
    perfil = get_object_or_404(Perfil, id=pk)
    if request.user != perfil.user:
        return HttpResponseForbidden("No puedes actualizar un perfil de otro usuario")  
    
    form = PerfilForm(instance = perfil)
        
    if request.method == 'POST':
        form = PerfilForm(request.POST, instance = perfil)
        if form.is_valid():
            form.save()
            return redirect('profile_user', request.user.id)

    context = {'form':form}        
    return render(request, 'base/profile_form.html', context)


def equipo_detail(request, pk):
    equipo = get_object_or_404(Equipo, id = pk)
    
    if request.user not in equipo.integrantes.all():
        return HttpResponseForbidden("No puedes acceder a esta informacion")
    
    integrantes = equipo.integrantes.all()
    context = {'equipo': equipo, 'integrantes': integrantes}
    return render(request, 'base/equipo_detail.html', context)


@login_required(login_url='login_user')
def equipo_update(request, pk):
    page = 'update'
    equipo = get_object_or_404(Equipo, id = pk)
    form = EquipoForm(instance=equipo)
    
    if request.user not in equipo.integrantes.all():
        return HttpResponseForbidden("No puedes acceder a esta informacion")

    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo)
        if form.is_valid():
            form.save()
            return redirect('equipos')
        else:
            messages.error(request, 'Los datos no son validos')

    context = {'form': form, 'page': page}
    return render(request, 'base/equipo_form.html', context)


@login_required(login_url='login_user')
def equipo_delete(request, pk):
    equipo = get_object_or_404(Equipo, id = pk)

    if request.user not in equipo.integrantes.all():
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
            equipo = form.save(commit = False)

            jefe = form.cleaned_data.get('jefe')
            integrantes = form.cleaned_data.get('integrantes', [])
            
            if request.user not in list(integrantes) and request.user != jefe:
                messages.error(request, 'No puede crear un equipo donde no participe')
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
        form.fields['integrantes'].queryset = User.objects.filter(id = request.user.id)
        form.fields['jefe'].queryset = User.objects.filter(id = request.user.id)
        
    context = {'form': form}
    return render(request, 'base/equipo_form.html', context)


@login_required(login_url='login_user')
def equipos(request):
    equipos = Equipo.objects.filter(Q(jefe=request.user) |
                                    Q(integrantes=request.user)).distinct()
    context = {'equipos': equipos}
    return render(request, 'base/equipos.html', context)


@login_required(login_url='login_user')
def proyectos(request):
    proyectos = Proyecto.objects.filter(Q(tutor=request.user) |
                                        Q(equipo__integrantes=request.user)).distinct()
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
        form.fields['equipo'].queryset = Equipo.objects.filter(integrantes = request.user)
        form.fields['tutor'].queryset = User.objects.filter(id = request.user.id)
        
    context = {'form': form, 'page': page}
    return render(request, 'base/proyecto_form.html', context)

3
def proyecto_detail(request, pk):
    proyecto = get_object_or_404(Proyecto, id = pk)
    
    if request.user not in proyecto.equipo.integrantes.all() or request.user != proyecto.tutor:
        return HttpResponseForbidden("No puedes acceder a esta informacion")
    
    context = {'proyecto': proyecto}
    return render(request, 'base/proyecto_detail.html', context)


@login_required(login_url='login_user')
def proyecto_update(request, pk):
    proyecto = get_object_or_404(Proyecto , id = pk)
    form = ProyectoForm(instance=proyecto)
    
    if request.user != proyecto.tutor:
        return HttpResponseForbidden("No puedes acceder a esta informacion")

    if request.method == 'POST':
        form = ProyectoForm(request.POST, instance=proyecto)
        if form.is_valid():
            form.save()
            return redirect('proyectos')

    context = {'form': form}
    return render(request, 'base/proyecto_form.html', context)


@login_required(login_url='login_user')
def proyecto_delete(request, pk):
    proyecto = get_object_or_404(Proyecto, id = pk)
    context = {'proyecto': proyecto}

    if request.user != proyecto.tutor:
        return HttpResponseForbidden('No tienes permiso para eliminar el proyecto')
    
    if request.method == 'POST':
        proyecto.delete()
        return redirect('proyectos')

    return render(request, 'base/delete.html', context)


@login_required(login_url='login_user')
def tareas(request):
    tareas_pendientes = Tarea.objects.filter((Q(asignado_a=request.user) |
                                             Q(proyecto__equipo__integrantes=request.user)) &
                                             (Q(estado='pendiente') |
                                             Q(estado='Pendiente'))).distinct()
    tareas_completadas = Tarea.objects.filter((Q(asignado_a=request.user) |
                                              Q(proyecto__equipo__integrantes=request.user)) &
                                              (Q(estado='completada') |
                                              Q(estado='Completada'))).distinct()

    tareas_en_progreso = Tarea.objects.filter((Q(asignado_a=request.user) |
                                              Q(proyecto__equipo__integrantes=request.user)) &
                                              (Q(estado='en_progreso') |
                                              Q(estado='En_progreso'))).distinct()

    tareas_pausadas = Tarea.objects.filter((Q(asignado_a=request.user) |
                                           Q(proyecto__equipo__integrantes=request.user)) &
                                           (Q(estado='pausada') |
                                           Q(estado='Pausada'))).distinct()

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
        form.fields['asignado_a'].queryset = User.objects.filter(id = request.user.id)
        
    form.fields['proyecto'].queryset = Proyecto.objects.filter(Q(tutor = request.user)|
                                                         Q(equipo__integrantes = request.user)).distinct()
    context = {'form': form, 'page': page}
    return render(request, 'base/tarea_form.html', context)


def tarea_detail(request, pk):
    tarea = get_object_or_404(Tarea, id = pk)
    
    if request.user not in tarea.proyecto.equipo.integrantes.all() or request.user != tarea.asignado_a:
        return HttpResponseForbidden("No puedes acceder a esta informacion")
    
    context = {'tarea': tarea}
    return render(request, 'base/tarea_detail.html', context)


@login_required(login_url='login_user')
def tarea_update(request, pk):
    tarea = get_object_or_404(Tarea, id = pk)
    form = TareaForm(instance=tarea)
    
    if request.user != tarea.asignado_a or not request.user.is_staff:
        if request.user != tarea.proyecto.tutor:
            return HttpResponseForbidden('No puedes acceder a esta informacion')

    if request.method == 'POST':
        form = TareaForm(request.POST, instance=tarea)
        if form.is_valid():
            form.save()
            return redirect('tareas')

    context = {'form': form}
    return render(request, 'base/proyecto_form.html', context)


@login_required(login_url='login_user')
def tarea_delete(request, pk):
    tarea = get_object_or_404(Tarea, id = pk)
    
    if request.user != tarea.proyecto.tutor or not request.user.is_staff:
        return HttpResponseForbidden('No puedes acceder a esta informacion')

    if request.method == 'POST':
        tarea.delete()
        return redirect('tareas')

    context = {'tarea': tarea}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login_user')
def comentarios(request):
    comentarios = Comentario.objects.filter(Q(user=request.user) |
                                            Q(tarea__proyecto__equipo__integrantes=request.user)).distinct()
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
        form.fields['tarea'].queryset = Tarea.objects.filter(Q(asignado_a = request.user)|
                                                         Q(proyecto__equipo__integrantes = request.user)).distinct()
    context = {'form': form, 'page': page}
    return render(request, 'base/comentario_form.html', context)


@login_required(login_url='login_user')
def comentario_update(request, pk):
    comentario = get_object_or_404(Comentario, id= pk)
    form = ComentarioForm(instance=comentario)

    if request.user != comentario.user:
        return HttpResponseForbidden('No puedes actualizar este comentario')

    if request.method == 'POST':
        form = ComentarioForm(request.POST, instance=comentario)
        if form.is_valid():
            form.save()
            return redirect('comentarios')

    context = {'form': form}
    return render(request, 'base/comentario_form.html', context)


@login_required(login_url='login_user')
def comentario_delete(request, pk):
    comentario = get_object_or_404(Comentario, id= pk)
    
    if request.user != comentario.user:
        return HttpResponseForbidden("No puedes eliminar este comentario")

    if request.method == 'POST':
        comentario.delete()
        return redirect('comentarios')

    context = {'comentario': comentario}
    return render(request, 'base/delete.html', context)
