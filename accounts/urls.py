from django.urls import path
from . import views

# --------------------------------------------------
# APP NAMESPACE (IMPORTANT FOR CLEAN URL REFERENCING)
# --------------------------------------------------
app_name = "accounts"

urlpatterns = [
    # User registration page
    path("register/", views.register, name="register"),

    # User login page
    path("login/", views.login_view, name="login"),

    # Logout action
    path("logout/", views.logout_view, name="logout"),

    # Guest login
    path("guest/", views.guest_login, name="guest_login"),

    # Password recovery
    path("forgot-password/", views.forgot_password, name="forgot_password"),
]