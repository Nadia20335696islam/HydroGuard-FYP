"""
Forms for the Community app.

This module defines the forms used in the HydroGuard community
feature. These forms allow authenticated users to:

- create community posts
- share water-saving tips
- report local water issues
- comment on existing posts

The forms include presentation-focused widgets and validation
rules to improve usability, consistency, and data quality.
"""

from django import forms
from .models import CommunityPost, Comment


# ==================================================
# COMMUNITY POST FORM
# ==================================================
class CommunityPostForm(forms.ModelForm):
    """
    Form for creating a new community post.

    This form is used for both:
    - water-saving tips
    - local water issue reports

    It applies user-friendly widgets and includes custom
    validation to ensure important fields are completed
    correctly based on the selected post type.
    """

    class Meta:
        model = CommunityPost
        fields = ["post_type", "title", "content", "location"]

        widgets = {
            "post_type": forms.Select(attrs={
                "class": "form-select"
            }),
            "title": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter a short and clear title"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Write your tip or describe the water issue clearly"
            }),
            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter area or location (required for issue reports)"
            }),
        }

        labels = {
            "post_type": "Post Type",
            "title": "Title",
            "content": "Post Content",
            "location": "Location / Area",
        }

        help_texts = {
            "post_type": "Choose whether you are sharing a tip or reporting a local water issue.",
            "title": "Keep the title brief and meaningful.",
            "content": "Provide enough detail so other users can understand the post.",
            "location": "This is especially useful when reporting a local water issue.",
        }

    # ----------------------------------------------
    # FIELD-LEVEL VALIDATION: TITLE
    # ----------------------------------------------
    def clean_title(self):
        """
        Validates the post title.

        Ensures the title is not too short and removes
        unnecessary surrounding spaces.
        """
        title = self.cleaned_data.get("title", "").strip()

        if len(title) < 5:
            raise forms.ValidationError("Title must be at least 5 characters long.")

        return title

    # ----------------------------------------------
    # FIELD-LEVEL VALIDATION: CONTENT
    # ----------------------------------------------
    def clean_content(self):
        """
        Validates the post content.

        Ensures users provide meaningful information rather
        than very short or empty submissions.
        """
        content = self.cleaned_data.get("content", "").strip()

        if len(content) < 10:
            raise forms.ValidationError("Post content must be at least 10 characters long.")

        return content

    # ----------------------------------------------
    # FORM-LEVEL VALIDATION
    # ----------------------------------------------
    def clean(self):
        """
        Applies cross-field validation rules.

        Business rule:
        - If the user selects 'ISSUE', location becomes required
          because issue reports should identify where the problem exists.
        """
        cleaned_data = super().clean()

        post_type = cleaned_data.get("post_type")
        location = cleaned_data.get("location")

        if post_type == "ISSUE" and (not location or not location.strip()):
            self.add_error("location", "Location is required when reporting a water issue.")

        return cleaned_data


# ==================================================
# COMMENT FORM
# ==================================================
class CommentForm(forms.ModelForm):
    """
    Form for submitting a comment on a community post.

    This form keeps the interaction process simple while
    ensuring comments are meaningful and not empty.
    """

    class Meta:
        model = Comment
        fields = ["content"]

        widgets = {
            "content": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write your comment here..."
            }),
        }

        labels = {
            "content": "Comment",
        }

        help_texts = {
            "content": "Share a helpful or respectful response to this post.",
        }

    # ----------------------------------------------
    # FIELD-LEVEL VALIDATION: COMMENT CONTENT
    # ----------------------------------------------
    def clean_content(self):
        """
        Validates comment text.

        Prevents empty or extremely short comments from
        being submitted.
        """
        content = self.cleaned_data.get("content", "").strip()

        if len(content) < 2:
            raise forms.ValidationError("Comment must be at least 2 characters long.")

        return content