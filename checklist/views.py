from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import ChecklistItem
from .serializers import ChecklistItemSerializer

class ChecklistView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = ChecklistItem.objects.filter(user=request.user)
        serializer = ChecklistItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request):
        item_name = request.data.get('item_name')
        status = request.data.get('status', False)

        item, created = ChecklistItem.objects.get_or_create(
            user=request.user, item_name=item_name,
            defaults={'status': status}
        )
        if not created:
            item.status = status
            item.save()

        return Response({'item_name': item_name, 'status': item.status})

    def patch(self, request, pk=None):
        try:
            item = ChecklistItem.objects.get(pk=pk, user=request.user)
        except ChecklistItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = ChecklistItemSerializer(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
            item = ChecklistItem.objects.get(pk=pk, user=request.user)
        except ChecklistItem.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
