from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

class User(AbstractUser): #Database model for custom users
    ROLE_CHOICES = [
        ('Technician', 'Technician'),
        ('Repair', 'Repair'),
        ('Manager', 'Manager'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

class Collection(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Machine(models.Model): #Database model for machines
    STATUS_CHOICES = [
        ('OK', 'OK'),
        ('Warning', 'Warning'),
        ('Fault', 'Fault'),
    ]
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')
    priority = models.IntegerField(default=0)
    collections = models.ManyToManyField(Collection, blank=True, related_name='machines')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    technicians = models.ManyToManyField(
        User, 
        blank=True, 
        related_name='assigned_machines_technician',
        limit_choices_to={'role': 'Technician'}
    )
    repair_personnel = models.ManyToManyField(
        User, 
        blank=True, 
        related_name='assigned_machines_repair',
        limit_choices_to={'role': 'Repair'}
    )
    def update_status(self):
        if self.faultcase_set.filter(resolved=False).exists():
            self.status = 'Fault'
        elif self.warnings.filter(resolved=False).exists():
            self.status = 'Warning'
        else:
            self.status = 'OK'
        self.save()
        
    def __str__(self):
        return f"{self.name} ({self.id})"


class MachineWarning(models.Model): #Database model for machine warnings. Renamed from warnings as it caused issues with a built-in python function
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name='warnings')
    warning_text = models.TextField()
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='warnings_added')
    added_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='warnings_resolved')
    resolved_at = models.DateTimeField(null=True, blank=True)

class FaultCase(models.Model): #Database model for fault cases
    case_number = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='faults_created')
    created_at = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='faults_resolved')
    resolved_at = models.DateTimeField(null=True, blank=True)
    summary = models.TextField(blank=True, null=True)
    assigned_technicians = models.ManyToManyField(
    User,
    blank=True,
    related_name='assigned_fault_cases',
    limit_choices_to={'role': 'Technician'}
)

class FaultNote(models.Model): #Database model for fault notes
    fault_case = models.ForeignKey(FaultCase, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    note = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class FaultImage(models.Model): # Database model for fault images
    fault_case = models.ForeignKey(FaultCase, on_delete=models.CASCADE)
    image_file = models.FileField(upload_to='fault_images/')
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)