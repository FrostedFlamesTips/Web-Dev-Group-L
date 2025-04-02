from rest_framework.decorators import api_view
from rest_framework.response import Response
from ACME.models import Machine
from .serializers import MachineSerializer, WarningSerializer, FaultCaseSerializer  

@api_view(['GET'])
def machine_list(request):
    machines = Machine.objects.all()
    serializer = MachineSerializer(machines, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def report_warning(request):
    serializer = WarningSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)



