from django.shortcuts import render, redirect, get_object_or_404
import csv
from django.http import HttpResponse
from .models import Machine, Collection
from .forms import CollectionForm, MachineForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib import messages
from django.http import HttpResponseForbidden

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

def index_view(request):
    return render(request, 'index.html')