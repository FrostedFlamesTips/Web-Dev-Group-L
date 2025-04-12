from django.shortcuts import render, redirect, get_object_or_404
import csv
from django.http import HttpResponse
from .models import Machine, Collection, FaultCase, FaultImage
from .forms import CollectionForm, MachineForm, FaultCaseForm, MachineWarningForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login

User = get_user_model()
from django.http import HttpResponseForbidden
from .models import MachineWarning
from django.utils import timezone
from collections import defaultdict



def index(request):
    # Chart Data
    collections = Collection.objects.prefetch_related('machines')
    chart_data = defaultdict(lambda: {'OK': 0, 'Warning': 0, 'Fault': 0})

    for collection in collections:
        for machine in collection.machines.all():
            chart_data[collection.name][machine.status] += 1

    labels = list(chart_data.keys())
    datasets = {
        'OK': [chart_data[label]['OK'] for label in labels],
        'Warning': [chart_data[label]['Warning'] for label in labels],
        'Fault': [chart_data[label]['Fault'] for label in labels],
    }

    # Faults and Warnings
    recent_faults = FaultCase.objects.select_related('machine').order_by('-created_at')[:3]
    active_warnings = MachineWarning.objects.filter(resolved=False).select_related('machine').order_by('-added_at')[:3]

    context = {
        'labels': labels,
        'ok_data': datasets['OK'],
        'warning_data': datasets['Warning'],
        'fault_data': datasets['Fault'],
        'recent_faults': recent_faults,
        'active_warnings': active_warnings,
    }

    return render(request, 'index.html', context)

def index_view(request):
    user = request.user
    collections = Collection.objects.all()
    recent_faults = FaultCase.objects.select_related('machine').order_by('-created_at')[:3]
    active_warnings = MachineWarning.objects.filter(resolved=False).select_related('machine').order_by('-added_at')[:3]

    view_all = request.GET.get('view') == 'all'
    assigned_machines = Machine.objects.none()

    if user.is_authenticated:
        print(f"User role: {user.role}")
        if user.role == 'Technician':
            assigned_machines = user.assigned_machines_technician.all()
        elif user.role == 'Repair':
            assigned_machines = user.assigned_machines_repair.all()
        print("Assigned machines queryset:", assigned_machines)
        print("Assigned machine names:", [m.name for m in assigned_machines])

    # Force evaluation
    assigned_machines_list = list(assigned_machines)
    print("Assigned machines list length:", len(assigned_machines_list))

    labels, ok_data, warning_data, fault_data = [], [], [], []
    for collection in collections:
        machines = collection.machines.all()
        if user.role in ['Technician', 'Repair'] and not view_all:
            machines = machines.filter(id__in=[m.id for m in assigned_machines_list])
        labels.append(collection.name)
        ok_data.append(machines.filter(status='OK').count())
        warning_data.append(machines.filter(status='Warning').count())
        fault_data.append(machines.filter(status='Fault').count())

    context = {
        'labels': labels,
        'ok_data': ok_data,
        'warning_data': warning_data,
        'fault_data': fault_data,
        'recent_faults': recent_faults,
        'active_warnings': active_warnings,
        'assigned_machines': assigned_machines_list,
        'assigned_machines_count': len(assigned_machines_list),
        'show_toggle': user.role in ['Technician', 'Repair'],
        'view_all': view_all,
    }

    return render(request, 'index.html', context)

def home_view(request):
    return render(request, 'home.html')

def pricing_view(request):
    return render(request, 'pricing.html')

def testimonials_view(request):
    return render(request, 'testimonials.html')

def privacy_view(request):
    return render(request, 'privacy.html')

def contact_view(request):
    return render(request, 'contact.html')

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

def machine_details(request):
    return render(request, 'machine-details.html')

def machinery(request):
    return render(request, 'machinery.html')

def report_fault(request):
    return render(request, 'report-fault.html')

