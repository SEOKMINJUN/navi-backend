from django.test import TestCase
from django.urls import reverse
from accounts.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Schedule
from datetime import datetime, timedelta
from django.utils import timezone

# Create your tests here.

class ScheduleTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword',
            student_id='12345678',
            nickname='testname',
        )
        self.admin_user = User.objects.create_superuser(
            username='admin', 
            email='admin@example.com', 
            password='adminpassword',
            student_id='0',
            nickname='Admin',
        )
        
        # 두 명의 사용자를 위한 스케줄 생성
        self.user_echedule = Schedule.objects.create(
            title='User Schedule',
            description='Test Schedule for user',
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=1),
            user=self.user
        )
        
        self.admin_echedule = Schedule.objects.create(
            title='Admin Schedule',
            description='Test Schedule for admin',
            start_time=timezone.now(),
            end_time=timezone.now() + timedelta(hours=2),
            user=self.admin_user
        )
        
        self.client = APIClient()
    
    def test_create_echedule(self):
        """스케줄 생성 테스트"""
        self.client.force_authenticate(user=self.user)
        url = reverse('schedule-list')
        data = {
            'title': 'New Schedule',
            'description': 'Test new Schedule',
            'start_time': timezone.now().isoformat(),
            'end_time': (timezone.now() + timedelta(hours=1)).isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Schedule.objects.count(), 3)
        self.assertEqual(Schedule.objects.get(title='New Schedule').user, self.user)
    
    def test_get_echedules(self):
        """스케줄 조회 테스트"""
        # 일반 사용자는 자신의 스케줄만 볼 수 있음
        self.client.force_authenticate(user=self.user)
        url = reverse('schedule-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'User Schedule')
        
        # 관리자는 모든 스케줄를 볼 수 있음
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
    
    def test_update_echedule(self):
        """스케줄 수정 테스트"""
        self.client.force_authenticate(user=self.user)
        url = reverse('schedule-detail', args=[self.user_echedule.id])
        data = {
            'title': 'Updated Schedule',
            'description': 'Updated description',
            'start_time': timezone.now().isoformat(),
            'end_time': (timezone.now() + timedelta(hours=3)).isoformat()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Schedule.objects.get(id=self.user_echedule.id).title, 'Updated Schedule')
    
    def test_delete_echedule(self):
        """스케줄 삭제 테스트"""
        self.client.force_authenticate(user=self.user)
        url = reverse('schedule-detail', args=[self.user_echedule.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Schedule.objects.filter(id=self.user_echedule.id).count(), 0)
    
    def test_echedule_permission(self):
        """스케줄 권한 테스트"""
        # 다른 사용자의 스케줄 접근 시도
        self.client.force_authenticate(user=self.user)
        url = reverse('schedule-detail', args=[self.admin_echedule.id])
        
        # 조회 시도
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # 수정 시도
        data = {'title': 'Trying to update'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # 삭제 시도
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)