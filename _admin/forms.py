from django import forms
from _db import models
from django.forms import TextInput, CharField, Form
from datetime import datetime
from crispy_forms.helper import FormHelper
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.core.exceptions import ValidationError
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import forms as django_forms


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


class SEOForm(forms.ModelForm):
    class Meta:
        model = models.SEO
        fields = ['id', 'title', 'keywords', 'description']
        widgets = {
            'id': forms.HiddenInput(),
            'title': forms.TextInput(attrs={
                'id': 'SEOTitleInput',
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
            }),
            'keywords': forms.TextInput(attrs={
                'id': 'SEOKeywordsInput',
                'class': 'form-control',
                'placeholder': 'Введите ключевые слова',
            }),
            'description': forms.TextInput(attrs={
                'id': 'SEODescriptionInput',
                'class': 'form-control',
                'placeholder': 'Введите описание',
            }),
        }


class WebsiteMainPageForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteMainPage
        fields = ['slide1', 'slide2', 'slide3', 'title', 'description']
        widgets = {
            'slide1': forms.FileInput(attrs={
                'id': 'File1Input',
            }),
            'slide2': forms.FileInput(attrs={
                'id': 'File2Input',
            }),
            'slide3': forms.FileInput(attrs={
                'id': 'File3Input',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'rows': '3',
            }),
            'description': forms.Textarea(attrs={
                'id': 'DescriptionInput',
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание',
            }),
        }


class WebsiteMainPageBlocksForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteMainPageBlocks
        fields = ['id', 'image', 'title', 'description']
        widgets = {
            'id': forms.HiddenInput(),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'rows': '3',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание',
            }),
        }


class WebsiteAboutForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteAbout
        fields = ['poster', 'title', 'description']
        widgets = {
            'poster': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'rows': '3',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание',
            }),
        }


class WebsiteAboutGalleryForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteMainPageBlocks
        fields = ['id', 'image']
        widgets = {
            'id': forms.HiddenInput(),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
        }


class WebsiteTariffsForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteTariffs
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'rows': '3',
            }),
            'description': forms.Textarea(attrs={
                'id': 'DescriptionInput',
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание',
            }),
        }


class WebsiteTariffsBlocksForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteTariffBlocks
        fields = ['id', 'image', 'title']
        widgets = {
            'id': forms.HiddenInput(),
            'image': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
                'rows': '3',
            }),
        }


class WebsiteServiceBlocksForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteServiceBlocks
        fields = ['id', 'image', 'name', 'description']
        widgets = {
            'id': forms.HiddenInput(),
            'image': forms.FileInput(attrs={
                'class': 'image-input',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите название услуги',
                'rows': '3',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание услуги',
            }),
        }


class WebsiteContactsForm(forms.ModelForm):
    class Meta:
        model = models.WebsiteContacts
        fields = ['title', 'description', 'site', 'name', 'address', 'tel', 'email', 'map' ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите заголовок',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите описание',
            }),
            'site': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите ссылку',
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес',
            }),
            'tel': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер телефона',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите электронную почту',
            }),
            'map': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите описание',
            }),
        }


class AccountTransactionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AccountTransactionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
    class Meta:
        model = models.Transfer
        fields = ['manager', 'account', 'transfer_type', 'amount', 'comment', 'payment_made', 'created_date',
                  'number']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'id': 'AmountInput',
                'class': 'form-control',
                'placeholder': 'Введите число',
            }),
            'comment': forms.Textarea(attrs={
                'id': 'CommentInput',
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите комментарий',
            }),
            'payment_made': forms.CheckboxInput(attrs={
                'id': 'PaymentMadeInput',
                'class': 'form-control',
            }),
            'created_date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control",
            }),
            'number': forms.TextInput(attrs={
                'input_type': 'text',
                 #'value': ,
                'class': 'form-control',
                'required': 'false'
            }),
        }

        
class AccountForm(forms.ModelForm):

    class Meta:
        model = models.Account
        fields = ['status', 'wallet']
        widgets = {
            'wallet': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
                # 'value': serial_number_account(),
                'aria-required': 'true'
            })
        }


class TariffCreateForm(forms.ModelForm):

    class Meta:
        model = models.Tariff
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
                'area_required': 'true',
            }),
            'description': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
                'area_required': 'true',
            }),
        }


