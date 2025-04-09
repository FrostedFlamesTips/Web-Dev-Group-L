from rest_framework.decorators import api_view
from rest_framework.response import Response
from ACME.models import Machine, MachineWarning, Collection, FaultCase
from .serializers import MachineSerializer, WarningSerializer, CollectionSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics, permissions
from .permissions import IsManager
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
import json


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

@csrf_exempt
def external_record_event(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            machine_id = data.get('machine_id')
            event_type = data.get('event_type')  # 'warning' or 'fault'
            message = data.get('message', '')

            print(f"Received event for machine ID: {machine_id}, type: {event_type}, message: {message}")
            machine = get_object_or_404(Machine, id=machine_id)

            if event_type == 'warning':
                MachineWarning.objects.create(machine=machine, warning_text=message, added_by=None, resolved=False)
                machine.update_status()
            elif event_type == 'fault':
                FaultCase.objects.create(machine=machine, summary=message, created_by=None, resolved=False)
                machine.update_status()
            else:
                return JsonResponse({'error': 'Invalid event_type'}, status=400)

            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)


def machine_status_api(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    return JsonResponse({
        'machine_id': machine.id,
        'name': machine.name,
        'status': machine.status,
        'priority': machine.priority
    })


def open_fault_cases_api(request):
    cases = FaultCase.objects.filter(resolved=False).select_related('machine')
    data = [
        {
            'id': f.id,
            'case_number': str(f.case_number),
            'machine': f.machine.name,
            'summary': f.summary,
            'created_at': f.created_at.isoformat()
        }
        for f in cases
    ]
    return JsonResponse({'open_cases': data})


def fault_case_detail_api(request, fault_id):
    fault = get_object_or_404(FaultCase, id=fault_id)
    return JsonResponse({
        'id': fault.id,
        'case_number': str(fault.case_number),
        'machine': fault.machine.name,
        'summary': fault.summary,
        'resolved': fault.resolved,
        'created_at': fault.created_at.isoformat(),
    })


@csrf_exempt
def add_fault_note_api(request, fault_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            note = data.get('comment')
            fault = get_object_or_404(FaultCase, id=fault_id)
            
            fault.summary += f"\n[Note]: {note}"
            fault.save()

            return JsonResponse({'status': 'note added'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'POST required'}, status=405)