from rest_framework import serializers
from ..models import Machine, FaultCase, Warning, Collection


class MachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Machine
        fields = '__all__'

class FaultCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultCase
        fields = '__all__'

class WarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warning
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name'] 