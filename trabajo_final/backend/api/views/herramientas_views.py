"""
Vistas (ViewSets) para gestionar operaciones CRUD de Herramientas.

Este módulo define los endpoints REST para crear, leer, actualizar y eliminar
herramientas en el sistema IHEP.
"""

from rest_framework import viewsets, status
from rest_framework.response import Response
from ..models.herramientas import Herramientas
from ..serializers.herramientas_serializer import HerramientasSerializer


class HerramientasViewSet(viewsets.ModelViewSet):
    """
    ViewSet que proporciona operaciones CRUD completas para Herramientas.
    
    Permite listar, crear, actualizar y eliminar herramientas a través de
    endpoints REST automáticamente generados por Django REST Framework.
    """
    
    queryset = Herramientas.objects.all()
    serializer_class = HerramientasSerializer

    def list(self, request, *args, **kwargs):
        """
        Obtiene la lista completa de herramientas sin paginación.
        
        GET /api/herramientas/
        
        Returns:
            Response: Lista de todas las herramientas en formato JSON
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        """
        Crea una nueva herramienta en el sistema.
        
        POST /api/herramientas/
        
        Valida los datos recibidos y crea un nuevo registro en la base de datos
        si la información es válida.
        
        Args:
            request: Petición HTTP con datos de la herramienta
            
        Returns:
            Response: Datos de la herramienta creada con status 201
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """
        Actualiza completamente una herramienta existente (PUT).
        
        PUT /api/herramientas/{id}/
        
        Valida los datos y actualiza todos los campos de la herramienta.
        Requiere que se envíen todos los campos obligatorios.
        
        Args:
            request: Petición HTTP con datos actualizados
            
        Returns:
            Response: Datos actualizados de la herramienta
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
        Elimina una herramienta del sistema.
        
        DELETE /api/herramientas/{id}/
        
        Elimina permanentemente una herramienta de la base de datos.
        
        Args:
            request: Petición HTTP de eliminación
            
        Returns:
            Response: Confirmación de eliminación con status 204
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
