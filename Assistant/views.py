from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from Assistant.core import process_user_input  # Import the updated function
from django.http import HttpResponse
from users.models.student import StudentProfile
from users.models.user import User  # Assuming you want to hardcode using a specific student

class NavigationView(APIView):
    def post(self, request):
        user_input = request.data.get('user_input', '').strip()
        username = request.data.get('username', '').strip()

        if not user_input or not username:
            return Response({"error": "Please provide both 'user_input' and 'username'."}, status=status.HTTP_400_BAD_REQUEST)

        result = process_user_input(user_input, username=username)
        return Response({"response": result}, status=status.HTTP_200_OK)



def Hello(request):
    return HttpResponse("Hello, world. You're at the polls index.")
