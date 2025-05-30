from rest_framework import serializers
from accounts.serializers import UserSignupSerializer
from .models import Board, Post, Comment

class CommentSerializer(serializers.ModelSerializer):
    author = UserSignupSerializer(read_only=True)
    author_username = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'author', 'author_username', 'parent', 
                 'created_at', 'updated_at', 'replies']
        read_only_fields = ['author']
    
    def get_author_username(self, obj):
        return obj.author.username
    
    def get_replies(self, obj):
        if not hasattr(obj, 'replies'):
            return []
        return CommentSerializer(obj.replies.all(), many=True, context=self.context).data
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostListSerializer(serializers.ModelSerializer):
    author = UserSignupSerializer(read_only=True)
    author_username = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'board', 'author', 'author_username', 
                 'created_at', 'updated_at', 'view_count', 'comment_count']
        read_only_fields = ['author', 'view_count']
    
    def get_author_username(self, obj):
        return obj.author.username
    
    def get_comment_count(self, obj):
        return obj.comments.count()

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSignupSerializer(read_only=True)
    author_username = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    board_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'board', 'board_name', 'author', 
                 'author_username', 'created_at', 'updated_at', 
                 'view_count', 'comments']
        read_only_fields = ['author', 'view_count']
    
    def get_author_username(self, obj):
        return obj.author.username
    
    def get_board_name(self, obj):
        return obj.board.name
    
    def get_comments(self, obj):
        # 최상위 댓글만 가져오기 (대댓글은 replies로 처리)
        comments = obj.comments.filter(parent=None)
        return CommentSerializer(comments, many=True, context=self.context).data
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class BoardSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'post_count']
    
    def get_post_count(self, obj):
        return obj.posts.count()