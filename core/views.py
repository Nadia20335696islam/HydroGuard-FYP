"""
Core views for the HydroGuard application.

This module defines the main entry points of the system, including:
- home page rendering
- dashboard rendering with dynamic user state handling
- goals and alerts integration
- gamification progress display

Enhancement:
The dashboard integrates both:
- the "Goals & Alerts" system
- the gamification system

Dashboard responsibilities now include:
- calculating today's water usage
- comparing usage against user-defined goals
- generating reminder, warning, and alert messages
- loading eco points, level, streaks, and earned badges
"""

# --------------------------------------------------
# DJANGO IMPORTS
# --------------------------------------------------
from django.shortcuts import render, redirect
from django.utils import timezone
from django.db.models import Sum

# --------------------------------------------------
# APPLICATION IMPORTS
# --------------------------------------------------
from accounts.models import User
from usage.models import WaterUsage
from goals.models import WaterGoal
from gamification.models import UserGameProfile, UserBadge

# --------------------------------------------------
# PYTHON IMPORTS
# --------------------------------------------------
from decimal import Decimal


# --------------------------------------------------
# DASHBOARD VIEW
# --------------------------------------------------
def dashboard(request):
    """
    Render the main dashboard.

    Responsibilities:
    - determine whether the visitor is authenticated or a guest
    - retrieve the logged-in user's profile data
    - calculate daily water usage
    - generate goal-based alerts
    - load gamification progress for display

    Context:
        user (User or None)
        is_guest (bool)
        reminder (str or None)
        warning (str or None)
        alert (str or None)
        game_profile (UserGameProfile or None)
        earned_badges (QuerySet)
    """

    # --------------------------------------------------
    # USER SESSION HANDLING
    # --------------------------------------------------
    user_id = request.session.get("user_id")
    is_guest = request.session.get("guest") is True

    # Redirect the visitor to login if there is no active
    # authenticated session and they are not using guest mode.
    if not user_id and not is_guest:
        return redirect("login")

    user = None
    reminder = None
    warning = None
    alert = None
    game_profile = None
    earned_badges = UserBadge.objects.none()

    # --------------------------------------------------
    # LOAD AUTHENTICATED USER DATA
    # --------------------------------------------------
    # If the session contains a valid user ID, load the user
    # and prepare their game profile and earned badges.
    if user_id:
        user = User.objects.get(id=user_id)

        # Ensure the logged-in user always has a game profile,
        # even if one was not created for any reason earlier.
        game_profile, _ = UserGameProfile.objects.get_or_create(user=user)

        # Load all badges earned by the current user so they can
        # be displayed on the dashboard.
        earned_badges = UserBadge.objects.filter(user=user).select_related("badge")

    # --------------------------------------------------
    # GOALS & ALERTS LOGIC (ONLY FOR AUTHENTICATED USERS)
    # --------------------------------------------------
    if user and not is_guest:

        today = timezone.now().date()

        # Fetch the user's first available goal record, if one exists.
        goal = WaterGoal.objects.filter(user=user).first()

        # Calculate the total amount of water used today.
        today_usage = (
            WaterUsage.objects.filter(user=user, usage_date=today)
            .aggregate(total=Sum("litres_used"))
            .get("total") or Decimal("0")
        )

        if goal:
            # --------------------------------------------------
            # REMINDER: NO USAGE RECORDED TODAY
            # --------------------------------------------------
            # Encourage the user to stay consistent with daily
            # tracking when reminders are enabled.
            if goal.reminders_enabled and today_usage == 0:
                reminder = "You have not logged any water usage today."

            # --------------------------------------------------
            # WARNING: USER IS APPROACHING DAILY LIMIT
            # --------------------------------------------------
            # Notify the user before they exceed their target.
            if goal.alerts_enabled and today_usage >= goal.warning_limit():
                warning = "You are close to your daily water limit."

            # --------------------------------------------------
            # ALERT: USER HAS EXCEEDED DAILY LIMIT
            # --------------------------------------------------
            # Display a stronger warning once the target has
            # been crossed.
            if goal.alerts_enabled and today_usage > goal.daily_target_litres:
                alert = "You have exceeded your daily water limit."

    # --------------------------------------------------
    # RENDER TEMPLATE
    # --------------------------------------------------
    # Send all dashboard, alert, and gamification data
    # to the template for display.
    return render(
        request,
        "core/dashboard.html",
        {
            "user": user,
            "is_guest": is_guest,
            "reminder": reminder,
            "warning": warning,
            "alert": alert,
            "game_profile": game_profile,
            "earned_badges": earned_badges,
        }
    )


# --------------------------------------------------
# HOME VIEW
# --------------------------------------------------
def home(request):
    """
    Render the landing page of the application.

    This page is accessible to all visitors and serves as
    the main public entry point to HydroGuard.
    """
    return render(request, "core/home.html")