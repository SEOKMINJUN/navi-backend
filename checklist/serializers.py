
from rest_framework import serializers
from .models import ChecklistItem

class ChecklistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChecklistItem
        fields = ['item_name', 'status']