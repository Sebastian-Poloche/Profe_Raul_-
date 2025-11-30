from rest_framework import serializers
from ..models.herramientas import Herramientas


class HerramientasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Herramientas
        fields = ['id', 'codigo', 'nombre', 'categoria', 'ubicacion', 'estado', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
