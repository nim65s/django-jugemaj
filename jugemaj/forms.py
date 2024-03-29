"""Django forms for the jugemaj app."""
from django import forms

from ndh.forms import AccessibleDateTimeField

from .models import Election


class ElectionForm(forms.ModelForm):
    """Form for the Election model."""

    end = AccessibleDateTimeField()

    class Meta:
        """Declare the model and fields for this form."""

        model = Election
        fields = ("name", "description", "end")
