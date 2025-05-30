from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from .serializers import UserSignupSerializer, CustomTokenObtainPairSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

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