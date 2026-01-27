from django.contrib import admin
from .models import Contact, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'contact_hash',
    )

    search_fields = (
        'user__username',
        'user__email',
    )

    ordering = ('id',)

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'owner',
        'contact_user',
        'created_at',
    )

    search_fields = (
        'owner__username',
        'contact_user__username',
        'contact_user__email',
    )

    list_filter = ('created_at',)
    ordering = ('-created_at',)
