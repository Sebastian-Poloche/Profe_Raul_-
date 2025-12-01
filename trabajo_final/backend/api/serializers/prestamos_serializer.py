"""
Serializador para el modelo de Préstamos.

Proporciona validaciones exhaustivas para garantizar que los préstamos
sean consistentes y las herramientas estén disponibles.
"""

from rest_framework import serializers
from ..models.prestamos import Prestamos
from ..models.herramientas import Herramientas
from datetime import date
import re


class PrestamosSerializer(serializers.ModelSerializer):
    """
    Serializador que convierte objetos Préstamos a JSON y valida datos.
    
    Incluye validaciones críticas:
    - Herramienta existe y está disponible
    - Número de préstamo es único
    - Consistencia entre fechas de salida y devolución
    - Campos requeridos sin estar vacíos
    """

    class Meta:
        model = Prestamos
        fields = [
            'id', 'numero', 'herramienta_codigo', 'responsable',
            'fecha_salida', 'fecha_esperada', 'fecha_devolucion',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_numero(self, value):
        """
        Valida que el número de préstamo sea único y con formato requerido.
        
        El número debe ser exactamente 7 caracteres alfanuméricos en mayúsculas.
        Verifica que no exista otro número idéntico en la base de datos.
        
        Args:
            value (str): Número de préstamo a validar
            
        Raises:
            serializers.ValidationError: Si el número es inválido o duplicado
            
        Returns:
            str: Número validado
        """
        if not value or len(value) == 0:
            raise serializers.ValidationError(
                "El número no puede estar vacío"
            )

        if len(value) != 7:
            raise serializers.ValidationError(
                "El número debe tener exactamente 7 caracteres"
            )

        # Validar que sea alfanumérico en mayúsculas
        if not re.match(r'^[A-Z0-9]{7}$', value):
            raise serializers.ValidationError(
                "El número debe contener solo 7 caracteres alfanuméricos en mayúsculas"
            )

        # Verificar unicidad al crear nuevo préstamo
        if not self.instance:
            if Prestamos.objects.filter(numero=value).exists():
                raise serializers.ValidationError(
                    f"Ya existe un préstamo con el número '{value}'"
                )
        else:
            # Al actualizar, permitir el número actual pero no otros iguales
            if Prestamos.objects.filter(numero=value).exclude(
                id=self.instance.id
            ).exists():
                raise serializers.ValidationError(
                    f"Ya existe otro préstamo con el número '{value}'"
                )

        return value

    def validate_responsable(self, value):
        """
        Valida que el responsable no esté vacío después de limpiar espacios.
        
        Elimina espacios en blanco al inicio y final.
        
        Args:
            value (str): Responsable a validar
            
        Raises:
            serializers.ValidationError: Si está vacío
            
        Returns:
            str: Responsable validado y limpio
        """
        if not value or len(value.strip()) == 0:
            raise serializers.ValidationError(
                "El responsable no puede estar vacío"
            )
        return value.strip()

    def validate_fecha_salida(self, value):
        """
        Valida que la fecha de salida esté presente.
        
        La fecha de salida es un campo obligatorio para cualquier préstamo.
        
        Args:
            value: Fecha de salida a validar
            
        Raises:
            serializers.ValidationError: Si no tiene fecha de salida
            
        Returns:
            date: Fecha de salida validada
        """
        if value is None:
            raise serializers.ValidationError(
                "La fecha de salida es requerida"
            )
        return value

    def validate_herramienta_codigo(self, value):
        """
        Valida que la herramienta con ese código exista en el sistema.
        
        Verifica que el código de herramienta sea válido y que la herramienta
        esté registrada en la base de datos.
        
        Args:
            value (str): Código de herramienta a validar
            
        Raises:
            serializers.ValidationError: Si el código no existe
            
        Returns:
            str: Código validado
        """
        if not value:
            raise serializers.ValidationError(
                "El código de herramienta es requerido"
            )

        try:
            Herramientas.objects.get(codigo=value)
        except Herramientas.DoesNotExist:
            raise serializers.ValidationError(
                f"La herramienta con código '{value}' no existe"
            )

        return value

    def validate(self, data):
        """
        Realiza validaciones cruzadas complejas entre múltiples campos.
        
        Verifica que:
        - La herramienta esté disponible para préstamo
        - Las fechas sean coherentes (devolución después de salida)
        - No haya inconsistencias en el registro del préstamo
        
        Args:
            data (dict): Datos completos del préstamo
            
        Raises:
            serializers.ValidationError: Si hay inconsistencias
            
        Returns:
            dict: Datos validados
        """
        codigo_herramienta = data.get('herramienta_codigo')
        fecha_salida = data.get('fecha_salida')
        fecha_esperada = data.get('fecha_esperada')
        fecha_devolucion = data.get('fecha_devolucion')

        # Verificar que la herramienta esté disponible para ser prestada
        if codigo_herramienta:
            try:
                herramienta = Herramientas.objects.get(
                    codigo=codigo_herramienta
                )
                if herramienta.estado != Herramientas.ESTADO_DISPONIBLE:
                    raise serializers.ValidationError(
                        f"La herramienta '{herramienta.nombre}' no está disponible. "
                        f"Estado actual: {herramienta.estado}"
                    )
            except Herramientas.DoesNotExist:
                raise serializers.ValidationError(
                    f"La herramienta con código '{codigo_herramienta}' no existe"
                )

        # Validar consistencia de fechas: esperada no puede ser antes de salida
        if fecha_salida and fecha_esperada:
            if fecha_esperada < fecha_salida:
                raise serializers.ValidationError(
                    "La fecha esperada no puede ser anterior a la fecha de salida"
                )

        # Validar consistencia de fechas: devolución no puede ser antes de salida
        if fecha_devolucion and fecha_salida:
            if fecha_devolucion < fecha_salida:
                raise serializers.ValidationError(
                    "La fecha de devolución no puede ser anterior a la fecha de salida"
                )

        return data
