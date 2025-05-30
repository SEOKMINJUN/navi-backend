from django.db import models
from accounts.models import User
from django.conf import settings

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=100, verbose_name='게시판 이름')
    description = models.TextField(verbose_name='게시판 설명')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')

    class Meta:
        verbose_name = '게시판'
        verbose_name_plural = '게시판'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name='제목')
    content = models.TextField(verbose_name='내용')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='작성자')
    board = models.ForeignKey(Board, on_delete=models.CASCADE, verbose_name='게시판')
    is_anon = models.BooleanField(default=False, verbose_name='익명 여부')
    likes = models.PositiveIntegerField(default=0, verbose_name='좋아요 수')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='작성일')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='수정일')
    view_count = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = '게시글'
        verbose_name_plural = '게시글'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class PostLike(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='liked_post', verbose_name='게시글')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='사용자')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='생성일')

    class Meta:
        verbose_name = '게시글 좋아요'
        verbose_name_plural = '게시글 좋아요'
        unique_together = ['post', 'user']  # 한 사용자는 한 게시글에 한 번만 좋아요 가능

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"

class Comment(models.Model):
    content = models.TextField()
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        if self.is_deleted:
            return "삭제된 댓글"
        return f"Comment by {self.author.username} on {self.post.title}"

    def delete(self, *args, **kwargs):
        if self.replies.exists():
            self.is_deleted = True
            self.content = "삭제된 댓글입니다."
            self.save()
        else:
            super().delete(*args, **kwargs)