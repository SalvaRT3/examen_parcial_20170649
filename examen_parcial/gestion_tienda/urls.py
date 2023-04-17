from django.urls import path, include
from . import views 

app_name = 'gestion_tienda'

urlpatterns = [
    path('', views.index, name='index'),
    path('cerrarSesion', views.cerrarSesion, name='cerrarSesion'),
    path('gestionUsuarios', views.gestionUsuarios, name='gestionUsuarios'),
    path('eliminarUsuario/<str:ind>', views.eliminarUsuario, name='eliminarUsuario'),
    path('verusuarios/<str:ind>', views.verusuarios, name='verusuarios'),
]