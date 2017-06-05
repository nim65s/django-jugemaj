from django import forms
from .models import Vote


VoteFormSet = forms.modelformset_factory(Vote, fields=('candidate', 'choice',), extra=0,
                                         widgets={'choice': forms.RadioSelect, 'candidate': forms.HiddenInput})
