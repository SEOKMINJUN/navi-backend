from django.contrib import admin
from .models import Schedule

@admin.register(Schedule)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'user')
    list_filter = ('start_time', 'end_time', 'user')
    search_fields = ('title', 'description')