"""
Admin configuration for the goals app.

This module registers the WaterGoal model with Django's admin site
so administrators can manage user water-saving goals and alert settings.

The admin configuration improves usability by providing:
- clear list display columns
- search functionality for user records
- filters for alert and reminder settings
- logical grouping of fields in the admin form
- default ordering for recently updated goal records
"""

# --------------------------------------------------
# DJANGO IMPORTS
# --------------------------------------------------
from django.contrib import admin

# --------------------------------------------------
# APPLICATION IMPORTS
# --------------------------------------------------
from .models import WaterGoal


# ==================================================
# WATER GOAL ADMIN
# ==================================================
@admin.register(WaterGoal)
class WaterGoalAdmin(admin.ModelAdmin):
    """
    Admin configuration for the WaterGoal model.

    This setup allows administrators to:
    - view each user's daily water target
    - manage reminder and alert preferences
    - review warning threshold settings
    - monitor recently updated goal records
    """

    # --------------------------------------------------
    # LIST VIEW CONFIGURATION
    # --------------------------------------------------
    # These fields are displayed as columns in the main
    # Django admin list page for goal records.
    list_display = (
        "user",
        "daily_target_litres",
        "warning_percentage",
        "reminders_enabled",
        "alerts_enabled",
        "created_at",
        "updated_at",
    )

    # --------------------------------------------------
    # FILTER CONFIGURATION
    # --------------------------------------------------
    # Adds filter options in the right sidebar so admins
    # can quickly narrow records based on alert settings
    # and timestamps.
    list_filter = (
        "reminders_enabled",
        "alerts_enabled",
        "created_at",
        "updated_at",
    )

    # --------------------------------------------------
    # SEARCH CONFIGURATION
    # --------------------------------------------------
    # Enables keyword search using related user details
    # to help administrators find a specific goal record.
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    # --------------------------------------------------
    # DEFAULT ORDERING
    # --------------------------------------------------
    # Shows the most recently updated records first so
    # recent changes are easier for administrators to review.
    ordering = ("-updated_at",)

    # --------------------------------------------------
    # READ-ONLY FIELDS
    # --------------------------------------------------
    # These timestamps are system-generated and should
    # normally not be edited manually in the admin panel.
    readonly_fields = (
        "created_at",
        "updated_at",
    )

    # --------------------------------------------------
    # FORM LAYOUT
    # --------------------------------------------------
    # Organises the admin detail page into logical sections
    # so administrators can clearly understand the record.
    fieldsets = (
        (
            "Goal Information",
            {
                "fields": (
                    "user",
                    "daily_target_litres",
                    "warning_percentage",
                )
            },
        ),
        (
            "Alert and Reminder Settings",
            {
                "fields": (
                    "reminders_enabled",
                    "alerts_enabled",
                ),
                "description": (
                    "These settings control whether the user receives "
                    "goal-related reminders and usage alerts."
                ),
            },
        ),
        (
            "System Information",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )