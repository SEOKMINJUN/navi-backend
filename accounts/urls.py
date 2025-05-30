from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import SignupView, ResetPasswordView, CustomTokenObtainPairView, PasswordResetRequestView

urlpatterns = [
    path('signup/', SignupView.as_view(), name='signup'),                   # 회원가입
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'), # 로그인 (JWT)
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),# 액세스토큰 갱신
    path('reset-password/', ResetPasswordView.as_view(), name='reset_password'), # 비밀번호 재설정
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password_reset_request'),
]