"""
Signals for the gamification app.

This module contains automatic game logic that runs when
important user actions happen inside HydroGuard.

Current responsibilities:
- create a game profile automatically for each new user
- award eco points when a new water usage record is created

This keeps the reward system automatic and connected to
real user actions that support water conservation.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User
from usage.models import WaterUsage
from .models import UserGameProfile


# --------------------------------------------------
# SIGNAL: CREATE GAME PROFILE AUTOMATICALLY
# --------------------------------------------------
@receiver(post_save, sender=User)
def create_user_game_profile(sender, instance, created, **kwargs):
    """
    Automatically create a game profile for each new user.
    """
    if created:
        UserGameProfile.objects.create(user=instance)


# --------------------------------------------------
# SIGNAL: AWARD POINTS FOR NEW WATER USAGE ENTRY
# --------------------------------------------------
@receiver(post_save, sender=WaterUsage)
def award_points_for_usage_entry(sender, instance, created, **kwargs):
    """
    Award eco points when a user creates a new water usage entry.

    Rules for version 1:
    - only award points for newly created entries
    - do not award points when an old record is edited
    - add 10 eco points for each valid new entry
    """
    if not created:
        return

    game_profile, _ = UserGameProfile.objects.get_or_create(user=instance.user)
    game_profile.points += 10
    game_profile.update_level()
    game_profile.save()