from django.urls import path
from . import views_api
from .views_api import MachineListCreateAPIView, MachineDetailAPIView

urlpatterns = [
    path('machines/', views_api.machine_list, name='api-machine-list'),
    path('report_warning/', views_api.report_warning, name='api-report-warning'),
    path('machines/', MachineListCreateAPIView.as_view(), name='machine-list'),
    path('machines/<int:pk>/', MachineDetailAPIView.as_view(), name='machine-detail'),
]