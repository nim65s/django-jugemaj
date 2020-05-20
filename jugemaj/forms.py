from django import forms

from ndh.forms import AccessibleDateTimeField

from .models import Election, Vote

VoteFormSet = forms.modelformset_factory(Vote,
                                         fields=(
                                             'candidate',
                                             'choice',
                                         ),
                                         extra=0,
                                         widgets={
                                             'choice': forms.RadioSelect,
                                             'candidate': forms.HiddenInput
                                         })


class ElectionForm(forms.ModelForm):
    end = AccessibleDateTimeField()

    class Meta:
        model = Election
        fields = ("name", "description", "end")
