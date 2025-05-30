from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSignupSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

# #회원가입 뷰

class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': '회원가입 성공'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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