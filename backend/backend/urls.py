"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from ACME.views import index
from ACME.views import collection_details
from ACME.views import collection_edit
from ACME.views import collections
from ACME.views import edit_fault
from ACME.views import edit_machine
from ACME.views import fault_details
from ACME.views import faults
from ACME.views import login
from ACME.views import machine_details
from ACME.views import machinery
from ACME.views import report_fault
from ACME.views import warnings
from django.conf import settings
from django.conf.urls.static import static
from ACME import views
from ACME.views import machinery_list_view, add_machine_view

urlpatterns = [
    path('admin', admin.site.urls),
    path('', index),
    path ('index.html', index),
    path('collection-details.html', collection_details),
    path('collection-edit.html', collection_edit),
    path('edit-fault.html', edit_fault),
    path('edit-machine.html', edit_machine),
    path('fault-details.html', fault_details),
    path('faults.html', faults),
    path('login.html', login),
    path('machine-details.html', machine_details),
    #path('machinery.html', machinery),
    path('report-fault.html', report_fault),
    path('warnings.html', warnings),
    path('api/', include('ACME.api.urls')),
    path('collections/delete/<int:id>/', views.delete_collection_view, name='delete_collection'),
    path('collection-create.html', views.add_collection_view, name='add_collection'),
    path('collections.html', views.collections_view, name='collections'),
    path('machinery/', machinery_list_view, name='machinery_list'),
    path('machinery/add/', add_machine_view, name='add_machine'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
