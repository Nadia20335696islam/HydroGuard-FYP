from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("guest/", views.guest_login, name="guest_login"),
    path("forgot-password/", views.forgot_password, name="forgot_password"),
]
