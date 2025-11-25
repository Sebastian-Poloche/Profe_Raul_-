from django.db import models

# Create your models here.

class Prestamos(models.Model):
    numero = models.CharField(max_length=7, verbose_name = "Número")
    herramienta_codigo = models.CharField(max_length=20, verbose_name = "Codigo de herramientas")
    responsable = models.CharField(max_length=15, verbose_name = "Responsable")
    fecha_salida = models.DateField(null=True, blank=True, verbose_name="Fecha de Salida")
    fecha_esperada = models.DateField(null=True, blank=True, verbose_name="Fecha Esperada")
    fecha_devolucion = models.DateField(null=True, blank=True, verbose_name="Fecha de Devolución")

    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)