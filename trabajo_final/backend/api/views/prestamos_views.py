"""
Vistas (ViewSets) para gestionar operaciones CRUD de Préstamos.

Este módulo define los endpoints REST para crear, leer, actualizar y eliminar
registros de préstamos en el sistema IHEP.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.prestamos import Prestamos
from ..serializers.prestamos_serializer import PrestamosSerializer


class PrestamosViewSet(viewsets.ModelViewSet):
    """
    ViewSet que proporciona operaciones CRUD completas para Préstamos.
    
    Permite listar, crear, actualizar y eliminar préstamos a través de
    endpoints REST automáticamente generados por Django REST Framework.
    """
    
    queryset = Prestamos.objects.all()
    serializer_class = PrestamosSerializer

    def list(self, request, *args, **kwargs):
        """
        Obtiene la lista completa de préstamos sin paginación.
        
        GET /api/prestamos/
        
        Returns:
            Response: Lista de todos los préstamos en formato JSON
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Crea un nuevo préstamo en el sistema.
        
        POST /api/prestamos/
        
        Valida los datos recibidos incluyendo disponibilidad de herramienta
        y crea un nuevo registro si la información es válida.
        
        Args:
            request: Petición HTTP con datos del préstamo
            
        Returns:
            Response: Datos del préstamo creado con status 201
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Actualiza completamente un préstamo existente (PUT).
        
        PUT /api/prestamos/{id}/
        
        Valida los datos y actualiza todos los campos del préstamo.
        Requiere que se envíen todos los campos obligatorios.
        
        Args:
            request: Petición HTTP con datos actualizados
            
        Returns:
            Response: Datos actualizados del préstamo
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance,
            data=request.data,
            partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Elimina un préstamo del sistema.
        
        DELETE /api/prestamos/{id}/
        
        Elimina permanentemente un préstamo de la base de datos.
        
        Args:
            request: Petición HTTP de eliminación
            
        Returns:
            Response: Confirmación de eliminación con status 204
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
