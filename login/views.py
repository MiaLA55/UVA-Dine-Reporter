from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.urls import reverse


# views.py


def auth_home(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='Site Admin').exists():
            return render(request=request, template_name="login/admin_home.html", context={})
        else:
            return render(request=request, template_name="login/auth_home.html", context={})
    else:
        return render(request, template_name="login/logout.html")


def home(request):
    return render(request=request, template_name="login/home.html", context={})


def logout_view(request):
    logout(request)
    return render(request, template_name="login/logout.html")

class CustomLoginView(LoginView):
    default_template_name = "login/auth_home.html"
    admin_template_name = "login/admin_home.html"  # Template for admin users

    def get_template_names(self):
        # Check if the user belongs to the 'Site Admin' group
        if self.request.user.groups.filter(name='Site Admin').exists():
            return [self.admin_template_name]
        else:
            return [self.default_template_name]

    def get_success_url(self):
        # Redirect users after login
        if self.request.user.groups.filter(name='Site Admin').exists():
            return reverse('admin_dashboard')  # Assuming 'admin_dashboard' is the URL name for admin dashboard
        else:
            return reverse('user_dashboard')  # Assuming 'user_dashboard' is the URL name for user dashboard

    def get(self, request, *args, **kwargs):
        # Ensure proper template rendering
        return render(request, self.get_template_names()[0], self.get_context_data())