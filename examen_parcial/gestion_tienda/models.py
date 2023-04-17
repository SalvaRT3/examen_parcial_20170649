from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class datosUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rolUsuario = models.CharField(max_length=32, default='VENDEDOR')
    nroCelular = models.CharField(max_length=32, default='000000000')
    fechaIngreso = models.DateField(default=date.today)

class datosProducto(models.Model):
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE)
    nameProducto = models.CharField(max_length=32, default='000000000')
    codigo = models.CharField(max_length=32, default='000000000')
    precioCompra = models.CharField(max_length=32, default='0')
    PrecioVenta = models.CharField(max_length=32, default='0')
    stockProducto = models.CharField(max_length=32, default='0')
    fechaventa = models.DateField(default=date.today)