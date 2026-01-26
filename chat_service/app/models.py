from django.db import models

class Contact(models.Model):
    user_id = models.UUIDField()
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        ordering = ['-created_at']
