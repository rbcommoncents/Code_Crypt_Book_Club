from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ["email", "username", "is_staff", "is_active"]
    search_fields = ["email", "username"]
    ordering = ["email"]

    fieldsets = (
        (None, {"fields": ("email", "password", "username", "phone_number", "profile_picture")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
