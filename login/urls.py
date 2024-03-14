from django.urls import path
from . import views

app_name = "login"
urlpatterns = [
    path("", views.home, name="home"),
    path("auth_home/", views.auth_home, name="auth_home"),
    path("logout/", views.logout_view, name="logout"),
    #path("upload/", views.upload_file, name="upload_file"),
]
