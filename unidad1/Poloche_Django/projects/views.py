from rest_framework import viewsets
from .models import FirstProject
from .serializers import ProductoSerializer

# Create your views here.

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = FirstProject.objects.all()
    serializer_class = ProductoSerializer
