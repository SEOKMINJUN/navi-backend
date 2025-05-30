from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class UserSignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'nickname', 'student_id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            nickname=validated_data['nickname'],
            student_id=validated_data['student_id'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        
        # 토큰에 추가 정보 포함
        token['username'] = user.username
        token['email'] = user.email
        token['student_id'] = user.student_id
        token['nickname'] = user.nickname
        
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)
        
        # 토큰 발급 시 추가 정보 포함
        data['username'] = self.user.username
        data['email'] = self.user.email
        data['student_id'] = self.user.student_id
        data['nickname'] = self.user.nickname
        
        return data

