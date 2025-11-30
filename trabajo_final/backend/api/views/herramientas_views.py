from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from ..models.herramientas import Herramientas
from ..serializers.herramientas_serializer import HerramientasSerializer


class Herramientas_ViewSet(viewsets.ModelViewSet):
    queryset = Herramientas.objects.all()
    serializer_class = HerramientasSerializer
    
    def list(self, request, *args, **kwargs):
        """Obtener lista de herramientas sin paginación"""
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def create(self, request, *args, **kwargs):
        """Crear nueva herramienta"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    def update(self, request, *args, **kwargs):
        """Actualizar herramienta"""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """Eliminar herramienta"""
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
