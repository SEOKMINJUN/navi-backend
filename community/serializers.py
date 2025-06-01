from rest_framework import serializers
from accounts.serializers import UserSignupSerializer
from .models import Board, Post, Comment, PostLike

class CommentSerializer(serializers.ModelSerializer):
    author = UserSignupSerializer(read_only=True)
    author_username = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'author', 'author_username', 'parent', 
                 'created_at', 'updated_at', 'replies', 'is_deleted']
        read_only_fields = ['author', 'is_deleted']
    
    def get_author_username(self, obj):
        if obj.is_deleted:
            return "삭제된 댓글"
        return obj.author.username
    
    def get_replies(self, obj):
        if obj.parent is None:  # 부모 댓글인 경우에만 답글을 가져옴
            replies = Comment.objects.filter(parent=obj)
            return CommentSerializer(replies, many=True).data
        return []
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_deleted:
            data['content'] = "삭제된 댓글입니다."
            data['author'] = {
                'id': None,
                'username': '삭제된 사용자',
                'nickname': '삭제된 사용자',
                'email': None,
                'student_id': None
            }
        return data
    
    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)

class PostListSerializer(serializers.ModelSerializer):
    author = UserSignupSerializer(read_only=True)
    author_username = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    content = serializers.CharField(read_only=True)
    likes = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'board', 'author', 'author_username',
                  'created_at', 'updated_at', 'view_count', 'comment_count',
                  'is_anon', 'likes']
        read_only_fields = ['author', 'view_count']

    def get_author_username(self, obj):
        return obj.author.username

    def get_comment_count(self, obj):
        return obj.comments.count()

    def get_likes(self, obj):
        return obj.liked_post.count()

    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_anon:
            data['author'] = {
                'id': None,
                'username': '익명',
                'nickname': '익명',
                'email': None,
                'student_id': None
            }
        return data

class PostDetailSerializer(serializers.ModelSerializer):
    author = UserSignupSerializer(read_only=True)
    author_username = serializers.SerializerMethodField()
    comments = serializers.SerializerMethodField()
    board_name = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    likes = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'board', 'board_name', 'author', 
                 'author_username', 'created_at', 'updated_at', 
                 'view_count', 'comments', 'is_liked', 'likes', 'is_anon']
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
    
    def get_is_liked(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=request.user).exists()
        return False
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if instance.is_anon:
            data['author'] = {
                'id': None,
                'username': '익명',
                'nickname': '익명',
                'email': None,
                'student_id': None
            }
        return data


class BoardSerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Board
        fields = ['id', 'name', 'description', 'created_at', 'updated_at', 'post_count']
    
    def get_post_count(self, obj):
        return Post.objects.filter(board=obj).count()
