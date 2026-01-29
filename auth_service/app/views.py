from django.utils import timezone
import uuid
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError , transaction
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
import pytz
from app.models import Contact, UserProfile
from app.serializers import ContactSerializer



def root(request):
        return JsonResponse({'message' : 'Welcome To The Auth Service'})



class AuthorizationAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {'message': 'Token is missing or invalid'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        user = request.user
        user_profile = UserProfile.objects.get(user=user)
        return Response(
            {
                'message': 'User fetched successfully',
                'userId': user.id,
                'username': user.username,
                'email': user.email,
                'dateJoined': user.date_joined,
                'bio': user_profile.bio,
                'avatar': user_profile.avatar.url if user_profile.avatar else None,
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


class ContactAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        contacts = (
            Contact.objects
            .filter(owner=request.user)
            .select_related('contact_user')
        )

        serializer = ContactSerializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    def post(self, request):
        contact_user_id = request.data.get('contact_user_id')
        contact_hash = request.data.get('contact_hash')

        if not contact_user_id and not contact_hash:
            return Response(
                {'message': 'contact_user_id or contact_hash is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            # 🔹 Add via user ID
            if contact_user_id:
                contact_user = UserProfile.objects.get(id=contact_user_id).user

            # 🔹 Add via QR hash
            else:
                qr_profile = (
                    UserProfile.objects
                    .select_related('user')
                    .get(contact_hash=contact_hash)
                )

                # 🚫 Reject expired QR
                if qr_profile.is_qr_expired():
                    # Optional: invalidate QR immediately
                    qr_profile.contact_hash = None
                    qr_profile.contact_hash_created_at = None
                    qr_profile.save(update_fields=[
                        'contact_hash',
                        'contact_hash_created_at'
                    ])

                    return Response(
                        {'message': 'QR code has expired'},
                        status=status.HTTP_410_GONE
                    )

                contact_user = qr_profile.user

            # 🚫 Prevent adding self
            if contact_user == request.user:
                return Response(
                    {'message': 'You cannot add yourself as a contact'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # ✅ Create contact if not exists
            contact, created = Contact.objects.get_or_create(
                owner=request.user,
                contact_user=contact_user
            )

            if not created:
                return Response(
                    {'message': 'Contact already exists'},
                    status=status.HTTP_409_CONFLICT
                )

            serializer = ContactSerializer(contact)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except UserProfile.DoesNotExist:
            return Response(
                {'message': 'User not found or invalid QR code'},
                status=status.HTTP_404_NOT_FOUND
            )
        except IntegrityError:
            return Response(
                {'message': 'Contact already exists'},
                status=status.HTTP_409_CONFLICT
            )


        
    def delete(self, request):
        contact_user_id = request.query_params.get('contact_user_id')

        if not contact_user_id:
            return Response(
                {'message': 'contact_user_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            contact = Contact.objects.get(
                owner=request.user,
                contact_user_id=contact_user_id
            )

            contact.delete()
            return Response(
                {'message': 'Contact deleted successfully'},
                status=status.HTTP_200_OK
            )

        except Contact.DoesNotExist:
            return Response(
                {'message': 'Contact not found'},
                status=status.HTTP_404_NOT_FOUND
            )


class QRCodeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = UserProfile.objects.select_for_update().get(user=request.user)

        with transaction.atomic():
            profile.contact_hash = uuid.uuid4()
            profile.contact_hash_created_at = timezone.now()
            profile.save()

        ist_tz = pytz.timezone("Asia/Kolkata")
        created_at_ist = timezone.localtime(
            profile.contact_hash_created_at,
            ist_tz
        )

        return Response(
            {
                "message": "New QR code generated",
                "contactHash": str(profile.contact_hash),
                "expiresInMinutes": "5",
                "createdAt": created_at_ist
            },
            status=status.HTTP_200_OK)