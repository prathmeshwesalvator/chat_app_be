from django.http import JsonResponse
from rest_framework.views import APIView

from app.models import Contact
from utils.auth_verification import authVerification


def root(request):
    return JsonResponse({
        'message' : 'WELCOME TO THE CHAT SERVICE'
    })


class ChatAPIView(APIView):

    def get(self , request):

        try:

            authVerification()

            contacts = Contact.objects.all()
        
        except Exception as e:
            return JsonResponse({
                'error' : str(e)
            } , status=500)
        
