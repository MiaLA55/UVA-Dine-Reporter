from django.urls import path
from . import views

app_name = "login"
urlpatterns = [
    path("", views.home, name="home"),
    path("auth_home/", views.auth_home, name="auth_home"),
    path("admin_home/", views.admin_home, name="admin_home"),
    path("logout/", views.logout_view, name="logout"),
    path("upload/", views.upload_file, name="upload_file"),
    # path("viewfiles/", views.view_file, name="view_file"),
    path("list_files/", views.list_files, name="list_files"),
    path("user_reports/", views.list_specific_user_files, name="user_reports"),
    path("detail/<str:file_name>/", views.file_detail, name="file_detail"),
    path(
        "resolve_report_submit/",
        views.resolve_report_submit,
        name="resolve_report_submit",
    ),
]
