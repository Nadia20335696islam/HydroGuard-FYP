"""
Models for the Community app.

This module defines the database structure for the HydroGuard
community feature, allowing users to:

- share water-saving tips
- report local water-related issues
- interact with other users through likes and comments

The design ensures scalability, clean relationships, and
clear separation of responsibilities across models.
"""

from django.db import models
from accounts.models import User


# ==================================================
# COMMUNITY POST MODEL
# ==================================================
class CommunityPost(models.Model):
    """
    Represents a user-generated post in the community.

    A post can be either:
    - a water-saving tip
    - a reported local water issue

    This model acts as the core entity of the community system.
    """

    # ----------------------------------------------
    # POST TYPE CHOICES
    # ----------------------------------------------
    POST_TYPE_CHOICES = [
        ("TIP", "Water Saving Tip"),
        ("ISSUE", "Water Issue Report"),
    ]

    # ----------------------------------------------
    # RELATIONSHIP: AUTHOR
    # ----------------------------------------------
    # Each post is created by a registered user
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="community_posts"
    )

    # ----------------------------------------------
    # POST CONTENT FIELDS
    # ----------------------------------------------
    title = models.CharField(max_length=150)
    content = models.TextField()

    # Defines whether the post is a tip or an issue
    post_type = models.CharField(
        max_length=10,
        choices=POST_TYPE_CHOICES
    )

    # Optional location field (useful for issue reports)
    location = models.CharField(
        max_length=150,
        blank=True,
        null=True
    )

    # ----------------------------------------------
    # TIMESTAMP FIELDS
    # ----------------------------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # ----------------------------------------------
    # STRING REPRESENTATION
    # ----------------------------------------------
    def __str__(self):
        return f"{self.title} ({self.post_type})"


# ==================================================
# COMMENT MODEL
# ==================================================
class Comment(models.Model):
    """
    Represents a comment made by a user on a community post.

    Enables interaction between users by allowing discussion
    under each post.
    """

    # Relationship to the post
    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    # Author of the comment
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="community_comments"
    )

    # Comment content
    content = models.TextField()

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    # String representation
    def __str__(self):
        return f"Comment by {self.author} on {self.post}"


# ==================================================
# POST LIKE MODEL
# ==================================================
class PostLike(models.Model):
    """
    Represents a 'like' interaction on a community post.

    Each user can like a post only once.
    This model helps track engagement within the community.
    """

    # Relationship to the post
    post = models.ForeignKey(
        CommunityPost,
        on_delete=models.CASCADE,
        related_name="likes"
    )

    # User who liked the post
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="liked_posts"
    )

    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    # Ensure a user cannot like the same post multiple times
    class Meta:
        unique_together = ("post", "user")

    # String representation
    def __str__(self):
        return f"{self.user} liked {self.post}"