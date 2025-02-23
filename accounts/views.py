from .models import CustomUser, APIClient
from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetView
from django.views.generic.edit import FormView
from django.views import View
from rest_framework.permissions import IsAdminUser

from django.shortcuts import redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm
from rest_framework import generics, viewsets, permissions
from rest_framework.response import Response
from .serializers import AdminUserSerializer


class RegisterView(FormView):
    template_name = "accounts/register.html"
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("profile_view")

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "accounts/login.html"
    form_class = CustomAuthenticationForm
    success_url = reverse_lazy("landing")

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("landing")


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy("password_reset_done")
    template_name = "accounts/password_reset.html"


#// User API Configurations \\#

class AdminProfileView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminUserSerializer

    def get_object(self):
        return self.request.user

class RegenerateTokenView(generics.GenericAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminUserSerializer

    def post(self, request):
        api_client, created = APIClient.objects.get_or_create(user=request.user)
        api_client.regenerate_token()
        serializer = self.get_serializer(request.user)
        return redirect("profile_view")