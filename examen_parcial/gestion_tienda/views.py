from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, FileResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import datosUsuario, datosProducto
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

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

@login_required(login_url="http://127.0.0.1:8000/")
def descargarReporteUsuarios(request, idUsuario):
    """
    PREGUNTA 1
    En esta funcion debe generar un pdf con utilizando la libreria reportlab
    Este reporte debe contener la informacion de todos los usuarios a excepcion
    de la contraseña y debe mostrar tambien la cantidad de tareas de cada 
    usuarios (Solo la cantidad no es necesario la descripcion de todas)
    Usuarios Nombre Apellido
    Username        Fecha de ingreso       Numero de celular
    Cantidad de tareas              Tipo de usuario
    Agregar una descripcion de cabecera de la siguiente forma
    Logo de DJANGO      Titulo: Reporte de usuarios     Logo de PUCP
    Fecha de creacion del reporte
    Cantidad de usuarios
    Usuario que genera el reporte
    Tipo de usuarios que genera el reporte
    
    """
    nombreArchivo = 'reporteUsuarios.pdf'
    usuarioInformacion = User.objects.get(id=idUsuario) 
    Usuarios_inscritos = User.objects.all().order_by('datosusuario')
    archivoPdf = canvas.Canvas(nombreArchivo,A4)

    archivoPdf.drawImage('./gestion_tienda/static/abarrotes.png',20, 700, width=140, height=80)
    archivoPdf.drawImage('./gestion_tienda/static/pucp_logo.png',430, 700, width=140, height=80)
    
    archivoPdf.setFont('Helvetica-Bold',25)
    archivoPdf.drawCentredString(297.5,730,'Reporte de Usuarios')

    #Informacion del usuario
    archivoPdf.setFont('Helvetica-Bold',12)
    archivoPdf.drawString(40,660, 'Nombre de usuario')
    archivoPdf.drawString(40,645, 'Nombres')
    archivoPdf.drawString(40,630, 'Apellidos')
    archivoPdf.drawString(40,615, 'Email')

    archivoPdf.drawString(155,660, ':')
    archivoPdf.drawString(155,645, ':')
    archivoPdf.drawString(155,630, ':')
    archivoPdf.drawString(155,615, ':')

    archivoPdf.setFont('Helvetica',12)
    archivoPdf.drawString(160,660, f'{usuarioInformacion.username}')
    archivoPdf.drawString(160,645, f'{usuarioInformacion.first_name}')
    archivoPdf.drawString(160,630, f'{usuarioInformacion.last_name}')
    archivoPdf.drawString(160,615, f'{usuarioInformacion.email}')

    lista_x = [30,550]
    lista_y = [420,560]
    archivoPdf.setStrokeColorRGB(0,0,1)

    for Usuario in Usuarios_inscritos:
        archivoPdf.grid(lista_x, lista_y)
        archivoPdf.setFont('Helvetica-Bold',12)
        archivoPdf.drawString(lista_x[0] + 20, lista_y[1]-25, 'Nombre usuario:')
        archivoPdf.drawString(lista_x[0] + 20, lista_y[1]-55, 'Nombres:')
        archivoPdf.drawString(lista_x[0] + 20, lista_y[1]-85, 'Apellidos:')
        archivoPdf.drawString(lista_x[0] + 20, lista_y[1]-115, 'Rol:')
        archivoPdf.setFont('Helvetica',12)
        archivoPdf.drawString(lista_x[0] + 120, lista_y[1]-25, f'{Usuario.username}')
        archivoPdf.drawString(lista_x[0] + 120, lista_y[1]-55, f'{Usuario.first_name}')
        archivoPdf.drawString(lista_x[0] + 120, lista_y[1]-85, f'{Usuario.last_name}')
        archivoPdf.drawString(lista_x[0] + 120, lista_y[1]-115, f'{Usuario.datosusuario.rolUsuario}')
        archivoPdf.setFont('Helvetica-Bold',12)
        archivoPdf.drawString(lista_x[0] + 280, lista_y[1]-55, 'Celular:')
        archivoPdf.drawString(lista_x[0] + 280, lista_y[1]-85, 'Fecha Ingreso:')
        archivoPdf.drawString(lista_x[0] + 280, lista_y[1]-115, 'Email:')
        archivoPdf.setFont('Helvetica',12)
        archivoPdf.drawString(lista_x[0] + 380, lista_y[1]-55, f'{Usuario.datosusuario.nroCelular}')
        archivoPdf.drawString(lista_x[0] + 380, lista_y[1]-85, f'{Usuario.datosusuario.fechaIngreso}')
        archivoPdf.drawString(lista_x[0] + 380, lista_y[1]-115, f'{Usuario.email}')

        lista_y[0] = lista_y[0] - 140
        lista_y[1] = lista_y[1] - 140

    archivoPdf.save()
    reporteUsuarios=open(nombreArchivo,'rb')
    return FileResponse(reporteUsuarios,as_attachment=True)