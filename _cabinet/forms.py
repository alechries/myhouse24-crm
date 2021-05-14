from django import forms
from _db import models
from datetime import datetime


class MasterRequestForm(forms.ModelForm):
    class Meta:
        model = models.MasterRequest
        fields = ['date', 'time', 'apartment', 'master_type', 'description', 'owner']
        widgets = {
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control",
            }),
            'time': forms.TimeInput(format=('%H:%M'), attrs={
                'type': "time",
                'class': "form-control",
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Введите текст.',
                'class': 'form-control',
                'rows': '11',
            }),
        }

