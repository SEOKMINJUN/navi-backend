from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSignupSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
import random
import string
import logging

User = get_user_model()

logger = logging.getLogger(__name__)

# #회원가입 뷰

class SignupView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                "message": "아이디와 비밀번호를 모두 입력해주세요."
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        
        if user is None:
            return Response({
                "message": "아이디 또는 비밀번호가 올바르지 않습니다."
            }, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "로그인 성공",
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "user": {
                "username": user.username,
                "email": user.email,
                "student_id": user.student_id,
                "nickname": user.nickname
            }
        }, status=status.HTTP_200_OK)

# # 비밀번호 재설정 뷰

class ResetPasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 관리자인 경우
        if request.user.is_staff:
            username = request.data.get('username')
            new_password = request.data.get('new_password')
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({'message': '일치하는 사용자가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        
        # 일반 사용자인 경우
        else:
            current_password = request.data.get('current_password')
            new_password = request.data.get('new_password')
            
            # 현재 비밀번호 확인
            if not request.user.check_password(current_password):
                return Response({'message': '현재 비밀번호가 일치하지 않습니다.'}, status=status.HTTP_400_BAD_REQUEST)
            
            # 새 비밀번호로 변경
            request.user.set_password(new_password)
            request.user.save()
            return Response({'message': '비밀번호가 성공적으로 변경되었습니다.'}, status=status.HTTP_200_OK)

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': '이메일을 입력해주세요.'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'error': '해당 이메일로 등록된 사용자가 없습니다.'}, status=404)

        # 임시 비밀번호 생성 (8자리)
        temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
        
        # 사용자 비밀번호 변경
        user.set_password(temp_password)
        user.save()

        # 이메일 전송
        subject = '[Navi] 비밀번호 초기화 안내'
        message = f'''
안녕하세요, {user.nickname}님.

요청하신 비밀번호 초기화가 완료되었습니다.
임시 비밀번호는 다음과 같습니다:

{temp_password}

보안을 위해 로그인 후 반드시 비밀번호를 변경해주세요.

감사합니다.
Navi 팀
'''
        try:
            # 이메일 전송 시도
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
            
            # 로그 기록
            logger.info(f'비밀번호 초기화 이메일 전송 성공: {email}')
            
            return Response({
                'message': '임시 비밀번호가 이메일로 전송되었습니다.',
                'temp_password': temp_password  # 개발 환경에서만 임시 비밀번호 반환
            }, status=200)
            
        except Exception as e:
            # 에러 로그 기록
            logger.error(f'비밀번호 초기화 이메일 전송 실패: {str(e)}')
            return Response({
                'error': '이메일 전송에 실패했습니다.',
                'temp_password': temp_password  # 개발 환경에서만 임시 비밀번호 반환
            }, status=500)
        # Use this on production
        # # 이메일 전송 시도
        #     send_mail(
        #         subject=subject,
        #         message=message,
        #         from_email=settings.DEFAULT_FROM_EMAIL,
        #         recipient_list=[email],
        #         fail_silently=False,
        #     )
            
        #     # 로그 기록
        #     logger.info(f'비밀번호 초기화 이메일 전송 성공: {email}')
            
        #     return Response({
        #         'message': '임시 비밀번호가 이메일로 전송되었습니다.',
        #         'temp_password': temp_password  # 개발 환경에서만 임시 비밀번호 반환
        #     }, status=200)
            
        # except Exception as e:
        #     # 에러 로그 기록
        #     logger.error(f'비밀번호 초기화 이메일 전송 실패: {str(e)}')
        #     return Response({
        #         'error': '이메일 전송에 실패했습니다.',
        #         'temp_password': temp_password  # 개발 환경에서만 임시 비밀번호 반환
        #     }, status=500)