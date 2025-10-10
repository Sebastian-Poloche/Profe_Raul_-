from django.db import models
from django.core.validators import RegexValidator

placa_validador = RegexValidator(
        regex=r'^[A-Z]{3}-\d{3}$',
        message='Formato: AAA-123 (3 letras, guión, 3 números)'
    )

# Create your models here.

class TipoCarga(models.TextChoices):
    GENERAL = "General", "Carga general"
    PELIGROSA = "Peligrosa", "Carga peligrosa"
    REFRIGERADA = "Refrigerada", "Carga refrigerada"
    VOLUMINOSA = "Voluminosa", "Carga voluminosa"
    LIQUIDA = "Liquida", "Carga líquida"

class FirstProject(models.Model):
    Placa_del_vehiculo = models.CharField(max_length = 7, validators = [placa_validador], unique = True, verbose_name = "Placa del vehículo")
    Valor_del_cargue = models.DecimalField(max_digits = 10, decimal_places = 2)
    Tipo_de_carga = models.CharField(max_length = 20, choices = TipoCarga.choices, default = TipoCarga.GENERAL, verbose_name = "Tipo de carga")
    Vencimiento_de_soat = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)