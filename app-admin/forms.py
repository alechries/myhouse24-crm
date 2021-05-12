from django import forms
from _db import models
from datetime import datetime


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
                'class': 'upload',
                'id': 'File1Input',
            }),
            'slide2': forms.FileInput(attrs={
                'class': 'upload',
                'id': 'File2Input',
            }),
            'slide3': forms.FileInput(attrs={
                'class': 'upload',
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
        fields = ['title', 'description', 'site', 'name', 'address', 'tel', 'email', ]
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
        }


class AccountTransactionForm(forms.ModelForm):
    class Meta:
        model = models.Transfer
        fields = ['user', 'manager', 'account', 'transfer_type', 'amount', 'comment', 'payment_made', 'created_date',
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
        house = forms.ModelChoiceField(
            queryset=models.House.objects.all(),
            empty_label=None,
        )

        section = forms.ModelChoiceField(
            queryset=models.Section.objects.all(),
            empty_label=None,
        )

        floor = forms.ModelChoiceField(
            queryset=models.Floor.objects.all(),
            empty_label=None,
        )

        fields = ['status', 'apartment', 'wallet']
        widgets = {
            'wallet': forms.TextInput(attrs={
                'input_type': 'text',
                'class': 'form-control',
                # 'value': serial_number_account(),
                'aria-required': 'true'
            })
        }


class RateForm(forms.ModelForm):

    class Meta:
        model = models.Rate
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


class ApartmentForm(forms.ModelForm):

    class Meta:
        model = models.Apartment
        self_account = forms.TextInput()
        fields = ['apartment_area', 'name', 'floor', 'self_account']
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
                'type': 'Password',
                'class': 'form-control',
            }),
            }


class HouseForm(forms.ModelForm):
    class Meta:
        model = models.House
        fields = ['user', 'name', 'address', 'image1', 'image2', 'image3', 'image4', 'image5']
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
    class Meta:
        model = models.Message
        destination = forms.ModelChoiceField(
            queryset=models.User.objects.all(),
            empty_label=None,
        )
        fields = ['title', 'destination', 'text', 'indebtedness']
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
        fields = ['date', 'time', 'owner', 'apartment', 'master_type', 'master', 'status', 'description', 'comment']
        owner = forms.ModelChoiceField(
            queryset=models.User.objects.all(),
            empty_label=None,
        )
        apartment = forms.ModelChoiceField(
            queryset=models.Apartment.objects.all(),
            empty_label=None
        )
        master = forms.ModelChoiceField(
            queryset=models.User.objects.filter(user_type='Обслуживающий персонал'),
            empty_label=None
        )
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
    class Meta:
        model = models.Meter
        fields = ['apartment', 'number', 'date', 'service', 'status', 'counter']
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
    pass


class RoleForm(forms.ModelForm):
    class Meta:
        model = models.UserRole
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput(),
            'name': forms.TextInput(),
            'statistic_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'cash_box_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'invoice_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'account_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'apartment': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'house_user_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'house_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'message_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'master_request_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'meter_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'website_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'service_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'tariffs_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'role_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'user_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'payments_detail_status': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
        }


class InvoiceIDCreateForm(forms.ModelForm):

    pass


class InvoiceTitleCreateForm(forms.ModelForm):
    pass


class InvoiceServicesCreateForm(forms.ModelForm):
    pass