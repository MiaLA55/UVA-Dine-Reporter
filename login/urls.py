from django.urls import path

from . import views

app_name = "login"
urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login, name="login"),
    path("auth_home/", views.auth_home, name="auth_home"),
]
