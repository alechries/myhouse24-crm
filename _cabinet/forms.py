from django import forms
from _db import models
from django.forms import TextInput, CharField, Form
from datetime import datetime
from crispy_forms.helper import FormHelper


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
    def __init__(self, *args, **kwargs):
        super(MasterRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
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

