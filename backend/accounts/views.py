from rest_framework import generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import (
    api_view,
    permission_classes



    )
from rest_framework.response import Response
from .serializers import RegisterSerializer

# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_test(request):
    return Response({
        "message":"authentication successful",
        "username":request.user.username


        })

