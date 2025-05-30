from django.urls import path
from .views import ChecklistView

urlpatterns = [
    path('checklist/', ChecklistView.as_view(), name='checklist'),
    path('checklist/<int:pk>/', ChecklistView.as_view(), name='checklist-detail'),
]