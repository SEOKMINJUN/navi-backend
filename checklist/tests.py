from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.models import User
from .models import ChecklistItem

class ChecklistModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            nickname='테스트유저',
            student_id='20240001'
        )
        self.checklist_item = ChecklistItem.objects.create(
            user=self.user,
            item_name='테스트 항목',
            status=False
        )

    def test_checklist_item_creation(self):
        self.assertEqual(self.checklist_item.user, self.user)
        self.assertEqual(self.checklist_item.item_name, '테스트 항목')
        self.assertFalse(self.checklist_item.status)

    def test_unique_constraints(self):
        with self.assertRaises(Exception):
            ChecklistItem.objects.create(
                user=self.user,
                item_name='테스트 항목',
                status=True
            )

class ChecklistAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            nickname='테스트유저',
            student_id='20240001'
        )
        self.client.force_authenticate(user=self.user)
        self.checklist_item = ChecklistItem.objects.create(
            user=self.user,
            item_name='테스트 항목',
            status=False
        )

    def test_create_checklist_item(self):
        url = reverse('checklist')
        data = {
            'item_name': '새로운 항목',
            'status': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(ChecklistItem.objects.count(), 2)

    def test_update_checklist_item(self):
        url = reverse('checklist-detail', args=[self.checklist_item.id])
        data = {
            'status': True
        }
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.checklist_item.refresh_from_db()
        self.assertTrue(self.checklist_item.status)

    def test_delete_checklist_item(self):
        url = reverse('checklist-detail', args=[self.checklist_item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ChecklistItem.objects.count(), 0)

    def test_list_checklist_items(self):
        url = reverse('checklist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
