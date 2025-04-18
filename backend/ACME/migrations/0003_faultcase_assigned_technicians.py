# Generated by Django 5.2 on 2025-04-07 07:44

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ACME', '0002_collection_machine_repair_personnel_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='faultcase',
            name='assigned_technicians',
            field=models.ManyToManyField(blank=True, limit_choices_to={'role': 'Technician'}, related_name='assigned_fault_cases', to=settings.AUTH_USER_MODEL),
        ),
    ]
