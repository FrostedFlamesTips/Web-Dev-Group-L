from django import forms
from .models import Collection, Machine, FaultCase
from django.contrib.auth import get_user_model
from .models import MachineWarning

class CollectionForm(forms.ModelForm): #Form for creating and updating collections
    class Meta:
        model = Collection
        fields = ['name']

class MachineForm(forms.ModelForm): #Form for creating and updating machines
    class Meta:
        model = Machine
        fields = ['name', 'description', 'status', 'priority', 'collections', 'technicians', 'repair_personnel']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


User = get_user_model()  #Needed in fault case form

class FaultCaseForm(forms.ModelForm): # Form for creating and updating fault cases
    class Meta:
        model = FaultCase
        fields = ['machine', 'summary', 'resolved', 'resolved_by', 'assigned_technicians']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
        }

    assigned_technicians = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='Technician'),  
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign Technicians"
    )


class MachineWarningForm(forms.ModelForm): # Form for creating and updating machine warnings
    class Meta:
        model = MachineWarning
        fields = ['machine', 'warning_text']

