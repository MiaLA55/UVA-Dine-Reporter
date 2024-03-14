from django.urls import path
from . import views

app_name = "file_upload"
urlpatterns = [
    path('user_submit_report/', views.user_submit_report, name='user_submit_report'),
    path('success/', views.success, name='success'),
]