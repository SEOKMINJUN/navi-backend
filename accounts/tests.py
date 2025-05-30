from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import User

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'nickname': '테스트유저',
            'student_id': '20240001'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.nickname, '테스트유저')
        self.assertEqual(self.user.student_id, '20240001')

    def test_unique_constraints(self):
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                password='testpass123',
                nickname='테스트유저',
                student_id='20240002'
            )
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                password='testpass123',
                nickname='테스트유저2',
                student_id='20240001'
            )

class UserAPITest(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'nickname': '테스트유저',
            'student_id': '20240001'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.client.force_authenticate(user=self.user)

    def test_user_registration(self):
        url = reverse('signup')
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'password': 'newpass123',
            'nickname': '새유저',
            'student_id': '20240002'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_user_login(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refresh', response.data)
