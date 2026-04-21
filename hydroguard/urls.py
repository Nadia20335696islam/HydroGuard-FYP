"""
URL configuration for the HydroGuard project.

This file serves as the main routing entry point for the entire application.
It maps top-level URL paths to their corresponding views or app-level
URL configurations.

Each app (e.g., accounts, usage, goals) manages its own internal routes,
which are included here using Django's `include()` function.
"""

from django.contrib import admin           # Django admin interface
from django.urls import path, include      # URL routing utilities
from core import views as core_views       # Core application views


# --------------------------------------------------
# PROJECT-LEVEL URL PATTERNS
# --------------------------------------------------
# These routes define the primary navigation structure
# of the HydroGuard system.

urlpatterns = [
    # --------------------------------------------------
    # ADMIN PANEL
    # --------------------------------------------------
    path("admin/", admin.site.urls),

    # --------------------------------------------------
    # CORE PAGES
    # --------------------------------------------------

    # Home page (landing page of the application)
    path("", core_views.home, name="home"),

    # Main user dashboard
    path("dashboard/", core_views.dashboard, name="dashboard"),

    # --------------------------------------------------
    # APPLICATION ROUTES
    # --------------------------------------------------

    # Authentication system (login, register, logout, etc.)
    path("accounts/", include("accounts.urls")),

    # Water usage tracking functionality
    path("usage/", include("usage.urls")),

    # Goals and alerts functionality (NEW FEATURE)
    path("goals/", include("goals.urls")),
    
    path("gamification/", include("gamification.urls")),
    
    path("community/", include("community.urls")),
]