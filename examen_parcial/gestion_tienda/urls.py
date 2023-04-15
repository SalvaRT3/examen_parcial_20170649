from django.urls import path, include
from . import views 

app_name = 'gestion_tienda'

urlpatterns = [
    path('', views.index, name='index'),
    path('consolaAdministrador', views.consolaAdministrador, name='consolaAdministrador'),
    path('cerrarSesion', views.cerrarSesion, name='cerrarSesion'),
    path('gestion-usuarios', views.usuarios, name='usuarios'),
    path('gestion-productos', views.productos, name='productos'),
]