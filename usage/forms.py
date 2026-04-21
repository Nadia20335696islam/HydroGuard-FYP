"""
Forms for the usage app.

This module defines Django forms used to collect water usage data
from users in a structured, user-friendly, and validated way.

The main form supports:
- general water usage input
- activity-specific questions
- both frontend and backend validation to ensure data quality
"""

from django import forms
from .models import WaterUsage


# --------------------------------------------------
# WATER USAGE FORM
# --------------------------------------------------
class WaterUsageForm(forms.ModelForm):
    """
    Form for creating a new water usage record.

    This form includes:
    - shared fields used for all entries
    - optional activity-specific fields
    - validation to ensure realistic and meaningful data

    Validation is handled at two levels:
    1. Frontend (HTML attributes like min/step)
    2. Backend (Django clean methods)
    """

    class Meta:
        model = WaterUsage

        # Fields included in the form
        fields = [
            "activity",
            "litres_used",
            "duration_minutes",
            "laundry_load_size",
            "dishwashing_method",
            "garden_area",
            "usage_date",
            "notes",
        ]

        # --------------------------------------------------
        # FORM WIDGETS (UI + FRONTEND VALIDATION)
        # --------------------------------------------------
        widgets = {
            "activity": forms.Select(attrs={
                "class": "form-select"
            }),

            # Prevent negative and unrealistic values using min/step
            "litres_used": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "For example: 45",
                "min": "0.01",     # Prevent zero/negative input
                "step": "0.01"     # Allow decimal precision
            }),

            # Prevent negative durations
            "duration_minutes": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "For example: 10",
                "min": "1",        # Minimum 1 minute
                "step": "1"        # Whole numbers only
            }),

            "laundry_load_size": forms.Select(attrs={
                "class": "form-select"
            }),

            "dishwashing_method": forms.Select(attrs={
                "class": "form-select"
            }),

            "garden_area": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "For example: small front garden"
            }),

            "usage_date": forms.DateInput(attrs={
                "class": "form-control",
                "type": "date"
            }),

            "notes": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 4,
                "placeholder": "Add any extra details about this usage activity"
            }),
        }

        # --------------------------------------------------
        # LABELS (USER-FRIENDLY TEXT)
        # --------------------------------------------------
        labels = {
            "activity": "What type of water activity did you do?",
            "litres_used": "How many litres of water did you use?",
            "duration_minutes": "How long did it take? (in minutes, if applicable)",
            "laundry_load_size": "What size was the laundry load?",
            "dishwashing_method": "How did you wash the dishes?",
            "garden_area": "What area did you water?",
            "usage_date": "When did this happen?",
            "notes": "Additional notes",
        }

        # --------------------------------------------------
        # HELP TEXTS (GUIDANCE FOR USERS)
        # --------------------------------------------------
        help_texts = {
            "activity": "Choose the activity that best matches your water usage.",
            "litres_used": "Enter your best estimate of the water consumed.",
            "duration_minutes": "Useful for activities such as showering or bathing.",
            "laundry_load_size": "Only needed if the activity is laundry.",
            "dishwashing_method": "Only needed if the activity is dishwashing.",
            "garden_area": "Only needed if the activity is garden watering.",
            "usage_date": "Select the date when the activity took place.",
            "notes": "Optional: include anything helpful, such as number of loads or special circumstances.",
        }

    # --------------------------------------------------
    # FIELD-LEVEL VALIDATION
    # --------------------------------------------------
    def clean_litres_used(self):
        """
        Ensure litres used is:
        - provided
        - greater than 0
        - within a realistic range
        """
        litres_used = self.cleaned_data.get("litres_used")

        if litres_used is None:
            raise forms.ValidationError("Please enter the amount of water used.")

        if litres_used <= 0:
            raise forms.ValidationError("Litres used must be greater than 0.")

        if litres_used > 5000:
            raise forms.ValidationError("Please enter a realistic water usage value.")

        return litres_used

    def clean_duration_minutes(self):
        """
        Ensure duration (if provided):
        - is positive
        - is within a realistic range
        """
        duration = self.cleaned_data.get("duration_minutes")

        if duration is not None:
            if duration <= 0:
                raise forms.ValidationError("Duration must be greater than 0 minutes.")

            if duration > 300:
                raise forms.ValidationError("Please enter a realistic duration.")

        return duration

    # --------------------------------------------------
    # FORM-LEVEL VALIDATION
    # --------------------------------------------------
    def clean(self):
        """
        Apply activity-specific validation rules.

        Certain fields become required depending on
        the selected activity.
        """
        cleaned_data = super().clean()

        activity = cleaned_data.get("activity")
        duration_minutes = cleaned_data.get("duration_minutes")
        laundry_load_size = cleaned_data.get("laundry_load_size")
        dishwashing_method = cleaned_data.get("dishwashing_method")
        garden_area = cleaned_data.get("garden_area")

        # Require duration for shower and bath
        if activity in ["shower", "bath"] and not duration_minutes:
            self.add_error(
                "duration_minutes",
                "Please enter the duration for this activity."
            )

        # Require laundry load size for laundry activity
        if activity == "laundry" and not laundry_load_size:
            self.add_error(
                "laundry_load_size",
                "Please select the laundry load size."
            )

        # Require dishwashing method for dishwashing activity
        if activity == "dishwashing" and not dishwashing_method:
            self.add_error(
                "dishwashing_method",
                "Please select how the dishes were washed."
            )

        # Require garden area for garden watering activity
        if activity == "garden" and not garden_area:
            self.add_error(
                "garden_area",
                "Please describe the area that was watered."
            )

        return cleaned_data