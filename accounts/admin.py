from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, APIClient
from rest_framework.authtoken.models import Token

class APIClientInline(admin.StackedInline):
    model = APIClient
    extra = 0  

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_active", "phone_number", "profile_picture") 
    list_filter = ("is_staff", "is_active")  
    search_fields = ("email", "username")  
    ordering = ("email",) 
    inlines = [APIClientInline] 
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        ("Permissions", {"fields": ("is_staff", "is_active")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "username", "password1", "password2", "is_staff", "is_active", "phone_number", "profile_picture")}
        ),
    )

class APIClientAdmin(admin.ModelAdmin):
    model = APIClient
    list_display = ("user", "client_id", "token", "created_at")
    search_fields = ("user__email", "client_id", "token")
    readonly_fields = ("client_id", "token", "created_at") 

class TokenAdmin(admin.ModelAdmin):
    model = Token
    list_display = ("user", "key")
    search_fields = ("user__email", "key")

# Register Models
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(APIClient, APIClientAdmin)
admin.site.register(Token, TokenAdmin)
