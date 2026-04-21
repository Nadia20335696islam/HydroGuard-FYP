"""
Views for the usage app.

This module contains view functions related to water usage features
within the HydroGuard system.

It currently supports:
- creating new water usage records
- retrieving and displaying a user's personal usage history
- preparing chart-ready and summary data for the history page
"""

import json
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Sum, Avg
from accounts.models import User
from .forms import WaterUsageForm
from .models import WaterUsage


# --------------------------------------------------
# WATER USAGE CREATION VIEW
# --------------------------------------------------
def add_usage(request):
    """
    Handle the creation of a new water usage record.

    This view:
    - verifies whether the user is authenticated via session
    - displays the water usage form
    - validates submitted input data
    - attaches the logged-in user to the record
    - saves the record to the database
    - provides a success message for user feedback
    """

    # Retrieve the logged-in user's ID from the session
    user_id = request.session.get("user_id")

    # Prevent unauthenticated access
    if not user_id:
        return redirect("/accounts/login/")

    # Retrieve the current user safely
    user = get_object_or_404(User, id=user_id)

    # Handle form submission
    if request.method == "POST":
        form = WaterUsageForm(request.POST)

        if form.is_valid():
            # Create object without saving immediately
            usage = form.save(commit=False)

            # Associate the record with the logged-in user
            usage.user = user

            # Save to database
            usage.save()

            # Provide detailed success feedback
            messages.success(
                request,
                f"You logged {usage.litres_used}L for "
                f"{usage.get_activity_display()} on "
                f"{usage.usage_date.strftime('%d %B %Y')}."
            )

            return redirect("/dashboard/")

    else:
        # Initialise an empty form for GET request
        form = WaterUsageForm()

    return render(request, "usage/add_usage.html", {
        "form": form,
        "user": user
    })


# --------------------------------------------------
# VIEW USAGE HISTORY
# --------------------------------------------------
def usage_history(request):
    """
    Display the logged-in user's water usage history.

    This view:
    - ensures the user is authenticated via session
    - retrieves all water usage records belonging to that user
    - orders records from newest to oldest
    - prepares summary statistics for dashboard-style display
    - prepares aggregated chart data grouped by date

    The template can use this data to present:
    - summary cards
    - a cleaner, more professional chart
    - a detailed table of records
    """

    # Retrieve the logged-in user's ID from session
    user_id = request.session.get("user_id")

    # Prevent unauthenticated access
    if not user_id:
        return redirect("/accounts/login/")

    # Retrieve the current user
    user = get_object_or_404(User, id=user_id)

    # Retrieve only this user's usage records
    usage_records = WaterUsage.objects.filter(user=user).order_by("-usage_date", "-id")

    # ----------------------------------------------
    # SUMMARY STATISTICS
    # ----------------------------------------------
    # Calculate overall metrics to support a more
    # professional analytics-style history page.
    summary = usage_records.aggregate(
        total_litres=Sum("litres_used"),
        average_litres=Avg("litres_used")
    )

    total_records = usage_records.count()
    total_litres = float(summary["total_litres"] or 0)
    average_litres = round(float(summary["average_litres"] or 0), 2)
    latest_record = usage_records.first()

    # ----------------------------------------------
    # CHART DATA PREPARATION
    # ----------------------------------------------
    # Group usage by date so the chart shows one clean
    # total per day instead of multiple repeated bars
    # for the same date.
    daily_usage = (
        WaterUsage.objects
        .filter(user=user)
        .values("usage_date")
        .annotate(total_litres=Sum("litres_used"))
        .order_by("usage_date")
    )

    chart_labels = [
        entry["usage_date"].strftime("%d %b %Y")
        for entry in daily_usage
    ]

    chart_values = [
        float(entry["total_litres"])
        for entry in daily_usage
    ]

    return render(request, "usage/usage_history.html", {
        "usage_records": usage_records,
        "user": user,
        "total_records": total_records,
        "total_litres": total_litres,
        "average_litres": average_litres,
        "latest_record": latest_record,
        "chart_labels_json": json.dumps(chart_labels),
        "chart_values_json": json.dumps(chart_values),
    })