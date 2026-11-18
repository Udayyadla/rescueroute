from rest_framework import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Create your views here.

class DonationCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({
            "message":"Donation created successfully"})
