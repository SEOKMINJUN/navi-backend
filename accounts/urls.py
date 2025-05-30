from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import SignupView, ResetPasswordView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),                   # 회원가입
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), # 로그인 (JWT)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),# 액세스토큰 갱신
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'), # 비밀번호 재설정
]