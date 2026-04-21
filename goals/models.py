"""
Models for the goals app.

This stores user water-saving goals and alert settings.
"""

from django.db import models


class WaterGoal(models.Model):
    """
    Stores a user's daily water usage goal and alert preferences.
    """

    user = models.OneToOneField(
        "accounts.User",
        on_delete=models.CASCADE,
        related_name="water_goal"
    )

    daily_target_litres = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    warning_percentage = models.PositiveIntegerField(
        default=80
    )

    reminders_enabled = models.BooleanField(default=True)
    alerts_enabled = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - {self.daily_target_litres}L/day"

    def warning_limit(self):
        """
        Calculates when warning should trigger.
        Example: 80% of target
        """
        return (self.daily_target_litres * self.warning_percentage) / 100