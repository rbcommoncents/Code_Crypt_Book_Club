from django.urls import path
from .views import RegisterView, LoginView, LogoutView, CustomPasswordResetView, AdminProfileView, RegenerateTokenView
from django.contrib.auth import views as auth_views
from allauth.account.views import ConfirmEmailView
from rest_framework.routers import SimpleRouter




urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_done.html"), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    path("account-confirm-email/<key>", ConfirmEmailView.as_view(), name="account_confirm_email"),
    path("profile/", AdminProfileView.as_view(), name="admin_profile"),
    path("profile/regenerate-token/", RegenerateTokenView.as_view(), name="regenerate_token"),
]
