from django import forms
from .models import Collection, Machine

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