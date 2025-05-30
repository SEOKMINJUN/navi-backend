from rest_framework import serializers
from accounts.serializers import UserSignupSerializer
from .models import Schedule

class ScheduleSerializer(serializers.ModelSerializer):
    user = UserSignupSerializer(read_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    
    class Meta:
        model = Schedule
        fields = ['id', 'title', 'description', 'start_time', 'end_time', 
                  'created_at', 'updated_at', 'user', 'user_id']
    
    def create(self, validated_data):
        user_id = validated_data.pop('user_id', None)
        if user_id is None and self.context.get('request'):
            user_id = self.context['request'].user.id
        
        schedule = Schedule.objects.create(**validated_data)
        
        if user_id:
            schedule.user_id = user_id
            schedule.save()
        
        return schedule

    def update(self, schedule, validated_data):
        # user_id는 업데이트에서 제외
        validated_data.pop('user_id', None)
        
        # 각 필드를 개별적으로 업데이트
        for attr, value in validated_data.items():
            setattr(schedule, attr, value)
        
        schedule.save()
        return schedule