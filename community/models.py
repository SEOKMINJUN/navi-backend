from django.db import models
from accounts.models import User

# Create your models here.
class Board(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='posts')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

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