from django.http import response
from django.test import TestCase
from django.urls.base import resolve, reverse
from .views import signup

class SignUpTest(TestCase):
    def test_signup_status_code(self):
        url = reverse('signup')
        response = self.client.get(url)
        self.assertEquals(response.status_code,200)

    def test_singnup_url_resolves_signuap_view(self):
        view = resolve('/signup/')
        self.assertEquals(view.func,signup)