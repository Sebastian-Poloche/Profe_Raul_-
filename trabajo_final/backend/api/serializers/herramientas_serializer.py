"""
Serializador para el modelo de Herramientas.

Proporciona validaciones exhaustivas para garantizar la integridad de los datos
al crear y actualizar herramientas en la base de datos.
"""

from rest_framework import serializers
from ..models.herramientas import Herramientas
import re


class HerramientasSerializer(serializers.ModelSerializer):
    """
    Serializador que convierte objetos Herramientas a JSON y valida datos.
    
    Incluye validaciones de integridad:
    - Código único y con formato requerido
    - Campos requeridos sin estar vacíos
    - Restricciones de longitud según especificaciones
    - Validaciones cruzadas entre campos
    """

    class Meta:
        model = Herramientas
        fields = [
            'id', 'codigo', 'nombre', 'categoria', 'ubicacion',
            'estado', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_codigo(self, value):
        """
        Valida que el código sea único y tenga el formato requerido.
        
        El código debe ser exactamente 7 caracteres alfanuméricos en mayúsculas.
        Verifica que no exista otro código idéntico en la base de datos.
        
        Args:
            value (str): Código a validar
            
        Raises:
            serializers.ValidationError: Si el código es inválido o duplicado
            
        Returns:
            str: Código validado
        """
        if not value or len(value) == 0:
            raise serializers.ValidationError("El código no puede estar vacío")

        if len(value) != 7:
            raise serializers.ValidationError(
                "El código debe tener exactamente 7 caracteres"
            )

        # Validar que contenga solo caracteres alfanuméricos en mayúsculas
        if not re.match(r'^[A-Z0-9]{7}$', value):
            raise serializers.ValidationError(
                "El código debe contener solo 7 caracteres alfanuméricos en mayúsculas"
            )

        # Verificar que el código sea único al crear una nueva herramienta
        if not self.instance:
            if Herramientas.objects.filter(codigo=value).exists():
                raise serializers.ValidationError(
                    f"Ya existe una herramienta con el código '{value}'"
                )
        else:
            # Al actualizar, permitir el código actual pero no otros iguales
            if Herramientas.objects.filter(codigo=value).exclude(
                id=self.instance.id
            ).exists():
                raise serializers.ValidationError(
                    f"Ya existe otra herramienta con el código '{value}'"
                )

        return value

    def validate_nombre(self, value):
        """
        Valida que el nombre no esté vacío después de limpiar espacios.
        
        Elimina espacios en blanco al inicio y final del nombre.
        
        Args:
            value (str): Nombre a validar
            
        Raises:
            serializers.ValidationError: Si el nombre está vacío
            
        Returns:
            str: Nombre validado y limpio
        """
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("El nombre no puede estar vacío")
        return value.strip()

    def validate_ubicacion(self, value):
        """
        Valida que la ubicación no esté vacía después de limpiar espacios.
        
        Elimina espacios en blanco al inicio y final de la ubicación.
        
        Args:
            value (str): Ubicación a validar
            
        Raises:
            serializers.ValidationError: Si la ubicación está vacía
            
        Returns:
            str: Ubicación validada y limpia
        """
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError("La ubicación no puede estar vacía")
        return value.strip()

    def validate(self, data):
        """
        Realiza validaciones cruzadas entre múltiples campos.
        
        Verifica que campos importantes estén presentes y sean válidos.
        
        Args:
            data (dict): Datos completos de la herramienta
            
        Raises:
            serializers.ValidationError: Si hay inconsistencias entre campos
            
        Returns:
            dict: Datos validados
        """
        if not data.get('categoria'):
            raise serializers.ValidationError(
                {"categoria": "La categoría es requerida"}
            )
        if not data.get('estado'):
            raise serializers.ValidationError(
                {"estado": "El estado es requerido"}
            )
        return data
