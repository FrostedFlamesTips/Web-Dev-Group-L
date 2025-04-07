from django import forms
from .models import Collection, Machine, FaultCase
from django.contrib.auth import get_user_model

class CollectionForm(forms.ModelForm):
    class Meta:
        model = Collection
        fields = ['name']

class MachineForm(forms.ModelForm):
    class Meta:
        model = Machine
        fields = ['name', 'description', 'status', 'priority', 'collections', 'technicians', 'repair_personnel']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }


User = get_user_model()  #Needed in fault case form

class FaultCaseForm(forms.ModelForm):
    class Meta:
        model = FaultCase
        fields = ['machine', 'summary', 'resolved', 'resolved_by']
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
        }

    assigned_technicians = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(role='Technician'),  
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Assign Technicians"
    )
