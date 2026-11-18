from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated
from acc.permissions import ADorReadO


class Reg(APIView):
    def post(self, request):
        serializer = RegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            return Response({"errors": serializer.errors},status=400)
        
class Profile(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)            