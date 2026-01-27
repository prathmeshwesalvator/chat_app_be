from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken



def root(request):
        return Response({'message' : 'Welcome To The Auth Service'})



class AuthorizationAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'message': 'Token is missing or invalid'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = request.user
        return Response(
            {
                'message': 'User fetched successfully',
                'userId': user.id,
                'username': user.username,
                'email': user.email,
                'dateJoined': user.date_joined,
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username:
            return Response(
                {'message': 'Username is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {'message': 'Password is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = authenticate(username=username, password=password)

        if not user:
            return Response(
                {'message': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                'message': 'Login successful',
                'accessToken': str(refresh.access_token),
                'refreshToken': str(refresh),
            },
            status=status.HTTP_200_OK
        )







class SignUpAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')

        if not username or not password or not email:
            return Response(
                {'message': 'All fields are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'message': 'Username already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {'message': 'Email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return Response(
            {
                'message': 'User created successfully',
                'userId': user.id,
                'username': user.username,
                'email': user.email,
                'dateJoined': user.date_joined,
            },
            status=status.HTTP_201_CREATED
        )




class ValidationsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(
            {'message': 'User is authenticated'},
            status=status.HTTP_200_OK
        )
