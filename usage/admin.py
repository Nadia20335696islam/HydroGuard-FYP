"""
Admin configuration for the usage app.

This module registers the WaterUsage model with Django's admin site
so administrators can monitor and manage user water usage records.

The admin configuration improves usability by providing:
- clear columns in the list view
- filtering options for activity and dates
- search functionality for user and record details
- logical grouping of fields in the edit form
- default ordering for recent records
"""

from django.contrib import admin
from .models import WaterUsage


# ==================================================
# WATER USAGE ADMIN
# ==================================================
@admin.register(WaterUsage)
class WaterUsageAdmin(admin.ModelAdmin):
    """
    Admin configuration for the WaterUsage model.

    This setup allows administrators to:
    - review submitted usage records
    - search for records by user or notes
    - filter records by activity and date
    - inspect both general and activity-specific fields
    """

    # --------------------------------------------------
    # LIST VIEW CONFIGURATION
    # --------------------------------------------------
    # These fields are displayed as columns in the main
    # admin list page for WaterUsage records.
    list_display = (
        "id",
        "user",
        "activity",
        "litres_used",
        "usage_date",
        "created_at",
    )

    # --------------------------------------------------
    # FILTER CONFIGURATION
    # --------------------------------------------------
    # Adds a filter sidebar so administrators can quickly
    # narrow records by activity type or dates.
    list_filter = (
        "activity",
        "usage_date",
        "created_at",
    )

    # --------------------------------------------------
    # SEARCH CONFIGURATION
    # --------------------------------------------------
    # Enables keyword search in the admin list page.
    # Related user fields are included to make it easier
    # to find records submitted by a specific person.
    search_fields = (
        "user__first_name",
        "user__last_name",
        "user__email",
        "notes",
        "garden_area",
    )

    # --------------------------------------------------
    # DEFAULT ORDERING
    # --------------------------------------------------
    # Shows the newest records first so administrators
    # can review recent submissions more easily.
    ordering = ("-created_at",)

    # --------------------------------------------------
    # READ-ONLY FIELDS
    # --------------------------------------------------
    # These timestamps are automatically generated and
    # should not normally be edited manually by admins.
    readonly_fields = ("created_at",)

    # --------------------------------------------------
    # FORM LAYOUT
    # --------------------------------------------------
    # Organises the admin detail page into logical sections
    # so the record is easier to understand and maintain.
    fieldsets = (
        (
            "Basic Water Usage Information",
            {
                "fields": (
                    "user",
                    "activity",
                    "litres_used",
                    "usage_date",
                    "notes",
                )
            },
        ),
        (
            "Activity-Specific Details",
            {
                "fields": (
                    "duration_minutes",
                    "laundry_load_size",
                    "dishwashing_method",
                    "garden_area",
                ),
                "description": (
                    "These fields are optional and should only be used "
                    "when relevant to the selected activity type."
                ),
            },
        ),
        (
            "System Information",
            {
                "fields": ("created_at",),
            },
        ),
    )