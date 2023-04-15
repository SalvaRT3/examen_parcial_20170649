from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import datosUsuario

# Create your views here.

def index(request):
    if request.method == 'POST':
        nombreUsuario = request.POST.get('nombreUsuario') 
        contraUsuario = request.POST.get('contraUsuario') 
        usuarioInfo = authenticate(request, username=nombreUsuario, password=contraUsuario)
        if usuarioInfo is not None:
            login(request, usuarioInfo)
            return HttpResponseRedirect(reverse('gestion_tienda:consolaAdministrador'))
        else:
            return HttpResponseRedirect(reverse('gestion_tienda:index')) 
    return render(request, 'login.html')

@login_required(login_url="http://127.0.0.1:8000/")
def consolaAdministrador(request):
    if request.method == 'POST':
        usernameUsuario = request.POST.get('usernameUsuario') 
        contraUsuario = request.POST.get('contraUsuario') 
        nombreUsuario = request.POST.get('nombreUsuario') 
        apellidoUsuario = request.POST.get('apellidoUsuario') 
        rolUsuario = request.POST.get('rolUsuario') 
        nroCelular = request.POST.get('nroCelular') 
        emailUsuario = request.POST.get('emailUsuario') 
        usuarioNuevo = User.objects.create(
            username = usernameUsuario,
            email = emailUsuario,
        )
        usuarioNuevo.set_password(contraUsuario)
        usuarioNuevo.first_name = nombreUsuario
        usuarioNuevo.last_name = apellidoUsuario
        usuarioNuevo.is_staff = True
        usuarioNuevo.save()
        datosUsuario.objects.create(
            user = usuarioNuevo,
            rolUsuario = rolUsuario,
            nroCelular = nroCelular
        )
        return HttpResponseRedirect(reverse('gestion_tienda:consolaAdministrador'))
    return render(request, 'consolaAdministrador.html', {
        'usuariosTotales': User.objects.all().order_by('id')
    })

@login_required(login_url="http://127.0.0.1:8000/")
def cerrarSesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('gestion_tienda:index'))

def usuarios(request):
    return HttpResponse('Ruta de usuarios')

def productos(request):
    return HttpResponse('Ruta de productos')