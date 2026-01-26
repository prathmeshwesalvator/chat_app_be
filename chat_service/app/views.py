from django.http import JsonResponse
from rest_framework.views import APIView

from chat_app_be.chat_service.app.models import Contact


def root(request):
    return JsonResponse({
        'message' : 'WELCOME TO THE CHAT SERVICE'
    })


class ChatAPIView(APIView):

    def get(self , request):

        try:

            contacts = Contact.objects.all()
        
        except Exception as e:
            return JsonResponse({
                'error' : str(e)
            } , status=500)
        