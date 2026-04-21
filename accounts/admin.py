"""
Admin configuration for the accounts app.

This file registers the User model with Django's admin site
and customizes how user records are displayed.
"""

from django.contrib import admin
from .models import User


# --------------------------------------------------
# USER MODEL ADMIN CONFIGURATION
# --------------------------------------------------

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """
    Admin view configuration for the custom User model.
    """

    # Columns shown in admin list view
    list_display = ("id", "first_name", "last_name", "email", "created_at")

    # Search functionality in admin panel
    search_fields = ("first_name", "last_name", "email")

    # Default ordering (newest first)
    ordering = ("-created_at",)