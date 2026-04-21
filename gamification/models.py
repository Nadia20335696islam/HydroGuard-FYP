"""
Models for the gamification app.

This module defines all database models related to HydroGuard's
gamification system.

The purpose of these models is to support:
- user progress tracking
- badge and reward management
- daily mini-game participation
- educational engagement through water-saving challenges
"""

# --------------------------------------------------
# DJANGO IMPORTS
# --------------------------------------------------
from django.db import models
from django.utils import timezone

# --------------------------------------------------
# APPLICATION IMPORTS
# --------------------------------------------------
from accounts.models import User


# --------------------------------------------------
# BADGE MODEL
# --------------------------------------------------
class Badge(models.Model):
    """
    Represents an achievement badge that can be unlocked by a user.

    Examples:
    - First Drop
    - 3-Day Saver
    - Eco Starter
    - Water Hero

    Each badge contains:
    - a name
    - a description
    - an optional icon label for future visual use
    """

    name = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique name of the badge."
    )
    description = models.TextField(
        help_text="Short explanation of how the badge is earned."
    )
    icon = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="Optional icon or emoji label for UI display."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp showing when the badge was created."
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Badge"
        verbose_name_plural = "Badges"

    def __str__(self):
        """
        Return the badge name for admin and debugging use.
        """
        return self.name


# --------------------------------------------------
# USER GAME PROFILE MODEL
# --------------------------------------------------
class UserGameProfile(models.Model):
    """
    Stores gamification progress for each user.

    This model tracks:
    - total eco points
    - current level
    - streak count
    - last game participation date

    A one-to-one relationship is used so that each user
    has exactly one gamification profile.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="game_profile",
        help_text="The user who owns this gamification profile."
    )

    points = models.PositiveIntegerField(
        default=0,
        help_text="Total eco points earned by the user."
    )

    level = models.PositiveIntegerField(
        default=1,
        help_text="Current level based on accumulated eco points."
    )

    streak_days = models.PositiveIntegerField(
        default=0,
        help_text="Number of consecutive days the user has engaged with HydroGuard."
    )

    last_played_date = models.DateField(
        blank=True,
        null=True,
        help_text="The last date the user completed the mini game."
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of the most recent profile update."
    )

    class Meta:
        verbose_name = "User Game Profile"
        verbose_name_plural = "User Game Profiles"

    def __str__(self):
        """
        Return a readable label for admin and debugging use.
        """
        return f"{self.user.first_name} {self.user.last_name} - Game Profile"

    def update_level(self):
        """
        Update the user's level based on current points.

        Level thresholds can be adjusted later as the project grows.
        This method keeps level logic centralised and reusable.
        """
        if self.points >= 500:
            self.level = 5
        elif self.points >= 350:
            self.level = 4
        elif self.points >= 200:
            self.level = 3
        elif self.points >= 100:
            self.level = 2
        else:
            self.level = 1


# --------------------------------------------------
# USER BADGE MODEL
# --------------------------------------------------
class UserBadge(models.Model):
    """
    Represents a badge unlocked by a specific user.

    This model creates a relationship between:
    - a user
    - a badge
    - the date it was unlocked

    A user should not unlock the same badge multiple times.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="earned_badges",
        help_text="The user who unlocked the badge."
    )

    badge = models.ForeignKey(
        Badge,
        on_delete=models.CASCADE,
        related_name="awarded_users",
        help_text="The badge unlocked by the user."
    )

    unlocked_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp showing when the badge was unlocked."
    )

    class Meta:
        unique_together = ("user", "badge")
        ordering = ["-unlocked_at"]
        verbose_name = "User Badge"
        verbose_name_plural = "User Badges"

    def __str__(self):
        """
        Return a readable label showing the user-badge relationship.
        """
        return f"{self.user.email} - {self.badge.name}"


# --------------------------------------------------
# DAILY GAME SESSION MODEL
# --------------------------------------------------
class DailyGameSession(models.Model):
    """
    Stores the result of a user's mini-game session for a specific day.

    This model is important because it allows HydroGuard to:
    - save game participation
    - count correct answers
    - award daily points fairly
    - prevent the same user from claiming the same daily reward multiple times

    One user can only have one recorded session per date.
    """

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="daily_game_sessions",
        help_text="The user who played the mini game."
    )

    play_date = models.DateField(
        default=timezone.now,
        help_text="The calendar date on which the game was played."
    )

    correct_answers = models.PositiveIntegerField(
        default=0,
        help_text="Number of correct answers achieved in the game."
    )

    total_questions = models.PositiveIntegerField(
        default=3,
        help_text="Total number of questions shown in the mini game."
    )

    points_earned = models.PositiveIntegerField(
        default=0,
        help_text="Points awarded to the user for this game session."
    )

    completed = models.BooleanField(
        default=False,
        help_text="Indicates whether the user fully completed the daily game."
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp showing when the game session was recorded."
    )

    class Meta:
        unique_together = ("user", "play_date")
        ordering = ["-play_date"]
        verbose_name = "Daily Game Session"
        verbose_name_plural = "Daily Game Sessions"

    def __str__(self):
        """
        Return a readable label for admin and debugging use.
        """
        return f"{self.user.email} - {self.play_date}"
    # --------------------------------------------------
# DAILY MISSION COMPLETION MODEL
# --------------------------------------------------
class DailyMissionCompletion(models.Model):
    """
    Stores completion records for daily water-saving missions.

    This model allows HydroGuard to:
    - track which missions a user completed
    - store the completion date
    - prevent duplicate point claims for the same mission on the same day
    - support reward-based mission interaction

    Each user can complete a specific mission only once per day.
    """

    MISSION_CHOICES = [
        ("short_shower", "Short Shower"),
        ("turn_off_tap", "Turn Off Tap"),
        ("smart_dishwashing", "Smart Dishwashing"),
        ("log_usage", "Log Usage"),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="daily_mission_completions",
        help_text="The user who completed the mission."
    )

    mission_key = models.CharField(
        max_length=50,
        choices=MISSION_CHOICES,
        help_text="Internal key representing the completed daily mission."
    )

    play_date = models.DateField(
        default=timezone.now,
        help_text="The date on which the mission was completed."
    )

    points_earned = models.PositiveIntegerField(
        default=0,
        help_text="Points awarded for this mission completion."
    )

    completed_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp showing when the mission was completed."
    )

    class Meta:
        unique_together = ("user", "mission_key", "play_date")
        ordering = ["-play_date", "-completed_at"]
        verbose_name = "Daily Mission Completion"
        verbose_name_plural = "Daily Mission Completions"

    def __str__(self):
        """
        Return a readable label for admin and debugging use.
        """
        return f"{self.user.email} - {self.mission_key} - {self.play_date}"