from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import datosUsuario, datosProducto

# Create your views here.

def index(request):
    if request.method == 'POST':
        nombreUsuario = request.POST.get('nombreUsuario') 
        contraUsuario = request.POST.get('contraUsuario') 
        usuarioInfo = authenticate(request, username=nombreUsuario, password=contraUsuario)
        if usuarioInfo is not None:
            login(request, usuarioInfo)
            if usuarioInfo.datosusuario.rolUsuario == 'ADMINISTRADOR':
                return HttpResponseRedirect(reverse('gestion_tienda:gestionUsuarios'))
            else:
                return HttpResponseRedirect(reverse('gestion_tienda:gestionProductos'))
        else:
            return HttpResponseRedirect(reverse('gestion_tienda:index')) 
    return render(request, 'login.html')

@login_required(login_url="http://127.0.0.1:8000/")
def cerrarSesion(request):
    logout(request)
    return HttpResponseRedirect(reverse('gestion_tienda:index'))

@login_required(login_url="http://127.0.0.1:8000/")
def gestionUsuarios(request):
    if request.user.datosusuario.rolUsuario == 'ADMINISTRADOR':
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
            return HttpResponseRedirect(reverse('gestion_tienda:gestionUsuarios'))
        return render(request, 'gestionUsuarios.html', {
        'usuariosTotales': User.objects.all().order_by('id')
        })
    else:
        return HttpResponseRedirect(reverse('gestion_tienda:gestionProductos'))


@login_required(login_url="http://127.0.0.1:8000/")
def eliminarUsuario(request, ind):
    usuarioEliminar = User.objects.get(id=ind)
    datosUsuario.objects.get(user=usuarioEliminar).delete()
    usuarioEliminar.delete()
    return HttpResponseRedirect(reverse('gestion_tienda:gestionUsuarios'))

@login_required(login_url="http://127.0.0.1:8000/")
def verusuarios(request, ind):
    usuarioInformacion = User.objects.get(id=ind)
    return render(request, 'InformacionUsuario.html', {
        'usuarioInfo': usuarioInformacion,
    })

@login_required(login_url="http://127.0.0.1:8000/")
def nuevoProducto(request, ind):
    if request.method == 'POST':
        nombreVendedor = User.objects.get(id=ind)
        nombreProducto = request.POST.get('usernameProducto') 
        codProducto = request.POST.get('codProducto') 
        PcompraProducto = request.POST.get('preciocompraProducto') 
        PventaProducto = request.POST.get('precioventaProducto') 
        stockdelproducto = request.POST.get('stockProducto') 
        datosProducto.objects.create(
            vendedor = nombreVendedor,
            nameProducto = nombreProducto,
            codigo = codProducto,
            precioCompra = PcompraProducto,
            PrecioVenta = PventaProducto,
            stockProducto = stockdelproducto,
        )
        return HttpResponseRedirect(reverse('gestion_tienda:gestionProductos'))

@login_required(login_url="http://127.0.0.1:8000/")
def gestionProductos(request):
    return render(request, 'gestionProductos.html', {
        'productosTotales': datosProducto.objects.all().order_by('id')
    })

@login_required(login_url="http://127.0.0.1:8000/")
def eliminarProducto(request, ind):
    productoEliminar = datosProducto.objects.get(id=ind).delete()
    return HttpResponseRedirect(reverse('gestion_tienda:gestionProductos'))