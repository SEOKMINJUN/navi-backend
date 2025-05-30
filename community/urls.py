from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BoardViewSet, PostViewSet, CommentViewSet
comunityRouter = DefaultRouter()
comunityRouter.register(r'boards', BoardViewSet)
comunityRouter.register(r'posts', PostViewSet, basename='post')
comunityRouter.register(r'comments', CommentViewSet, basename='comment')

urlpatterns = [
    path('community/', include(comunityRouter.urls)),
]