from rest_framework import serializers
from api.models.herramientas import Herramientas

class Serializador_Herramientas(serializers.ModelSerializer):
    class Meta:
        model = Herramientas
        exclude = ['created_at']