class TariffServiceForm(forms.ModelForm):
    class Meta:
        model = models.TariffService
        fields = ['id', 'price', 'service']
        widgets = {
            'id': forms.HiddenInput(),
            'price': forms.TextInput(attrs={
                'placeholder': 'Введите цену',
                'class': 'form-control',
                'style': 'margin: 0.25rem 0',
            }),

        }


class TariffInvoiceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TariffInvoiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
    class Meta:
        model = models.TariffService
        fields = ['id', 'service', 'amount', 'price']
        widgets = {
            'id': forms.HiddenInput(),
            'amount': forms.NumberInput(attrs={
                'placeholder': 'Введите показания',
                'class': 'form-control invoice-change-event invoice-amount',
                'step': "1",
                'style': 'margin: 0.25rem 0',
            }),
            'price': forms.NumberInput(attrs={
                'placeholder': 'Введите показания',
                'step': "0.1",
                'class': 'form-control invoice-change-event invoice-price',
                'style': 'margin: 0.25rem 0',
            }),

        }


class ApartmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ApartmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    house = forms.ModelChoiceField(
        queryset=models.House.objects.all(),
        empty_label='Выберите...',
        required=False
    )
    section = forms.ModelChoiceField(
        queryset=models.Section.objects.all(),
        empty_label='Выберите...',
        required=False
    )
    class Meta:
        model = models.Apartment
        self_account = forms.TextInput()
        fields = ['apartment_area', 'name', 'floor', 'account', 'user', 'tariff', 'section', 'house']
        widgets = {
            'name': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
                'area_required': 'true',
            }),
            'apartment_area': forms.NumberInput(attrs={
                'class': 'form-control',
                'area_required': 'false',
            }),
        }


class UserForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['status', 'avatar', 'first_name', 'middle_name', 'last_name', 'date_of_birth', 'about', 'number',
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

class HouseForm(forms.ModelForm):
    class Meta:
        model = models.House
        fields = [ 'name', 'address', 'image1', 'image2', 'image3', 'image4', 'image5']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'image1': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'image2': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'image3': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'image4': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),
            'image5': forms.FileInput(attrs={
                'class': 'form-control-file',
            }),

        }


class MessageCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(MessageCreateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False
    house = forms.ModelChoiceField(
        queryset=models.House.objects.all(),
        empty_label='Все',
        required=False
    )
    section = forms.ModelChoiceField(
        queryset=models.Section.objects.all(),
        empty_label='Все',
        required=False
    )
    floor = forms.ModelChoiceField(
        queryset=models.Floor.objects.all(),
        empty_label='Все',
        required=False
    )
    apartment = forms.ModelChoiceField(
        queryset=models.Apartment.objects.all(),
        empty_label='Все',
        required=False
    )
    class Meta:
        model = models.Message
        fields = ['title', 'text', 'indebtedness', 'house', 'section', 'floor', 'apartment']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Введите тему сообщения',
                'type': 'text',
                'class': 'form-control',
            }),
            'text': forms.Textarea(attrs={
                'placeholder': 'Введите текст сообщения...',
                'class': 'form-control',
                'rows': '11',
            }),
            'indebtedness': forms.CheckboxInput(attrs={
                'id': 'PaymentMadeInput',
                'class': 'form-control',
            }),
        }


class MasterRequestForm(forms.ModelForm):
    class Meta:
        model = models.MasterRequest
        owner = forms.ModelChoiceField(
            queryset=models.User.objects.filter(is_superuser=0),
            empty_label=None,
        )
        fields = ['date', 'time', 'owner', 'apartment', 'master_type', 'master', 'status', 'description', 'comment']
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
            'comment': forms.Textarea(attrs={
                'placeholder': 'Введите текст.',
                'class': 'form-control',
                'rows': '6',
            })
        }


class TransactionPurposeForm(forms.ModelForm):
    class Meta:
        model = models.TransferType
        fields = ['status', 'name']


