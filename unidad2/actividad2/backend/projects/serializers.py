from rest_framework import serializers
from projects.models import Project_cargues

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project_cargues
        fields = ['id', 'Placa_del_vehiculo', 'Valor_del_cargue', 'Tipo_de_carga', 'Vencimiento_de_soat', 'created_at',]
