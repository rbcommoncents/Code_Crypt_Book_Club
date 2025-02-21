from django.urls import reverse_lazy
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordResetView
from django.views.generic.edit import FormView
from django.views import View
from django.shortcuts import redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomPasswordResetForm


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
