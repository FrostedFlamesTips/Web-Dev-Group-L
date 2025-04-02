from django.urls import path
from . import views_api

urlpatterns = [
    path('machines/', views_api.machine_list, name='api-machine-list'),
    path('report_warning/', views_api.report_warning, name='api-report-warning'),
]