from rest_framework import serializers
from ..models import Machine, FaultCase, MachineWarning, Collection


class MachineSerializer(serializers.ModelSerializer):
    technicians = serializers.StringRelatedField(many=True)
    repair_personnel = serializers.StringRelatedField(many=True)
    collections = serializers.StringRelatedField(many=True)

    class Meta:
        model = Machine
        fields = '__all__'


class FaultCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = FaultCase
        fields = '__all__'

class WarningSerializer(serializers.ModelSerializer):
    class Meta:
        model = MachineWarning
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'name'] 