from django.urls import path
from .views import * 
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('' ,  root, name='auth_service'),
    path('token/' , AuthorizationAPIView.as_view() , name='auth'),
    path('token/refresh/' , TokenRefreshView.as_view() , name='refresh_token'),
    path('me/' , AuthorizationAPIView.as_view() , name = 'me'),
    path('check/' , ValidationsAPIView.as_view() , name = 'token_check'),
    path('signup/' , SignUpAPIView.as_view() , name='signup'),
    path('contacts/' , ContactAPIView.as_view() , name='contacts'),
    path('qr-code/' , QRCodeAPIView.as_view() , name='qr_code'),
    path('send-otp/' , SendOtpAPIView.as_view() , name='send_otp'),
    path('verify-otp/' , VerifyOtpAPIView.as_view() , name='verify_otp'),
]
