from django.shortcuts import render
import csv
from django.http import HttpResponse
from .models import Machine
def index(request):
    return render(request, 'index.html')

def collection_details(request):
    return render(request, 'collection-details.html')

def collection_edit(request):
    return render(request, 'collection-edit.html')

def collections(request):
    return render(request, 'collections.html')

def edit_fault(request):
    return render(request, 'edit-fault.html')

def edit_machine(request):
    return render(request, 'edit-machine.html')

def fault_details(request):
    return render(request, 'fault-details.html')

def faults(request):
    return render(request, 'faults.html')

def login(request):
    return render(request, 'login.html')

def machine_details(request):
    return render(request, 'machine-details.html')

def machinery(request):
    return render(request, 'machinery.html')

def report_fault(request):
    return render(request, 'report-fault.html')

def warnings(request):
    return render(request, 'warnings.html')

def export_machines_csv(request):
    if request.user.role != 'Manager':
        return HttpResponse("Unauthorized", status=401)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="machines_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Status', 'Priority', 'Created At'])

    machines = Machine.objects.all().order_by('-priority')
    for machine in machines:
        writer.writerow([machine.name, machine.status, machine.priority, machine.created_at])

    return response
