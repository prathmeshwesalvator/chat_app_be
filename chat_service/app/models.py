from django.db import models

class Contact(models.Model):
    
    user_id = models.UUIDField()      
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.email}"

    class Meta:
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ['name']
