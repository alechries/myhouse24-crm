from django import forms
from _db import models
from django.forms import TextInput, CharField, Form
from datetime import datetime
from crispy_forms.helper import FormHelper
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.core.exceptions import ValidationError


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


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['avatar', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'about', 'number',
                  'viber', 'telegram', 'email', 'password']
        widgets = {
            'avatar': forms.FileInput(),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'middle_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'date_of_birth': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'placeholder': 'Введите дату рождения',
                'class': "form-control",
            }),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '11',
                'placeholder': 'Введите описание',
            }),
            'number': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
            }),
            'email': forms.TextInput(attrs={
                'type': 'email',
                'class': 'form-control',
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user