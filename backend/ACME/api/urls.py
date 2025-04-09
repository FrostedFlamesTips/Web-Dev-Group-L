from django.urls import path
from . import views_api
from .views_api import MachineListCreateAPIView, MachineDetailAPIView

urlpatterns = [
    path('machines/', views_api.machine_list, name='api-machine-list'),
    path('report_warning/', views_api.report_warning, name='api-report-warning'),
    path('machines/', MachineListCreateAPIView.as_view(), name='machine-list'),
    path('machines/<int:pk>/', MachineDetailAPIView.as_view(), name='machine-detail'),
    path('record/', views_api.external_record_event, name='external_record_event'),
    path('machine/<int:machine_id>/status/', views_api.machine_status_api, name='machine_status_api'),
    path('faults/open/', views_api.open_fault_cases_api, name='open_fault_cases_api'),
    path('faults/<int:fault_id>/', views_api.fault_case_detail_api, name='fault_case_detail_api'),
    path('faults/<int:fault_id>/add-note/', views_api.add_fault_note_api, name='add_fault_note_api'),
]