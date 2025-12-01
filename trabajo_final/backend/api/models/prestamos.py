"""
Modelos de Préstamos para el sistema IHEP.

Este módulo define la estructura de datos para registrar préstamos de herramientas,
incluyendo fechas de salida, devolución esperada y control de auditoría.
"""

from django.db import models


class Prestamos(models.Model):
    """
    Modelo que representa un préstamo de herramienta en el sistema IHEP.
    
    Almacena información sobre préstamos realizados, incluyendo identificación
    de la herramienta, responsable del préstamo y fechas de control.
    """

    # Campos del modelo que registran la información del préstamo
    numero = models.CharField(
        max_length=7,
        verbose_name="Número",
        help_text="Número único de 7 caracteres que identifica el préstamo"
    )
    herramienta_codigo = models.CharField(
        max_length=20,
        verbose_name="Código de Herramienta",
        help_text="Referencia al código de la herramienta prestada"
    )
    responsable = models.CharField(
        max_length=15,
        verbose_name="Responsable",
        help_text="Persona responsable de la herramienta durante el préstamo"
    )
    
    # Fechas importantes del préstamo para control y seguimiento
    fecha_salida = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Salida",
        help_text="Fecha en que la herramienta sale del inventario"
    )
    fecha_esperada = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha Esperada de Devolución",
        help_text="Fecha planificada para la devolución de la herramienta"
    )
    fecha_devolucion = models.DateField(
        null=True,
        blank=True,
        verbose_name="Fecha de Devolución",
        help_text="Fecha real en que se devolvió la herramienta"
    )

    # Campos de auditoría para rastrear cambios en la base de datos
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        help_text="Fecha y hora en que se creó el registro del préstamo"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización",
        help_text="Fecha y hora del último cambio realizado"
    )

    class Meta:
        """Metadatos del modelo que configura su comportamiento en Django."""
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['-fecha_salida']

    def __str__(self):
        """Representación en texto del objeto para mejor legibilidad."""
        return f"Préstamo {self.numero} - {self.herramienta_codigo} ({self.responsable})"