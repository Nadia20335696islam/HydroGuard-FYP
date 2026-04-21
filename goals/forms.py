"""
Forms for the goals app.

Handles user input for setting water-saving goals and alerts.
"""

from django import forms
from .models import WaterGoal


class WaterGoalForm(forms.ModelForm):
    """
    Form for creating or updating a water goal.
    """

    class Meta:
        model = WaterGoal
        fields = [
            "daily_target_litres",
            "warning_percentage",
            "reminders_enabled",
            "alerts_enabled",
        ]

        widgets = {
            "daily_target_litres": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter daily target in litres"
            }),
            "warning_percentage": forms.NumberInput(attrs={
                "class": "form-control",
                "placeholder": "Enter warning percentage (e.g. 80)"
            }),
            "reminders_enabled": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
            "alerts_enabled": forms.CheckboxInput(attrs={
                "class": "form-check-input"
            }),
        }

    def clean_daily_target_litres(self):
        value = self.cleaned_data.get("daily_target_litres")

        if value is None or value <= 0:
            raise forms.ValidationError("Target must be greater than 0.")

        return value

    def clean_warning_percentage(self):
        value = self.cleaned_data.get("warning_percentage")

        if value < 1 or value > 100:
            raise forms.ValidationError("Must be between 1 and 100.")

        return value