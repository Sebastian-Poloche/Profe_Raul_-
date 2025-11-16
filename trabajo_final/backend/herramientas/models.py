from django.db import models

# Create your models here.

class lista_categoria(models.TextChoices):
    ENVIAR = "Enviar", "Tipo enviar"
    DEVOLVER = "Devolver", "Tipo devolver"

class Herramientas(models.Model):
    codigo = models.DecimalField(max_digits=7, decimal_places=0, verbose_name="Codigo")
    nombre = models.CharField(max_length=20, verbose_name="Nombre")
    categoria = models.CharField(max_length=15, choices=lista_categoria.choices, verbose_name="Categoria")
    ubicacion = models.CharField(max_length=30, verbose_name="Ubicación")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)