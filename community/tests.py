from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from datetime import datetime, timedelta
from django.utils import timezone

from .models import Board, Post, Comment, PostLike
from accounts.models import User

class BoardTests(APITestCase):
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
        
        self.board = Board.objects.create(
            name='Test Board',
            description='Board for testing'
        )
        
        self.client = APIClient()
    
    def test_list_boards(self):
        """게시판 목록 조회 테스트"""
        url = reverse('board-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Board')
    
    def test_create_board_permissions(self):
        """게시판 생성 권한 테스트"""
        url = reverse('board-list')
        data = {
            'name': 'New Board',
            'description': 'New board for testing'
        }
        
        # 인증되지 않은 사용자
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # 일반 사용자
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # 관리자
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Board.objects.count(), 2)
    
    def test_update_board(self):
        """게시판 수정 테스트"""
        url = reverse('board-detail', args=[self.board.id])
        data = {
            'name': 'Updated Board',
            'description': 'Updated description'
        }
        
        # 관리자만 수정 가능
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Board.objects.get(id=self.board.id).name, 'Updated Board')


class PostTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword',
            student_id='12345678',
            nickname='testname',
        )
        self.user2 = User.objects.create_user(
            username='testuser2', 
            email='test2@example.com', 
            password='testpassword',
            student_id='01234567',
            nickname='testname2',
        )
        
        self.board = Board.objects.create(
            name='Test Board',
            description='Board for testing'
        )
        
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            board=self.board,
            author=self.user
        )
        
        self.client = APIClient()
    
    def test_create_post(self):
        """게시글 생성 테스트"""
        self.client.force_authenticate(user=self.user)
        url = reverse('post-list')
        data = {
            'title': 'New Post',
            'content': 'New post content',
            'board': self.board.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)
        self.assertEqual(Post.objects.get(title='New Post').author, self.user)
    
    def test_list_posts(self):
        """게시글 목록 조회 테스트"""
        url = reverse('post-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        # 게시판 ID로 필터링
        response = self.client.get(f"{url}?board={self.board.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
    
    def test_retrieve_post(self):
        """게시글 상세 조회 및 조회수 증가 테스트"""
        url = reverse('post-detail', args=[self.post.id])
        
        # 조회 전 조회수 확인
        self.assertEqual(self.post.view_count, 0)
        
        # 게시글 조회
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Post')
        
        # 조회 후 조회수 확인
        self.post.refresh_from_db()
        self.assertEqual(self.post.view_count, 1)
    
    def test_update_post(self):
        """게시글 수정 테스트"""
        self.client.force_authenticate(user=self.user)
        url = reverse('post-detail', args=[self.post.id])
        data = {
            'title': 'Updated Post',
            'content': 'Updated content',
            'board': self.board.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.get(id=self.post.id).title, 'Updated Post')
    
    def test_post_permissions(self):
        """게시글 권한 테스트"""
        url = reverse('post-detail', args=[self.post.id])
        data = {
            'title': 'Trying to update',
            'content': 'Unauthorized update',
            'board': self.board.id
        }
        
        # 다른 사용자가 수정 시도
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # 게시물 삭제 시도
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # 작성자는 삭제 가능
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.filter(id=self.post.id).count(), 0)
    
    def test_create_anonymous_post(self):
        """익명 게시글 작성 테스트"""
        self.client.force_authenticate(user=self.user)
        url = reverse('post-list')
        data = {
            'title': '익명 게시글',
            'content': '익명으로 작성된 게시글입니다.',
            'board': self.board.id,
            'is_anon': True
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        # 게시글 조회 시 작성자 정보가 익명으로 표시되는지 확인
        post = Post.objects.get(title='익명 게시글')
        self.assertTrue(post.is_anon)
        
        # 게시글 목록 조회 시 익명 표시 확인
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        anonymous_post = next(p for p in response.data if p['title'] == '익명 게시글')
        self.assertTrue(anonymous_post['is_anon'])
        self.assertEqual(anonymous_post['author']['nickname'], '익명')
    
    def test_update_anonymous_post(self):
        """익명 게시글 수정 테스트"""
        # 익명 게시글 생성
        self.post.is_anon = True
        self.post.save()
        
        self.client.force_authenticate(user=self.user)
        url = reverse('post-detail', args=[self.post.id])
        data = {
            'title': '수정된 익명 게시글',
            'content': '수정된 익명 게시글 내용입니다.',
            'board': self.board.id,
            'is_anon': True
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # 수정 후에도 익명 상태 유지 확인
        self.post.refresh_from_db()
        self.assertTrue(self.post.is_anon)
        
        # 다른 사용자가 익명 게시글 수정 시도
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class CommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword',
            student_id='12345678',
            nickname='testname',
        )
        self.user2 = User.objects.create_user(
            username='testuser2', 
            email='test2@example.com', 
            password='testpassword',
            student_id='01234567',
            nickname='testname2',
        )
        
        self.board = Board.objects.create(
            name='Test Board',
            description='Board for testing'
        )
        
        self.post = Post.objects.create(
            title='Test Post',
            content='Test content',
            board=self.board,
            author=self.user
        )
        
        self.comment = Comment.objects.create(
            content='Test comment',
            post=self.post,
            author=self.user
        )
        
        self.client = APIClient()
    
    def test_add_comment(self):
        """댓글 추가 테스트"""
        self.client.force_authenticate(user=self.user)
        url = reverse('post-add-comment', args=[self.post.id])
        data = {
            'content': 'New comment'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Comment.objects.count(), 2)
        self.assertEqual(Comment.objects.filter(content='New comment').first().author, self.user)
    
    def test_add_reply(self):
        """대댓글 추가 테스트"""
        self.client.force_authenticate(user=self.user2)
        url = reverse('comment-reply', args=[self.comment.id])
        data = {
            'content': 'Reply to comment'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        reply = Comment.objects.get(content='Reply to comment')
        self.assertEqual(reply.parent, self.comment)
        self.assertEqual(reply.author, self.user2)
    
    def test_list_comments(self):
        """댓글 목록 조회 테스트"""
        url = reverse('comment-list')
        
        # 포스트 ID로 필터링
        response = self.client.get(f"{url}?post={self.post.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['content'], 'Test comment')
    
    def test_update_comment(self):
        """댓글 수정 테스트"""
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-detail', args=[self.comment.id])
        data = {
            'content': 'Updated comment',
            'post': self.post.id
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.get(id=self.comment.id).content, 'Updated comment')
    
    def test_delete_comment(self):
        """댓글 삭제 테스트"""
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-detail', args=[self.comment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Comment.objects.filter(id=self.comment.id).count(), 0)
    
    def test_comment_permissions(self):
        """댓글 권한 테스트"""
        url = reverse('comment-detail', args=[self.comment.id])
        data = {
            'content': 'Trying to update',
            'post': self.post.id
        }
        
        # 다른 사용자가 수정 시도
        self.client.force_authenticate(user=self.user2)
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostLikeTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com',
            nickname='테스트',
            student_id='20240001'
        )
        self.other_user = User.objects.create_user(
            username='otheruser',
            password='testpass123',
            email='other@example.com',
            nickname='다른사용자',
            student_id='20240002'
        )
        self.board = Board.objects.create(
            name='테스트 게시판',
            description='테스트용 게시판입니다.'
        )
        self.post = Post.objects.create(
            title='테스트 게시글',
            content='테스트 내용입니다.',
            author=self.user,
            board=self.board
        )
        self.client.force_authenticate(user=self.user)
    
    def test_like_post(self):
        """게시글 좋아요 테스트"""
        url = reverse('post-like', kwargs={'pk': self.post.pk})
        
        # 좋아요 추가
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], '좋아요가 추가되었습니다.')
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes, 1)
        
        # 좋아요 취소
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], '좋아요가 취소되었습니다.')
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes, 0)
    
    def test_get_likes(self):
        """게시글 좋아요 목록 조회 테스트"""
        # 좋아요 추가
        PostLike.objects.create(post=self.post, user=self.user)
        PostLike.objects.create(post=self.post, user=self.other_user)
        self.post.likes = 2
        self.post.save()
        
        url = reverse('post-likes', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes'], 2)
        self.assertEqual(len(response.data['liked_users']), 2)
        self.assertIn(self.user.username, response.data['liked_users'])
        self.assertIn(self.other_user.username, response.data['liked_users'])
    
    def test_like_anonymous_post(self):
        """익명 게시글 좋아요 테스트"""
        self.post.is_anon = True
        self.post.save()
        
        url = reverse('post-like', kwargs={'pk': self.post.pk})
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], '좋아요가 추가되었습니다.')
        self.post.refresh_from_db()
        self.assertEqual(self.post.likes, 1)
        
        # 좋아요 목록 조회 시 익명 게시글도 정상적으로 표시
        url = reverse('post-likes', kwargs={'pk': self.post.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['likes'], 1)
        self.assertEqual(len(response.data['liked_users']), 1)
        self.assertIn(self.user.username, response.data['liked_users'])