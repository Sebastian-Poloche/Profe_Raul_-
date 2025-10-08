from rest_framework import serializers
from .models import FirstProject

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirstProject
        fields = ['id', 'Placa_del_vehiculo', 'Valor_del_cargue', 'Tipo_de_carga', 'Vencimiento_de_soat', 'created_at',]
