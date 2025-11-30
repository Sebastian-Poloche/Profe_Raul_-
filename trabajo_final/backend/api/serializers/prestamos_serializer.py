from rest_framework import serializers
from ..models.prestamos import Prestamos
from ..models.herramientas import Herramientas


class PrestamosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prestamos
        fields = ['id', 'numero', 'herramienta_codigo', 'responsable', 'fecha_salida', 'fecha_esperada', 'fecha_devolucion', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        codigo_herramienta = data.get('herramienta_codigo')
        
        try:
            herramienta = Herramientas.objects.get(codigo=codigo_herramienta)
        except Herramientas.DoesNotExist:
            raise serializers.ValidationError(
                f"La herramienta con código '{codigo_herramienta}' no existe."
            )
        
        if herramienta.estado != Herramientas.ESTADO_DISPONIBLE:
            raise serializers.ValidationError(
                f"La herramienta '{herramienta.nombre}' no está disponible. "
                f"Estado actual: {herramienta.estado}"
            )
        
        return data
    
    def validate_numero(self, value):
        if Prestamos.objects.filter(numero=value).exists():
            raise serializers.ValidationError("Este número de préstamo ya existe.")
        return value
    
    def validate_responsable(self, value):
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("El responsable no puede estar vacío.")
        return value.strip()
    
    def validate_fecha_salida(self, value):
        if value is None:
            raise serializers.ValidationError("La fecha de salida es requerida.")
        return value
