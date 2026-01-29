from time import timezone
from django.db import models
from django.contrib.auth.models import User
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    contact_hash = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        unique=True,
        null=True,
        blank=True
    )

    contact_hash_created_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def is_qr_expired(self):
        if not self.contact_hash_created_at:
            return True
        return timezone.now() > self.contact_hash_created_at + timezone.timedelta(minutes=5)

    def __str__(self):
        return f"{self.user.username}'s Profile"


class Contact(models.Model):
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contacts'
    )
    contact_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='saved_as_contact'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('owner', 'contact_user')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.owner.username} → {self.contact_user.username}"
