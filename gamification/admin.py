"""
Admin configuration for the gamification app.

This module registers gamification-related models with the Django
administration site so administrators can manage:
- badges
- user gamification profiles
- unlocked user badges
- daily mini-game sessions

The admin layout is configured to improve readability and make
data management easier during development and testing.
"""

# --------------------------------------------------
# DJANGO IMPORTS
# --------------------------------------------------
from django.contrib import admin

# --------------------------------------------------
# APPLICATION IMPORTS
# --------------------------------------------------
from .models import Badge, UserGameProfile, UserBadge, DailyGameSession


# --------------------------------------------------
# BADGE ADMIN
# --------------------------------------------------
@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Badge model.

    Displays key badge information and enables easy searching.
    """

    list_display = ("name", "description", "icon", "created_at")
    search_fields = ("name", "description")
    ordering = ("name",)


# --------------------------------------------------
# USER GAME PROFILE ADMIN
# --------------------------------------------------
@admin.register(UserGameProfile)
class UserGameProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserGameProfile model.

    Displays each user's current progress in the gamification system.
    """

    list_display = ("user", "points", "level", "streak_days", "last_played_date", "updated_at")
    search_fields = ("user__email", "user__first_name", "user__last_name")
    ordering = ("-points",)


# --------------------------------------------------
# USER BADGE ADMIN
# --------------------------------------------------
@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    """
    Admin configuration for the UserBadge model.

    Displays badge unlock records for users.
    """

    list_display = ("user", "badge", "unlocked_at")
    search_fields = ("user__email", "badge__name")
    list_filter = ("unlocked_at",)
    ordering = ("-unlocked_at",)


# --------------------------------------------------
# DAILY GAME SESSION ADMIN
# --------------------------------------------------
@admin.register(DailyGameSession)
class DailyGameSessionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the DailyGameSession model.

    Displays daily mini-game participation and reward data.
    """

    list_display = (
        "user",
        "play_date",
        "correct_answers",
        "total_questions",
        "points_earned",
        "completed",
        "created_at",
    )
    search_fields = ("user__email", "user__first_name", "user__last_name")
    list_filter = ("completed", "play_date")
    ordering = ("-play_date",)