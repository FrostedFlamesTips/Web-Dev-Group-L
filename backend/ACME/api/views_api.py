from rest_framework.decorators import api_view
from rest_framework.response import Response
from ACME.models import Machine, MachineWarning, Collection
from .serializers import MachineSerializer, WarningSerializer, CollectionSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from .permissions import IsManager


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


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer

class MachineListCreateAPIView(generics.ListCreateAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), IsManager()]
        return [permissions.AllowAny()]

class MachineDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Machine.objects.all()
    serializer_class = MachineSerializer