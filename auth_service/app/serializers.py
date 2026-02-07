from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    contact_user_id = serializers.IntegerField(
        source='contact_user.id',
        read_only=True
    )
    contact_username = serializers.CharField(
        source='contact_user.username',
        read_only=True
    )
    contact_email = serializers.EmailField(
        source='contact_user.email',
        read_only=True
    )

    class Meta:
        model = Contact
        fields = [
            'id',
            'contact_user_id',
            'contact_username',
            'contact_email',
            'created_at',
        ]



class ContactUserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()