class CounterForm(forms.ModelForm):
    house = forms.ModelChoiceField(
        queryset=models.House.objects.all(),
        empty_label='Выберите...',
    )

    def __init__(self, *args, **kwargs):
        super(CounterForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = models.Meter
        fields = ['apartment', 'number', 'date', 'service', 'status', 'counter', 'house']
        widgets = {
            'counter': forms.NumberInput(attrs={
                'id': 'AmountInput',
                'class': 'form-control',
                'placeholder': 'Показания счётчика',
            }),
            'comment': forms.Textarea(attrs={
                'id': 'CommentInput',
                'class': 'form-control',
                'rows': '3',
                'placeholder': 'Введите комментарий',
            }),
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control",
            }),
            'number': forms.TextInput(attrs={
                'input_type': 'text',
                 #'value': ,
                'class': 'form-control',
                'required': 'false'
            }),
        }


class RoleForm(forms.ModelForm):
    class Meta:
        model = models.UserRole
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput(),
            'name': forms.TextInput(),
            'statistic_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'cash_box_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'invoice_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'account_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'apartment': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'house_user_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'house_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'message_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'master_request_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'meter_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'website_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'service_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'tariffs_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'role_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'user_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
            'payments_detail_status': forms.CheckboxInput(attrs={
                'style': 'margin: auto; width: 18px',
                'class': 'form-control',
            }),
        }


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = models.User
        fields = ['email', 'first_name', 'last_name', 'number', 'role', 'status', 'password', 'is_superuser']
        field_classes = {
            'email': django_forms.UsernameField
        }
        widgets = {
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
            }),
            'number': TextInput(attrs={
                'placeholder': "Номер телефона",
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': "Почта",
                'class': 'form-control',
            }),
            'first_name': TextInput(attrs={
                'placeholder': "Имя",
                'class': 'form-control',
            }),
            'last_name': TextInput(attrs={
                'placeholder': "Фамилия",
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


class PaymentCompany(forms.ModelForm):
    class Meta:
        model = models.Requisites
        fields = ['company_name', 'information']
        widgets = {
            'company_name': forms.TextInput(attrs={
                'placeholder': 'Введите название компании',
                'type': 'text',
                'class': 'form-control',
            }),
            'information': forms.Textarea(attrs={
                'placeholder': 'Введите дополнительную информацию',
                'class': 'form-control',
                'rows': '12',
            }),
        }
    pass


class InvoiceIDCreateForm(forms.ModelForm):
    pass


class InvoiceForm(forms.ModelForm):
    house = forms.ModelChoiceField(
        queryset=models.House.objects.all(),
        empty_label='Выберите...',
    )
    result = forms.CharField(
        required=False
    )


    def __init__(self, *args, **kwargs):
        super(InvoiceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False


    class Meta:
        model = models.Invoice
        fields = ['number', 'house', 'apartment', 'type', 'date', 'period_from', 'period_to', 'status', 'result']
        widgets = {
            'result': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'number': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'status': forms.CheckboxInput(attrs={
                'class': 'form-control custom-checkbox-formset',
                'id': 'PaymentMadeInput',
            }),
            'date': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control",
            }),
            'period_from': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control",
            }),
            'period_to': forms.DateInput(format=('%Y-%m-%d'), attrs={
                'type': "date",
                'value': datetime.now().strftime('%Y-%m-%d'),
                'class': "form-control",
            }),
        }




class ServiceForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput(),
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите название услуги',
                'type': 'text',
                'style': 'margin-top: 5px; margin-bottom: 5px',
                'class': 'form-control'
            }),
            'active': forms.CheckboxInput(attrs={
                'class': 'form-control custom-checkbox-formset',
                'id': 'PaymentMadeInput',
            }),
        }


class MeasureForm(forms.ModelForm):
    class Meta:
        model = models.Service
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput(),
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите еденицу измерения',
                'type': 'text',
                'class': 'form-control',
            }),
        }


class FloorForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FloorForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = models.Floor
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput(),
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите этаж',
                'type': 'text',
                'class': 'form-control',
                'style': 'margin: 0.25rem 0',
            }),
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = models.Section
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput(),
            'name': forms.TextInput(attrs={
                'placeholder': 'Введите название',
                'type': 'text',
                'class': 'form-control',
                'style': 'margin: 0.25rem 0',
            }),
        }


class UserHouseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserHouseForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    class Meta:
        model = models.UserHouse
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput(),
        }


class UserInviteForm(forms.ModelForm):
    class Meta:
        model = models.UserInvite
        fields = ['email', 'phone']
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'Введите телефон',
                'type': 'text',
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Введите email',
                'class': 'form-control',
            })
        }
