"""
URL configuration for the Community app.

This module defines the URL routes for the HydroGuard
community feature.

The community app supports:
- viewing the main community feed
- creating a new post
- viewing a single post in detail
- adding comments to a post
- liking and unliking posts

These routes are kept inside a dedicated app-level URL
configuration to maintain modular project structure.
"""

from django.urls import path
from . import views


# ==================================================
# APPLICATION NAMESPACE
# ==================================================
# Namespacing helps avoid URL name collisions across apps
# and keeps route references clear within templates/views.
app_name = "community"


# ==================================================
# COMMUNITY URL PATTERNS
# ==================================================
urlpatterns = [
    # Main community feed page
    path("", views.community_feed, name="community_feed"),

    # Create a new community post
    path("create/", views.create_post, name="create_post"),

    # View a specific community post in detail
    path("post/<int:post_id>/", views.post_detail, name="post_detail"),

    # Submit a comment for a specific post
    path("post/<int:post_id>/comment/", views.add_comment, name="add_comment"),

    # Toggle like/unlike for a specific post
    path("post/<int:post_id>/like/", views.toggle_like, name="toggle_like"),
]