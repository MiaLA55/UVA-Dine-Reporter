from django.urls import path
from . import views

app_name = "login"
urlpatterns = [
    path("", views.home, name="home"),
    path("auth_home/", views.auth_home, name="auth_home"),
    path("admin_home/", views.admin_home, name="admin_home"),
    path("logout/", views.logout_view, name="logout"),
    path("upload/", views.upload_file, name="upload_file"),
    path("list_files/", views.list_files, name="list_files"),
    path("user_reports/", views.list_specific_user_files, name="user_reports"),
    path("user_list_files_new/", views.user_list_files_new, name="user_list_files_new"),
    path("user_list_files_ip/", views.user_list_files_ip, name="user_list_files_ip"),
    path("user_list_files_resolved/", views.user_list_files_resolved, name="user_list_files_resolved"),
    path("individual_file_view/<int:report_id>/", views.individual_file_view, name="individual_file_view"),
    path("detail/<str:file_name>/", views.file_detail, name="file_detail"),
    path(
        "resolve_report_submit/<int:report_id>/",
        views.resolve_report_submit,
        name="resolve_report_submit",
    ),
    path("delete_report/<int:report_id>/", views.delete_report, name="delete_report"),
]
