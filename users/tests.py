from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse

from .models import User


class UserRegistrationTestCase(TestCase):

    def setUp(self) -> None:
        self.path = reverse('users:register')
        self.user_data = {
            'first_name': 'test',
            'last_name': 'test',
            'username': 'test12',
            'password1': 'Aa1234567',
            'password2': 'Aa1234567',
            'email': 'exasdsad@ya.ru'
        }

    def test_user_registrate_get(self):
        response = self.client.get(self.path)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_create_user(self):
        response = self.client.post(path=self.path, data=self.user_data)

        self.assertEquals(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse('users:login'))

    def test_login_user(self):
        path = reverse('users:login')
        data = {'username': self.user_data['username'], 'password': self.user_data['password1']}
        response = self.client.post(path=path, data=data, follow=True)

        self.assertEquals(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'users/login.html')
