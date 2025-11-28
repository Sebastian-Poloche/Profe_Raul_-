from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django.shortcuts import render

@api_view(['GET'])
def api_root(request):
    """
    Vista personalizada para el root de la API.
    Muestra la página de inicio con interfaz mejorada.
    """
    return Response({
        'herramientas': reverse('herramientas-list', request=request),
        'prestamos': reverse('prestamos-list', request=request),
    })

def home(request):
    """
    Vista para la página de inicio con template personalizado.
    """
    return render(request, 'rest_framework/base_custom.html')
