"""
Admin configuration for the Community app.

This module registers Community-related models with the
Django admin site so administrators can manage:

- community posts
- comments
- likes

The admin setup improves maintainability by providing
search, filtering, ordering, and clear list displays.
"""

from django.contrib import admin
from .models import CommunityPost, Comment, PostLike


# ==================================================
# COMMUNITY POST ADMIN
# ==================================================
@admin.register(CommunityPost)
class CommunityPostAdmin(admin.ModelAdmin):
    """
    Admin configuration for community posts.

    Provides a structured overview of:
    - post title
    - author
    - post type
    - location
    - creation date
    """

    list_display = (
        "title",
        "author",
        "post_type",
        "location",
        "created_at",
        "updated_at",
    )

    list_filter = (
        "post_type",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "title",
        "content",
        "location",
        "author__first_name",
        "author__last_name",
        "author__email",
    )

    ordering = ("-created_at",)


# ==================================================
# COMMENT ADMIN
# ==================================================
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    Admin configuration for community comments.

    Helps administrators review comments linked to posts
    and identify the users who created them.
    """

    list_display = (
        "post",
        "author",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "content",
        "author__first_name",
        "author__last_name",
        "author__email",
        "post__title",
    )

    ordering = ("-created_at",)


# ==================================================
# POST LIKE ADMIN
# ==================================================
@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    """
    Admin configuration for post likes.

    Allows administrators to monitor engagement activity
    across community posts.
    """

    list_display = (
        "post",
        "user",
        "created_at",
    )

    list_filter = (
        "created_at",
    )

    search_fields = (
        "post__title",
        "user__first_name",
        "user__last_name",
        "user__email",
    )

    ordering = ("-created_at",)