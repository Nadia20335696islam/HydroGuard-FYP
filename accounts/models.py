"""
Database models for the accounts app.

This file defines the custom User model used by the HydroGuard
application for registration and login.
"""

from django.db import models


# --------------------------------------------------
# USER MODEL
# --------------------------------------------------
# This model stores account information for HydroGuard users.
# It currently supports custom registration and login using email.

class User(models.Model):
    """
    Custom user model for the HydroGuard application.
    """

    # User's first name
    first_name = models.CharField(max_length=50)

    # User's last name
    last_name = models.CharField(max_length=50)

    # User's email address (must be unique)
    email = models.EmailField(unique=True)

    # Securely stored password hash
    password_hash = models.CharField(max_length=128)

    # Salt used for password hashing
    salt = models.CharField(max_length=64)

    # Timestamp automatically set when the account is created
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        Return a readable string representation of the user.
        """
        return f"{self.first_name} {self.last_name} ({self.email})"