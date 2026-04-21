"""
URL configuration for the gamification app.

This module defines routes related to HydroGuard's gamification system,
including:
- the gamification dashboard
- the endpoint used to save daily mini-game results
- the endpoint used to save daily mission completions
"""

from django.urls import path
from . import views

# --------------------------------------------------
# APP NAMESPACE
# --------------------------------------------------
app_name = "gamification"

urlpatterns = [
    # Dedicated gamification dashboard
    path("", views.gamification_dashboard, name="gamification_dashboard"),

    # Endpoint used by the mini game to submit results
    path("save-result/", views.save_game_result, name="save_game_result"),

    # Endpoint used by daily missions to submit completion
    path("complete-mission/", views.complete_daily_mission, name="complete_daily_mission"),
]