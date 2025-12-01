"""
Modelos de Herramientas para el sistema IHEP.

Este módulo define la estructura de datos para registrar herramientas en el
inventario, incluyendo categorías, estados y control de auditoría.
"""

from django.db import models


class ListaCategoria(models.TextChoices):
    """
    Clasificación de tipos de herramientas en el sistema.
    
    Define las categorías disponibles que especifican si una herramienta
    es para enviar o recibir en el sistema de préstamos.
    """
    ENVIAR = "Enviar", "Tipo enviar"
    DEVOLVER = "Devolver", "Tipo devolver"


class Herramientas(models.Model):
    """
    Modelo que representa una herramienta en el inventario IHEP.
    
    Almacena toda la información necesaria para gestionar herramientas,
    incluyendo su estado, ubicación y disponibilidad para préstamo.
    """

    # Constantes que definen los estados posibles de una herramienta
    ESTADO_DISPONIBLE = 'Disponible'
    ESTADO_EN_PRESTAMO = 'En préstamo'
    ESTADO_MANTENIMIENTO = 'En mantenimiento'
    ESTADO_INACTIVO = 'Inactivo'

    # Lista de estados válidos que puede tener una herramienta
    ESTADOS_CHOICES = [
        (ESTADO_DISPONIBLE, 'Disponible'),
        (ESTADO_EN_PRESTAMO, 'En préstamo'),
        (ESTADO_MANTENIMIENTO, 'En mantenimiento'),
        (ESTADO_INACTIVO, 'Inactivo'),
    ]

    # Campos del modelo con sus restricciones y validaciones
    codigo = models.CharField(
        max_length=7,
        verbose_name="Código",
        help_text="Código único de 7 caracteres que identifica la herramienta"
    )
    nombre = models.CharField(
        max_length=20,
        verbose_name="Nombre",
        help_text="Nombre descriptivo de la persona solicitante del prestamo"
    )
    categoria = models.CharField(
        max_length=15,
        choices=ListaCategoria.choices,
        verbose_name="Categoría",
        help_text="Clasificación de la herramienta (Enviar/Devolver)"
    )
    ubicacion = models.CharField(
        max_length=30,
        verbose_name="Ubicación",
        help_text="Ubicación física donde se guarda la herramienta"
    )
    estado = models.CharField(
        max_length=50,
        choices=ESTADOS_CHOICES,
        default=ESTADO_DISPONIBLE,
        verbose_name="Estado",
        help_text="Estado actual de la herramienta en el inventario"
    )

    # Campos de auditoría para rastrear cambios en la BD
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de Creación",
        help_text="Fecha y hora en que se creó el registro"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Última Actualización",
        help_text="Fecha y hora del último cambio realizado"
    )

    class Meta:
        """Metadatos del modelo que configura su comportamiento en Django."""
        verbose_name = "Herramienta"
        verbose_name_plural = "Herramientas"
        ordering = ['codigo']

    def __str__(self):
        """Representación en texto del objeto para mejor legibilidad."""
        return f"{self.codigo} - {self.nombre} ({self.estado})"