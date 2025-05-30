from rest_framework import serializers
from .models import User

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

