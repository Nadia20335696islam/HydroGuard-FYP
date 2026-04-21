"""
Database models for the usage app.

This module defines the data structure for recording user water usage
within the HydroGuard project. Each record represents one water usage
activity entered by a logged-in user.

The model supports both:
- general fields used for every water usage entry
- optional activity-specific fields used only for certain activities
  such as shower, laundry, dishwashing, or garden watering
"""

from django.db import models
from accounts.models import User


# --------------------------------------------------
# WATER USAGE MODEL
# --------------------------------------------------
class WaterUsage(models.Model):
    """
    Represents a single water usage record created by a user.

    A record stores:
    - the user who logged the activity
    - the type of activity
    - the amount of water used in litres
    - the date of usage
    - optional extra information depending on activity type

    Examples:
    - Shower -> duration_minutes may be filled
    - Laundry -> laundry_load_size may be filled
    - Dishwashing -> dishwashing_method may be filled
    - Garden watering -> garden_area may be filled
    """

    # ----------------------------------------------
    # MAIN ACTIVITY CHOICES
    # ----------------------------------------------
    # These predefined choices help keep activity data
    # consistent across all user entries.
    ACTIVITY_CHOICES = [
        ("shower", "Shower"),
        ("bath", "Bath"),
        ("dishwashing", "Dishwashing"),
        ("laundry", "Laundry"),
        ("cleaning", "Cleaning"),
        ("cooking", "Cooking"),
        ("drinking", "Drinking"),
        ("garden", "Garden Watering"),
        ("other", "Other"),
    ]

    # ----------------------------------------------
    # ACTIVITY-SPECIFIC CHOICES
    # ----------------------------------------------
    # Used only when the activity is laundry.
    LAUNDRY_SIZE_CHOICES = [
        ("small", "Small Load"),
        ("medium", "Medium Load"),
        ("large", "Large Load"),
    ]

    # Used only when the activity is dishwashing.
    DISHWASHING_METHOD_CHOICES = [
        ("hand", "Hand Wash"),
        ("dishwasher", "Dishwasher"),
    ]

    # ----------------------------------------------
    # CORE FIELDS
    # ----------------------------------------------
    # The user who created this water usage entry.
    # If the user is deleted, all their related usage
    # records will also be deleted.
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="water_usages"
    )

    # The type of water usage activity.
    activity = models.CharField(
        max_length=50,
        choices=ACTIVITY_CHOICES
    )

    # Estimated amount of water used in litres.
    # DecimalField is used so the system can store
    # more precise values such as 12.50 litres.
    litres_used = models.DecimalField(
        max_digits=6,
        decimal_places=2
    )

    # The date on which the activity took place.
    usage_date = models.DateField()

    # Optional user note for additional details.
    notes = models.TextField(
        blank=True
    )

    # Timestamp automatically created when the record
    # is first saved to the database.
    created_at = models.DateTimeField(auto_now_add=True)

    # ----------------------------------------------
    # OPTIONAL ACTIVITY-SPECIFIC FIELDS
    # ----------------------------------------------
    # Duration in minutes, mainly useful for shower
    # or bath-related records.
    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    # Laundry load size, only relevant when activity
    # is set to laundry.
    laundry_load_size = models.CharField(
        max_length=10,
        choices=LAUNDRY_SIZE_CHOICES,
        null=True,
        blank=True
    )

    # Dishwashing method, only relevant when activity
    # is set to dishwashing.
    dishwashing_method = models.CharField(
        max_length=15,
        choices=DISHWASHING_METHOD_CHOICES,
        null=True,
        blank=True
    )

    # Simple description of the garden area, only
    # relevant when activity is garden watering.
    # Example values:
    # - "small front garden"
    # - "backyard plants"
    # - "indoor plants"
    garden_area = models.CharField(
        max_length=100,
        null=True,
        blank=True
    )

    def __str__(self):
        """
        Return a readable string representation of the record.
        """
        return f"{self.user.email} - {self.get_activity_display()} - {self.litres_used}L"