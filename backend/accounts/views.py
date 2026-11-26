from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializers import CurrentUserSerializer, LogoutSerializer, RegisterSerializer

# Create your views here.


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    authentication_classes = []


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def protected_test(request):
    return Response(
        {"message": "authentication successful", "username": request.user.username}
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    serializer = CurrentUserSerializer(request.user)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_user(request):
    serializer = LogoutSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    token_user_id = serializer.token.payload.get("user_id")

    if str(token_user_id) != str(request.user.pk):
        return Response(
            {"message": "Refresh token does not belong to this user."},
            status=status.HTTP_403_FORBIDDEN,
        )

    serializer.save()
    return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
