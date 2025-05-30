from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class UserModelTest(TestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'password': 'testpass123',
            'nickname': '테스트유저',
            'student_id': '20240001',
            'email': 'test@example.com'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.nickname, '테스트유저')
        self.assertEqual(self.user.student_id, '20240001')
        self.assertEqual(self.user.email, 'test@example.com')

    def test_unique_constraints(self):
        # 닉네임 중복 테스트
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                password='testpass123',
                nickname='테스트유저',
                student_id='20240002',
                email='test2@example.com'
            )
        # 학번 중복 테스트
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                password='testpass123',
                nickname='테스트유저2',
                student_id='20240001',
                email='test2@example.com'
            )
        # 이메일 중복 테스트
        with self.assertRaises(Exception):
            User.objects.create_user(
                username='testuser2',
                password='testpass123',
                nickname='테스트유저2',
                student_id='20240002',
                email='test@example.com'
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

class PasswordResetRequestTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.password_reset_url = reverse('password_reset_request')
        
        # 테스트용 사용자 생성
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            student_id='20240001',
            nickname='테스트유저'
        )

    def test_password_reset_request_with_valid_email(self):
        """유효한 이메일로 비밀번호 초기화 요청 테스트"""
        data = {
            'email': 'test@example.com'
        }
        response = self.client.post(self.password_reset_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('temp_password', response.data)
        
        # 사용자의 비밀번호가 실제로 변경되었는지 확인
        user = User.objects.get(email='test@example.com')
        self.assertTrue(user.check_password(response.data['temp_password']))

    def test_password_reset_request_with_invalid_email(self):
        """존재하지 않는 이메일로 비밀번호 초기화 요청 테스트"""
        data = {
            'email': 'nonexistent@example.com'
        }
        response = self.client.post(self.password_reset_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

    def test_password_reset_request_without_email(self):
        """이메일 없이 비밀번호 초기화 요청 테스트"""
        data = {}
        response = self.client.post(self.password_reset_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_password_reset_request_with_empty_email(self):
        """빈 이메일로 비밀번호 초기화 요청 테스트"""
        data = {
            'email': ''
        }
        response = self.client.post(self.password_reset_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_password_reset_request_with_invalid_email_format(self):
        """잘못된 이메일 형식으로 비밀번호 초기화 요청 테스트"""
        data = {
            'email': 'invalid-email'
        }
        response = self.client.post(self.password_reset_url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)
