from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import User

class UserLoginSignupTests(APITestCase):
    def setUp(self):
        self.signup_data = {
            'email': 'dumkaabhipray12890c@gmail.com',
            'password': 'notesneofi',
            'name': 'Abhipray',
            'contact': '1234567890'
        }
        self.login_data = {
            "email": "dumkaabhipray@gmail.com",
            "password": "notesneofi"
        }

    def tearDown(self):
        User.objects.filter(email=self.signup_data['email']).delete()

    def test_user_signup(self):
        url = reverse('signup')
        response = self.client.post(url, self.signup_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.filter(email=self.signup_data['email']).exists(), True)

    def test_user_login_user_does_not_exist(self):
        url = reverse('login')
        non_existent_user_data = {
            'email': 'nonexistent@example.com',
            'password': 'password',
        }
        response = self.client.post(url, non_existent_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, 'User does not exists')



