# Generated by Django 5.1.7 on 2025-04-09 18:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ACME', '0004_rename_warning_machinewarning'),
    ]

    operations = [
        migrations.AlterField(
            model_name='machinewarning',
            name='machine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='warnings', to='ACME.machine'),
        ),
    ]
