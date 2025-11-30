from rest_framework import serializers
from ..models.prestamos import Prestamos


class PrestamosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamos
        fields = ['id', 'numero', 'herramienta_codigo', 'responsable', 'fecha_salida', 'fecha_esperada', 'fecha_devolucion', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
