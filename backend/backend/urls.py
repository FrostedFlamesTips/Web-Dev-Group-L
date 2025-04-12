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
from ACME.views import dashboard_view, add_collection_view
from django.conf import settings
from django.conf.urls.static import static
from ACME import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin', admin.site.urls),
    path('', views.home_view, name='public-index'), #New public facing home page
    path('dashboard/', dashboard_view, name='index'), #Original index page which is staff dashboard page
    path('login/', views.login_view, name='login'),
    path('api/', include('ACME.api.urls')),
    path('collections/delete/<int:id>/', views.delete_collection_view, name='delete_collection'),
    path('collection-create/', add_collection_view, name='add_collection'),
    path('collections/', views.collections_view, name='collections'),
    path('machinery/', views.machinery_list_view, name='machinery_list'),
    path('machinery/add/', views.add_machine_view, name='add_machine'),
    path('machinery/<int:machine_id>/edit/', views.edit_machine_view, name='edit_machine'),
    path('machinery/<int:machine_id>/', views.machinery_detail, name='machinery_detail'),
    path('export/csv/', views.export_machines_csv, name='export_machines_csv'),
    path('report-fault/', views.create_fault_view, name='report_fault'),
    path('faults/', views.faults_list_view, name='faults_list'),
    path('faults/<int:fault_id>/', views.fault_detail, name='fault_detail'),
    path('faults/<int:fault_id>/resolve/', views.resolve_fault, name='resolve_fault'),
    path('faults/<int:fault_id>/edit/', views.edit_fault, name='edit_fault'),
    path('warnings/', views.warnings_view, name='warnings'),
    path('warnings/create/', views.create_warning_view, name='create_warning'),
    path('warnings/resolve/<int:warning_id>/', views.resolve_warning_view, name='resolve_warning'),
    path('warnings/<int:warning_id>/', views.warning_detail_view, name='warning_detail'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('api/test-record/', views.test_record_api_view, name='test_record_api'),
    path('pricing/', views.pricing_view, name='pricing'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('privacy/', views.privacy_view, name='privacy'),
    path('contact/', views.contact_view, name='contact'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
