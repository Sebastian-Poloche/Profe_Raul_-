from django.contrib import admin
from .models.herramientas import Herramientas
from .models.prestamos import Prestamos

# Register your models here.

admin.site.register(Herramientas)
admin.site.register(Prestamos)