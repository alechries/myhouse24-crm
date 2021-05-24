from django import forms
from _db import models
from django.forms import TextInput, CharField, Form
from datetime import datetime


class LoginForm(Form):
    class Meta:
        model = models.User

    email = CharField(widget=TextInput(attrs={
        'type': 'text',
        'class': 'form-control',
        'placeholder': 'Email',
    }))
    password = CharField(widget=TextInput(attrs={
        'type': 'password',
        'class': 'form-control',
        'placeholder': 'Password',
    }))

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

