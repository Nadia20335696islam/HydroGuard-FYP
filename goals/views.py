"""
Views for the goals app.

This module implements the "Goals & Alerts" feature of HydroGuard.

It provides functionality for:
- creating and updating user-specific water-saving goals
- calculating daily water usage progress
- generating intelligent reminders, warnings, and alerts
  based on real-time usage data

The system integrates with:
- a custom session-based authentication mechanism
- the WaterUsage model from the usage app
"""

# --------------------------------------------------
# DJANGO IMPORTS
# --------------------------------------------------
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum

# --------------------------------------------------
# PYTHON STANDARD LIBRARY IMPORTS
# --------------------------------------------------
from decimal import Decimal

# --------------------------------------------------
# LOCAL APPLICATION IMPORTS
# --------------------------------------------------
from .forms import WaterGoalForm
from .models import WaterGoal
from usage.models import WaterUsage


# --------------------------------------------------
# HELPER FUNCTIONS
# --------------------------------------------------
def get_current_user(request):
    """
    Retrieve the currently authenticated user using session data.

    Returns:
        User: The logged-in user instance.

    Raises:
        Http404: If no valid user is found in the session.
    """
    from accounts.models import User

    user_id = request.session.get("user_id")
    return get_object_or_404(User, id=user_id)


# --------------------------------------------------
# GOAL SETTINGS VIEW
# --------------------------------------------------
def goal_settings(request):
    """
    Handle creation and updating of a user's water-saving goal.

    Behaviour:
    - Restricts access to authenticated users only
    - Automatically creates a default goal if none exists
    - Processes form submission for updating goal settings
    - Displays existing goal values in the form

    Context:
        form (WaterGoalForm): Bound form instance
        goal (WaterGoal): Current user's goal object
    """

    # --------------------------------------------------
    # ACCESS CONTROL
    # --------------------------------------------------
    if not request.session.get("user_id"):
        messages.error(request, "Please log in to access goal settings.")
        return redirect("login")

    # Retrieve current user
    user = get_current_user(request)

    # --------------------------------------------------
    # FETCH OR INITIALISE USER GOAL
    # --------------------------------------------------
    goal, created = WaterGoal.objects.get_or_create(
        user=user,
        defaults={
            "daily_target_litres": 100,
            "warning_percentage": 80,
            "reminders_enabled": True,
            "alerts_enabled": True,
        }
    )

    # --------------------------------------------------
    # HANDLE FORM SUBMISSION
    # --------------------------------------------------
    if request.method == "POST":
        form = WaterGoalForm(request.POST, instance=goal)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Your water-saving goal has been updated successfully."
            )

            return redirect("goal_settings")

    else:
        form = WaterGoalForm(instance=goal)

    # --------------------------------------------------
    # RENDER TEMPLATE
    # --------------------------------------------------
    return render(
        request,
        "goals/goal_settings.html",
        {
            "form": form,
            "goal": goal,
        }
    )


# --------------------------------------------------
# GOAL DASHBOARD VIEW (ALERT ENGINE)
# --------------------------------------------------
def goal_dashboard(request):
    """
    Display the user's daily water usage progress and generate alerts.

    This view performs:
    - aggregation of today's water usage
    - comparison against the user's defined goal
    - generation of contextual feedback messages:
        • Reminder → no usage logged
        • Warning → approaching target threshold
        • Alert → target exceeded

    Context:
        goal (WaterGoal): User's goal configuration
        today_usage (Decimal): Total litres used today
        progress_percentage (float): Percentage of goal used
        reminder (str): Reminder message (if applicable)
        warning (str): Warning message (if applicable)
        alert (str): Alert message (if applicable)
        today (date): Current date
    """

    # --------------------------------------------------
    # ACCESS CONTROL
    # --------------------------------------------------
    if not request.session.get("user_id"):
        messages.error(request, "Please log in to access goals dashboard.")
        return redirect("login")

    user = get_current_user(request)
    today = timezone.localdate()

    # --------------------------------------------------
    # FETCH USER GOAL
    # --------------------------------------------------
    goal = WaterGoal.objects.filter(user=user).first()

    # --------------------------------------------------
    # CALCULATE TODAY'S USAGE
    # --------------------------------------------------
    today_usage = (
        WaterUsage.objects.filter(user=user, usage_date=today)
        .aggregate(total=Sum("litres_used"))
        .get("total") or Decimal("0")
    )

    # --------------------------------------------------
    # INITIALISE FEEDBACK VARIABLES
    # --------------------------------------------------
    progress_percentage = 0
    reminder = None
    warning = None
    alert = None

    # --------------------------------------------------
    # ALERT LOGIC ENGINE
    # --------------------------------------------------
    if goal:
        # Calculate progress percentage safely
        if goal.daily_target_litres > 0:
            progress_percentage = round(
                (today_usage / goal.daily_target_litres) * 100, 2
            )

        # Reminder: no usage logged
        if goal.reminders_enabled and today_usage == 0:
            reminder = "You have not logged any water usage today."

        # Warning: approaching threshold
        if goal.alerts_enabled and today_usage >= goal.warning_limit():
            warning = "You are close to reaching your daily water target."

        # Alert: exceeded goal
        if goal.alerts_enabled and today_usage > goal.daily_target_litres:
            alert = "You have exceeded your daily water target."

    # --------------------------------------------------
    # RENDER DASHBOARD
    # --------------------------------------------------
    return render(
        request,
        "goals/goal_dashboard.html",
        {
            "goal": goal,
            "today_usage": today_usage,
            "progress_percentage": progress_percentage,
            "reminder": reminder,
            "warning": warning,
            "alert": alert,
            "today": today,
        }
    )