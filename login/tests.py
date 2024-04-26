from unittest import TestCase
from django.contrib.auth import authenticate, login
from django.test import Client
from django.urls import reverse
from login.views import login_view
from django.contrib.auth.models import User  # Assuming User model is defined

class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()  # Use Client for sessions and messages

    def test_login_view_post(self):
        # No need to manually create a request or set user in request (handled by Client)
        response = self.client.post('/login/', {'username': 'admin', 'password': 'admin'})
        self.assertEqual(response.status_code, 200)

    def test_login_view_get(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

"""
    def test_login_view_invalid_credentials(self):
        request = self.client.post('/login/', {'username': 'invaliduser', 'password': 'invalidpassword'})
        response = login_view(request)
        self.assertEqual(response.status_code, 200)

    def test_login_view_no_credentials(self):
        request = self.client.post('/login/', {})
        response = login_view(request)
        self.assertEqual(response.status_code, 200)

    def test_login_view_missing_credentials(self):
        request = self.client.post('/login/', {'username': 'testuser'})
        response = login_view(request)
        self.assertEqual(response.status_code, 200)

    def test_login_view_invalid_method(self):
        request = self.client.get('/login/')
        response = login_view(request)
        self.assertEqual(response.status_code, 200)
"""