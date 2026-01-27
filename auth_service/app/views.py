from django.http import JsonResponse
from django.contrib.auth import authenticate , login
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny , IsAuthenticated 
from rest_framework import status 
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User

def root(request):
        return JsonResponse({'message' : 'Welcome To The Auth Service'})



class AuthorizationAPIView(APIView):
        
        permission_classes = [AllowAny]

        def get(self , request):
                
                try : 
                        if not request.user:
                                return JsonResponse({'message' : 'token is unavailable'} , status = status.HTTP_401_UNAUTHORIZED)
                        
                        user = request.user

                        return JsonResponse(
                                {
                                        'message' : 'User fetched successfully',
                                        'userId' : user.pk,
                                        'username' : user.username,
                                        'email' : user.email,
                                        'dateJoined' : user.date_joined,
                                })
                
                except Exception as e:
                        
                        return JsonResponse({'message' : f'{e}'})

                        
        def post(self , request):
                try:
                        data = request.data
                        username = data.get('username')
                        password = data.get('password')

                        if not username:
                                return JsonResponse({'message' : 'Username is required'} , status = status.HTTP_400_BAD_REQUEST)
                        
                        if not password:
                                return JsonResponse({'message' : 'Password is required'} , status = status.HTTP_400_BAD_REQUEST)
                        
                        user = authenticate(request=request, username = username , password = password)

                        

                        if not user :
                                return JsonResponse({'message' : 'Invalid CRedentials'} , status = status.HTTP_401_UNAUTHORIZED)
                        
                        refresh = RefreshToken.for_user(user=user)

                        return JsonResponse(
                                {
                                  'message' : 'Login Successful' ,
                                  'accessToken' : str(refresh.access_token),
                                  'refreshToken' : str(refresh)
                                 } , status = status.HTTP_200_OK) 
                                
                
                except Exception as e:
                        
                        return JsonResponse({'message' : f'An error occured, {str(e)}'} , status = status.HTTP_200_OK)


class SignUpAPIView(APIView):
        permission_classes = [AllowAny]
        def post(self , request):
                    
                    try:
                        data = request.data
                        username = data.get('username')
                        password =data.get('password')
                        email = data.get('email')


                        if not username and not password and not email:
                                return JsonResponse({'message': 'Enter all details'} , status = status.HTTP_400_BAD_REQUEST)
                        
                        
                        if User.objects.filter(username = username).exists() : 
                                return JsonResponse({'message' : 'Username is already exists' }, status = status.HTTP_400_BAD_REQUEST)

                        if User.objects.filter(email = email).exists():
                                return JsonResponse({'message' : 'Email already exists'} , status = status.HTTP_400_BAD_REQUEST) 
                        
                        user = User.objects.create_user(
                                username=username , 
                                email=email,
                                password=password
                        )

                        return JsonResponse(
                                {
                                        'message' : 'User created successfully',
                                        'userId' : user.pk,
                                        'username' : user.username,
                                        'email' : user.email,
                                        'dateJoined' : user.date_joined,
                                } , status = status.HTTP_201_CREATED)
                    except Exception as e:
                            
                            return JsonResponse({'message' : f'An error occurred {str(e)}'})




class ValidationsAPIView (APIView) :
        permission_classes = [IsAuthenticated]

        def get( self , request):
                return JsonResponse({'message' : 'user is authenticated'} , status = status.HTTP_200_OK)