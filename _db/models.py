import datetime

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from solo.models import SingletonModel
# from embed_video.fields import EmbedVideoField
from . import managers
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator


class Model(models.Model):
    class Meta:
        app_label = '_db'


class UserRole(models.Model):
    name = models.CharField(max_length=255)
    statistic_status = models.BooleanField(default=0)
    cash_box_status = models.BooleanField(default=0)
    invoice_status = models.BooleanField(default=0)
    account_status = models.BooleanField(default=0)
    apartment = models.BooleanField(default=0)
    house_user_status = models.BooleanField(default=0)
    house_status = models.BooleanField(default=0)
    message_status = models.BooleanField(default=0)
    master_request_status = models.BooleanField(default=0)
    meter_status = models.BooleanField(default=0)
    website_status = models.BooleanField(default=0)
    service_status = models.BooleanField(default=0)
    tariffs_status = models.BooleanField(default=0)
    role_status = models.BooleanField(default=0)
    user_status = models.BooleanField(default=0)
    payments_detail_status = models.BooleanField(default=0)

    def __str__(self):
        return self.name

class CustomAbstractUser(AbstractBaseUser, PermissionsMixin):
    """
    An abstract base class implementing a fully featured User model with
    app-admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()

    email = models.CharField(
        _('email address'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[],
        error_messages={
            'unique': _("A user with that email already exists."),
        },
    )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this app-admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = managers.CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(CustomAbstractUser):
    STATUS = (
        ('Активен', 'Активен'),
        ('Новый', 'Новый'),
        ('Отключен', 'Отключен')
    )
    TYPE = (
        ('Администратор', 'Администратор'),
        ('Обслуживающий персонал', 'Обслуживающий персонал'),
        ('Управляющий домом', 'Управляющий домом')
    )

    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, verbose_name='', blank=True, null=True)
    status = models.CharField('', choices=STATUS, max_length=55, blank=True)
    avatar = models.FileField('Аватар', upload_to='images/user/', null=True)
    middle_name = models.CharField('Отчество', max_length=150, null=True)
    date_of_birth = models.DateField('дата рождения', null=True)
    number = models.CharField(max_length=255)
    viber = models.CharField('', max_length=255, null=True, blank=True)
    telegram = models.CharField('', max_length=255, null=True, blank=True)
    about = models.TextField(null=True, blank=True)
    user_type = models.CharField(choices=TYPE, default='Управляющий домом', max_length=155, null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name} - {self.role.name}'

    class Meta:
        app_label = '_db'


class House(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255, verbose_name='', blank=True)
    address = models.CharField(max_length=255)
    number = models.IntegerField('', null=True)
    image1 = models.ImageField(upload_to='images/')
    image2 = models.ImageField(upload_to='images/')
    image3 = models.ImageField(upload_to='images/')
    image4 = models.ImageField(upload_to='images/')
    image5 = models.ImageField(upload_to='images/')

    def __str__(self):
        return f'{self.name}, ул. {self.address}'


class UserHouse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    house = models.ForeignKey(House, on_delete=models.CASCADE)


class Section(models.Model):
    house = models.ForeignKey(House, on_delete=models.CASCADE, verbose_name='', blank=True)
    name = models.CharField(max_length=255, verbose_name='', blank=True)

    def __str__(self):
        return f'{self.name} - {self.house.name}'


class Floor(models.Model):
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Measure(models.Model):  # ед измерения
    name = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.name


class Tariff(models.Model):
    name = models.CharField(max_length=155)
    description = models.CharField(max_length=155)
    price = models.CharField(max_length=155, null=True)

    def __str__(self):
        return self.name


class Service(models.Model):   # услуга
    measure = models.ForeignKey(Measure, on_delete=models.CASCADE, blank=True, verbose_name='', null=True)
    name = models.CharField(max_length=255, null=True)
    active = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.name


class TariffToService(models.Model):
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)


class Apartment(models.Model):
    floor = models.ForeignKey(Floor, on_delete=models.CASCADE, blank=True, verbose_name='')
    name = models.CharField('Номер квартиры', max_length=255)
    apartment_area = models.FloatField('Площадь квартиры', max_length=255)
    self_account = models.CharField('', max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_full_name(self):
        return f'{self.floor.section.house.name}, кв.{self.name}'


class Meter(models.Model):
    STATUS = (
        ('Новое', 'Новое'),
        ('Учтено', 'Учтено'),
        ('Учтено и оплаченно', 'Учтено и оплаченно'),
        ('Нулевое', 'Нулевое')
    )
    number = models.CharField(max_length=155, null=True)
    date = models.DateField(default=timezone.now)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank=True, verbose_name='', null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, blank=True, verbose_name='')
    counter = models.IntegerField()
    indication_date = models.DateField(null=True)
    status = models.CharField(choices=STATUS, max_length=255, blank=True, verbose_name='')


class Account(models.Model):
    STATUS = (
        ('Active', 'Активен'),
        ('Inactive','Неактивен')
    )
    wallet = models.CharField('Номер лицевого счёта', max_length=255, null=True)
    money = models.FloatField(default=0)
    status = models.CharField('',choices=STATUS, max_length=55, blank=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank=True, null=True, verbose_name='')

    def __str__(self):
        return self.wallet


class TransferType(models.Model):
    TYPE = (
        ('Приход', 'Приход'),
        ('Расход', 'Расход')
    )
    status = models.CharField(choices=TYPE, max_length=55, verbose_name='', blank=True)
    name = models.CharField(max_length=255, verbose_name='', blank=True)

    def __str__(self):
        return self.name


class Transfer(models.Model):
    number = models.CharField('Номер транзакции', max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='transfer_user', verbose_name='', null=True)
    manager = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, related_name='transfer_manager', verbose_name='')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True,  verbose_name='', null=True)
    transfer_type = models.ForeignKey(TransferType, on_delete=models.CASCADE, blank=True, verbose_name='', null=True)
    amount = models.IntegerField(verbose_name='', blank=True)
    comment = models.TextField('', null=True, blank=True)
    # статус платежа
    payment_made = models.BooleanField(verbose_name='', null=True)
    #
    created_date = models.DateField(default=timezone.now, null=True)


class Invoice(models.Model):
    TYPE = (
        ('Оплачена', 'Оплачена'),
        ('Частично оплачена', 'Частично оплачена'),
        ('Неоплачена', 'Неоплачена')
    )

    # Добавить модель Тарифа и сделать связь
    status = models.BooleanField(default=False)
    number = models.CharField('', max_length=255, null=True)
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, null=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    type = models.CharField('Статус квитанции', choices=TYPE, max_length=55, null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE)
    period_from = models.DateField("Дата с", null=True)
    period_to = models.DateField("Дата по", null=True)
    date = models.DateField(null=True)


class SEO(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    keywords = models.CharField(max_length=255, null=True, blank=True)


class Requisites(SingletonModel):
    company_name = models.CharField(max_length=255)
    information = models.TextField(null=True, blank=True)


class WebsiteMainPage(SingletonModel):
    seo = models.ForeignKey(SEO, on_delete=models.CASCADE, null=True, blank=True)
    slide1 = models.ImageField(upload_to='images/', null=True, blank=True)
    slide2 = models.ImageField(upload_to='images/', null=True, blank=True)
    slide3 = models.ImageField(upload_to='images/', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class WebsiteMainPageBlocks(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class WebsiteAbout(SingletonModel):
    seo = models.ForeignKey(SEO, on_delete=models.CASCADE, null=True)
    poster = models.ImageField(upload_to='images/', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class WebsiteAboutGallery(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)


class WebsiteService(SingletonModel):
    seo = models.ForeignKey(SEO, on_delete=models.CASCADE, null=True)


class WebsiteServiceBlocks(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class WebsiteTariffs(SingletonModel):
    seo = models.ForeignKey(SEO, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)


class WebsiteTariffBlocks(models.Model):
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)


class WebsiteContacts(SingletonModel):
    seo = models.ForeignKey(SEO, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    site = models.URLField(null=True, blank=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    tel = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    map = models.CharField(max_length=255)


class Message(models.Model):
    destination = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='')
    addressee = models.CharField(default='Админ', max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255)
    text = models.TextField()
    indebtedness = models.BooleanField('', default=False)
    created_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.title

    def get_short_text(self):
        if len(self.text) > 50:
            return f'<b>{self.title}</b> - {self.text[:49]}...'
        else:
            return f'<b>{self.title}</b> - {self.text}'

    def get_long_date(self):
        return self.created_date.strftime('%d.%m.%Y')


class MasterRequest(models.Model):
    TYPE = (
        ('Сантехник', 'Сантехник'),
        ('Электрик', 'Электрик'),
        ('Слесарь', 'Слесарь'),
        ('Любой специалист', 'Любой специалист'),
    )
    STATUS = (
        ('Новое', 'Новое'),
        ('В работе', 'В работе'),
        ('Выполнено', 'Выполнено'),
    )
    date = models.DateField(blank=True, verbose_name='')
    time = models.TimeField(blank=True, verbose_name='')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owner', blank=True, verbose_name='', null=True)
    apartment = models.ForeignKey(Apartment, on_delete=models.CASCADE, blank=True, verbose_name='')
    master_type = models.CharField(choices=TYPE, max_length=155, blank=True, verbose_name='')
    status = models.CharField(choices=STATUS, max_length=155, blank=True, verbose_name='', default='Новое')
    master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='master', blank=True, verbose_name='', null=True)
    description = models.TextField(blank=True, verbose_name='')
    comment = models.TextField(blank=True, verbose_name='')

    def __str__(self):
        return self.description

    def get_full_time(self):
        return f'{self.date} - {self.time}'

