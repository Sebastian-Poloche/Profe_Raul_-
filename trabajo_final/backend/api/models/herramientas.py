from django.db import models

# Create your models here.

class lista_categoria(models.TextChoices):
    ENVIAR = "Enviar", "Tipo enviar"
    DEVOLVER = "Devolver", "Tipo devolver"

class Herramientas(models.Model):

    ESTADO_DISPONIBLE = 'Disponible'
    ESTADO_EN_PRESTAMO = 'En préstamo'
    ESTADO_MANTENIMIENTO = 'En mantenimiento'
    ESTADO_INACTIVO = 'Inactivo'
    
    ESTADOS_CHOICES = [
        (ESTADO_DISPONIBLE, 'Disponible'),
        (ESTADO_EN_PRESTAMO, 'En préstamo'),
        (ESTADO_MANTENIMIENTO, 'En mantenimiento'),
        (ESTADO_INACTIVO, 'Inactivo'),
    ]

    codigo = models.CharField(max_length=7, verbose_name = "Codigo")
    nombre = models.CharField(max_length=20, verbose_name = "Nombre")
    categoria = models.CharField(max_length=15, choices = lista_categoria.choices, verbose_name = "Categoria")
    ubicacion = models.CharField(max_length=30, verbose_name = "Ubicación")
    estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES, default=ESTADO_DISPONIBLE)
    
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)