def warnings(request):
    return render(request, 'warnings.html')

def export_machines_csv(request):
    if not request.user.is_authenticated or request.user.role != 'Manager':
        return HttpResponse("Unauthorized", status=401)

    collection_id = request.GET.get('collection_id')
    machine_id = request.GET.get('machine_id')

    machines = Machine.objects.all()

    if collection_id:
        machines = machines.filter(collections__id=collection_id)

    if machine_id:
        machines = machines.filter(id=machine_id)

    machines = machines.distinct().order_by('-priority')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="machines_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Name', 'Status', 'Priority', 'Created At'])

    for machine in machines:
        writer.writerow([
            machine.name,
            machine.status,
            machine.priority,
            machine.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    return response

def collections_view(request):
    search_query = request.GET.get('search', '')
    collections = Collection.objects.filter(name__icontains=search_query)
    return render(request, 'collections.html', {'collections': collections})

def collection_details_view(request, id):
    collection = Collection.objects.get(id=id)
    machines = Machine.objects.filter(collection_id=id)
    return render(request, 'collection-details.html', {'collection': collection, 'machines': machines})

def add_collection_view(request):
    if request.method == 'POST':
        form = CollectionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('collections')  
    else:
        form = CollectionForm()
    return render(request, 'collection-create.html', {'form': form})


def delete_collection_view(request, id):
    if request.method == 'POST':  
        collection = get_object_or_404(Collection, id=id)
        collection.delete()
        return redirect('collections')  
    else:
        return HttpResponse("Invalid request method", status=405)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')  # or your desired landing page
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

def machinery_list(request):
    machines = Machine.objects.all().prefetch_related('collections', 'technicians', 'repair_personnel')
    return render(request, 'machinery.html', {'machines': machines})

def machinery_detail(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    return render(request, 'machinery-details.html', {'machine': machine})

@login_required
def machinery_list_view(request):
    return render(request, 'machinery.html')


@login_required
def add_machine_view(request):
    if request.user.role != 'Manager':
        return HttpResponseForbidden("Only managers can add machines.")

    if request.method == 'POST':
        form = MachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('machinery_list')
    else:
        form = MachineForm()

    return render(request, 'add_machine.html', {'form': form})

@login_required
def edit_machine_view(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)

    # Only managers can edit
    if request.user.role != 'Manager':
        return HttpResponseForbidden("Only managers can edit machines.")

    if request.method == 'POST':
        form = MachineForm(request.POST, instance=machine)
        if form.is_valid():
            form.save()
            return redirect('machinery_list')
    else:
        form = MachineForm(instance=machine)

    
    technicians = User.objects.filter(role='Technician')
    collections = Collection.objects.all()

    return render(request, 'edit-machine.html', {
        'machine': machine,
        'form': form,
        'technicians': technicians,
        'collections': collections
    })

def machinery_detail(request, machine_id):
    machine = get_object_or_404(Machine, id=machine_id)
    return render(request, 'machine-details.html', {'machine': machine})

def index_view(request):
    return render(request, 'index.html')

@login_required
def create_fault_view(request):
    machine_id = request.GET.get('id')
    initial = {}

    if machine_id:
        machine = get_object_or_404(Machine, id=machine_id)
        initial['machine'] = machine

    if request.method == 'POST':
        form = FaultCaseForm(request.POST, request.FILES)
        files = request.FILES.getlist('images')

        if form.is_valid():
            fault = form.save(commit=False)
            fault.created_by = request.user
            fault.save()
            form.save_m2m()

            for f in files:
                FaultImage.objects.create(
                    fault_case=fault,
                    image_file=f,
                    uploaded_by=request.user
                )

            return redirect('faults_list')
    else:
        form = FaultCaseForm(initial=initial)
        form.fields['assigned_technicians'].queryset = User.objects.filter(role='Technician')
    return render(request, 'report-fault.html', {'form': form})

def faults_list_view(request):
    faults = FaultCase.objects.select_related('machine', 'created_by', 'resolved_by')
    return render(request, 'faults.html', {'faults': faults})

def fault_detail(request, fault_id):
    fault = get_object_or_404(FaultCase, id=fault_id)
    return render(request, 'fault-details.html', {'fault': fault})

@login_required
def resolve_fault(request, fault_id):
    fault = get_object_or_404(FaultCase, id=fault_id)
    if request.method == 'POST':
        fault.resolved = True
        fault.resolved_by = request.user
        fault.resolved_at = timezone.now()
        fault.save()
    return redirect('fault_detail', fault_id=fault.id)

@login_required
def edit_fault(request, fault_id):
    fault = get_object_or_404(FaultCase, id=fault_id)

    if request.method == 'POST':
        form = FaultCaseForm(request.POST, instance=fault)
        if form.is_valid():
            fault = form.save(commit=False)
            fault.save()
            form.save_m2m()  
            return redirect('faults_list')
    else:
        form = FaultCaseForm(instance=fault)
        form.fields['assigned_technicians'].initial = fault.assigned_technicians.all()

    return render(request, 'edit-fault.html', {'form': form, 'fault': fault})

@login_required
def warnings_view(request):
    warnings = MachineWarning.objects.filter(resolved=False).select_related('machine', 'added_by')
    return render(request, 'warnings.html', {'warnings': warnings})

@login_required
def create_warning_view(request):
    if request.method == 'POST':
        form = MachineWarningForm(request.POST)
        if form.is_valid():
            warning = form.save(commit=False)
            warning.added_by = request.user
            warning.save()
            return redirect('warnings')  
    else:
        form = MachineWarningForm()
    return render(request, 'create-warning.html', {'form': form})

@login_required
def resolve_warning_view(request, warning_id):
    warning = get_object_or_404(MachineWarning, id=warning_id)
    warning.resolved = True
    warning.resolved_by = request.user
    warning.resolved_at = timezone.now()
    warning.save()
    return redirect('warnings') 

@login_required
def warning_detail_view(request, warning_id):
    warning = get_object_or_404(MachineWarning, id=warning_id)
    return render(request, 'warning-details.html', {'warning': warning})

@login_required
def dashboard_view(request):
    user = request.user
    view_all = request.GET.get('view') == 'all'

    # Decide which machines to show based on role
    if user.role == 'Manager' or view_all:
        machines = Machine.objects.all()
    elif user.role == 'Technician':
        machines = Machine.objects.filter(technicians=user)
    elif user.role == 'Repair':
        machines = Machine.objects.filter(repair_personnel=user)
    else:
        machines = Machine.objects.none()

    # Pull recent fault cases and active warnings based on those machines
    recent_faults = FaultCase.objects.filter(machine__in=machines).select_related('machine').order_by('-created_at')[:3]
    active_warnings = MachineWarning.objects.filter(machine__in=machines, resolved=False).select_related('machine').order_by('-added_at')[:3]

    # Build chart data for machinery status per collection
    collections = Collection.objects.all()
    labels = []
    ok_data = []
    warning_data = []
    fault_data = []

    for collection in collections:
        collection_machines = machines.filter(collections=collection)
        labels.append(collection.name)
        ok_data.append(collection_machines.filter(status='OK').count())
        warning_data.append(collection_machines.filter(status='Warning').count())
        fault_data.append(collection_machines.filter(status='Fault').count())

    context = {
        'labels': labels,
        'ok_data': ok_data,
        'warning_data': warning_data,
        'fault_data': fault_data,
        'recent_faults': recent_faults,
        'active_warnings': active_warnings,
        'machines': machines,
        'view_all': view_all,
        'show_toggle': user.role in ['Technician', 'Repair'],
    }

    return render(request, 'index.html', context)

def test_record_api_view(request):
    return render(request, 'test-record-api.html')
