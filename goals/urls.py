"""
URL configuration for the goals app.
"""

from django.urls import path
from . import views


urlpatterns = [
    path("", views.goal_dashboard, name="goal_dashboard"),  # NEW
    path("settings/", views.goal_settings, name="goal_settings"),
]