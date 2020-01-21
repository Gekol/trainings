from django import forms

from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ("date", "distance", "duration")
        help_texts = {
            "date": "Enter the date(yyyy-mm-dd)",
            "distance": "Enter the distance(in km)",
            "duration": "Enter the duration(in minutes)"
        }

        # widgets = {
        #     "date": forms.DateField(attrs={'placeholder': 'Enter the date'}),
        #     "distance": forms.FloatField(attrs={'placeholder': 'Enter the distance(in km)'}),
        #     "duration": forms.FloatField(attrs={'placeholder': 'Enter the duration(in minutes)'}),
        # }

class FilterForm(forms.Form):
    date_from = forms.DateField(label="From")
    date_to = forms.DateField(label="To")