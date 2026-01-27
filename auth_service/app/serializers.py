from rest_framework import serializers
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
