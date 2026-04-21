"""
URL configuration for the usage app.

This file defines routes related to water usage functionality,
including creating and viewing water usage records.
"""

from django.urls import path
from . import views


# --------------------------------------------------
# USAGE URL PATTERNS
# --------------------------------------------------

urlpatterns = [
    # Route for adding a new water usage record
    path("add/", views.add_usage, name="add_usage"),

    # Route for viewing personal water usage history
    path("history/", views.usage_history, name="usage_history"),
]