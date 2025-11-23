from rest_framework import serializers
from api.models.prestamos import Prestamos

class Serializador_Prestamos(serializers.ModelSerializer):
    class Meta:
        model = Prestamos
        exclude = ['created_at']