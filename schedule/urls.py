from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ScheduleViewSet
scheduleRouter = DefaultRouter()
scheduleRouter.register(r'schedule', ScheduleViewSet, basename='schedule')

urlpatterns = [
    path('', include(scheduleRouter.urls)),
]