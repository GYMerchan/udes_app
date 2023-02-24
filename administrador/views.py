from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import  AuthenticationForm
from .models import Sitio, Reserva
from .forms import SitioForm, ReservaForm
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404

# Create your views here.
def home(request):
    return render(request, 'app/home.html')

def genesis(request):
    return render(request, 'app/genesis/genesis.html')

def galileo(request):
    return render(request, 'app/galileo/galileo.html')

@login_required
def genesis_home(request):
    context = {'is_estudiante': request.user.groups.filter(name='Estudiante').exists()}
    return render(request, 'app/genesis/genesis_home.html', context)

def sign_in(request):
    if request.method == 'GET':
        return render(request, 'registration/sign_in.html', {
        'form': AuthenticationForm
        })
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])

        if user is None:
          return render(request, 'registration/sign_in.html', {
            'form': AuthenticationForm,
            'error': 'Usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('genesis_home')

@login_required
def galileo_home(request):
    context = {'is_usuario_control': request.user.groups.filter(name='Usuario_Control').exists(),
               'is_estudiante': request.user.groups.filter(name='Estudiante').exists()}
    return render(request, 'app/galileo/galileo_home.html', context)

@login_required
def crear_sitio(request):
    data = {
        'form' : SitioForm()
    }

    if request.method == 'POST':
        formulario = SitioForm(data=request.POST)#files=request.FILES por si en algún momento envían archivos
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Creado Correctamente')#envío un alert bonito
            data["mensaje"] = 'Creado con exito'
        else:
            data['form'] = formulario

            #return redirect('galileo_home')

    return render(request, 'app/galileo/crear_sitio.html', data)

@login_required
def leer_sitio(request):
    context = {'is_usuario_control': request.user.groups.filter(name='Usuario_Control').exists(),
               'is_estudiante': request.user.groups.filter(name='Estudiante').exists()}

    sitios = Sitio.objects.all()
    page = request.GET.get('page',1)

    try:
        paginator = Paginator(sitios, 10)#con esta el linea el men ponía un pagindor de a 10 items 
        sitios = paginator.page(page)
    except:
        raise Http404#acá para cuando no había ningún registro no se cayera,https://www.youtube.com/watch?v=g-76pNgPFl8&list=PL3XiwX4b6ls0Ye0IkKgZpxzXh3EGe_TOJ&index=12 

    data = {
        'sitios': sitios,
    }
    data.update(context)

    return render(request, 'app/galileo/leer_sitio.html', data)

@login_required
def editar_sitio(request, id):

    sitio = get_object_or_404(Sitio, id=id)#get_object_or_404 busca un elemento(modelo, condición)
    data = {
        'form' : SitioForm(instance=sitio)#creo el form pero con datos, instancia igual al sitio de la db
    }
    if request.method == 'POST':
        formulario = SitioForm(data=request.POST, instance=sitio, files=request.FILES)#para que pueda guardar necesito pasarle la instancia
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Editado Correctamente')#envío un alert bonito
            return redirect('leer_sitio')#redirecciono al listado
        data['form'] = formulario#si hay algun problema envío el form con los datos de la validacion

    return render(request, 'app/galileo/editar_sitio.html', data)#instance rellena el formulario ahora

@login_required
def eliminar_sitio(request, id):

    sitio = get_object_or_404(Sitio, id=id)
    sitio.delete()
    messages.error(request,'Eliminado Correctamente')

    return redirect('leer_sitio')

@login_required
def crear_reserva(request):
    data = {
        'form' : ReservaForm()
    }
    if request.method == 'POST':
        formulario = ReservaForm(data=request.POST)#files=request.FILES por si en algún momento envían archivos
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Creado Correctamente')#envío un alert bonito
            data["mensaje"] = 'Creado con exito'
        else:
            data['form'] = formulario
    return render(request, 'app/genesis/crear_reserva.html', data)

'''
def crear_reserva(request):#esto es otra forma de hacerlo pero me enrede, guardar no borrar para futuras ocasiones
    data = {
        'form' : ReservaForm()
    }
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            usuario = form.cleaned_data['usuario']
            sitio = form.cleaned_data['sitio']
            fecha_reserva = form.cleaned_data['fecha']
            hora_inicio = form.cleaned_data['hora_inicio']
            hora_fin = form.cleaned_data['hora_fin']
            estado_reserva = 'por hacer'

            reserva = Reserva(usuario=usuario, sitio=sitio, fecha_reserva=fecha_reserva,
                              hora_inicio=hora_inicio, hora_fin=hora_fin, estado_reserva=estado_reserva)
            reserva.save()
    return render(request, 'app/genesis/crear_reserva.html', data)
'''

@login_required
def leer_reserva(request):
    reservas = Reserva.objects.all()
    is_estudiante = request.user.groups.filter(name='Estudiante').exists()
    context = {'is_estudiante': is_estudiante}
    data = {
        'reservas': reservas,
        **context,  # agregamos el diccionario context al diccionario data
    }
    return render(request, 'app/genesis/leer_reserva.html', data)

@login_required
def editar_reserva(request, id):
    context = {'is_estudiante': request.user.groups.filter(name='Estudiante').exists()}

    reserva = get_object_or_404(Reserva, id=id)#get_object_or_404 busca un elemento(modelo, condición)

    data = {
        'form' : ReservaForm(instance=reserva)#creo el form pero con datos, instancia igual al reserva de la db
    }
    data.update(context)
    if request.method == 'POST':
        formulario = ReservaForm(data=request.POST, instance=reserva, files=request.FILES)#para que pueda guardar necesito pasarle la instancia
        if formulario.is_valid():
            formulario.save()
            messages.success(request,'Editado Correctamente')#envío un alert bonito
            return redirect('leer_reserva')#redirecciono al listado
        data['form'] = formulario#si hay algun problema envío el form con los datos de la validacion

    return render(request, 'app/genesis/editar_reserva.html', data)#instance rellena el formulario ahora    

@login_required
def eliminar_reserva(request, id):
    reserva = get_object_or_404(Reserva, id=id)
    reserva.delete()
    messages.error(request,'Eliminado Correctamente')
    return redirect('leer_reserva')

@login_required
def lista_control(request):
    grupo = Group.objects.get(name='Usuario_Control')
    usuarios = grupo.user_set.all()
    context = {
        'usuarios' : usuarios
    }
    return render(request, 'app/galileo/control_ingreso/lista_control.html', context)

def in_allowed_groups(user):
    return user.groups.filter(name__in=['Estudiante', 'Usuario_Control']).exists()

@login_required
@user_passes_test(lambda u: u.groups.filter(name__in=['Estudiante', 'Usuario_Control']).exists())
def my_view(request):
    if request.user.groups.filter(name='Estudiante').exists():
        grupo = 'Sólo para estudiantes'
    else:
        grupo = 'Para usuarios control y otros grupos'

    data = {
        'grupo': grupo
    }

    return render(request, 'app/genesis/leer_reserva.html', data)

@login_required
def cancelar_reserva(request, reserva_id, sitio_id):
    # Sitio y Reserva correspondiente a los id foraneos
    sitio = get_object_or_404(Sitio, id=sitio_id)
    reserva = get_object_or_404(Reserva, id=reserva_id, sitio=sitio)
    # miro si tiene el permiso para hacerlo
    if not reserva.puede_cancelar_reserva(request.user):
        messages.error(request, "No tienes permiso para cancelar esta reserva.")
        return redirect('app/genesis/leer_reserva.html')
  






