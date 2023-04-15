from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class datosUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rolUsuario = models.CharField(max_length=32, default='VENDEDOR')
    nroCelular = models.CharField(max_length=32, default='000000000')
    fechaIngreso = models.DateField(default=date.today)

#class datosProducto(models.Model):
#    nameProducto = models.CharField(max_length=32, default='VENDEDOR')
#    user = models.OneToOneField(datosUsuario, on_delete=models.CASCADE)
#    codigo = models.CharField(max_length=32, default='VENDEDOR')
#    precioCompra = models.CharField(max_length=32, default='VENDEDOR')
#    PrecioVenta = models.CharField(max_length=32, default='VENDEDOR')