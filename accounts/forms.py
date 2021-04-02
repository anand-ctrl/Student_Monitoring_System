from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from accounts.models import feedback


class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=200)
    c = [(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]
    rating = forms.ChoiceField(help_text="(Rate between 1 to 5)", choices=c)
    comment = forms.CharField(max_length=500, required=False, widget=forms.Textarea)

