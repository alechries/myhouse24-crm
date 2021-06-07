from django.shortcuts import render, get_object_or_404, redirect
from _db import models, utils, auth
from django.db.models import Q
from django.contrib.auth import login, logout
from . import forms
from django.core.mail import send_mail
from . import utils as utility
from django.forms import modelformset_factory
from django.http import HttpResponse
from django.forms import inlineformset_factory
import xlwt


def index_view(request):
    new_user_count = models.User.objects.filter(status='Новый'),
    new_user_slice = {}
    if models.User.objects.filter(status='Новый').count() > 3:
        new_user_slice = models.User.objects.filter(status='Новый')[:2]
    elif 3 > models.User.objects.filter(status='Новый').count() > 0:
        new_user_slice = models.User.objects.filter(status='Новый')
        print(new_user_slice)
    context = {
        'new_user_count': new_user_count,
        'new_user_slice': new_user_slice,
        'user': request.user,
        'houses': models.House.objects.all().count(),
        'active_user': models.User.objects.filter(Q(is_active=True), Q(is_superuser=0)).count(),
        'master_request': models.MasterRequest.objects.filter(status='В работе').count(),
        'master_request_new': models.MasterRequest.objects.filter(status='Новое').count(),
        'apartment': models.Apartment.objects.all().count(),
        'account': models.Account.objects.all().count(),
    }

    statistic = utility.calculate_statistic()
    context.update(statistic)
    return render(request, 'admin/index.html', context)


def test_view(request):
    return render(request, 'admin/test.html')


def update_me_view(request):
    return render(request, 'admin/update-me.html')


def login_view(request):
    alerts = []

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        print(form.is_valid())
        if form.is_valid():
            user = auth.EmailAuthBackend.authenticate(email=form.cleaned_data['email'],
                                                      password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    print('user is:', request.user)
                    return redirect('admin_index')
                else:
                    alerts.append('User is not active')
            else:
                alerts.append('User does not exist')
        else:
            alerts.append('Data is incorrect')
    else:
        alerts.append('')
    return render(request, 'admin/login.html', {'form': forms.LoginForm(), 'alerts': alerts})


def logout_view(request):
    logout(request)
    return redirect('admin_login')


def export_tranfer_xls_view(request):
    return utils.model_to_xls(
        xls_name='account-transaction',
        xls_columns=['Number', 'Manager', 'Account', 'Transfer type', 'Amount', 'Comment', 'Payment made', 'Created date'],
        model_rows=models.Transfer.objects.all().values_list(
            'number', 'manager', 'account', 'transfer_type', 'amount', 'comment', 'payment_made', 'created_date'),
    )


def account_transaction_view(request):
    statistic = utility.calculate_statistic()
    accounts = models.Transfer.objects.all().order_by('-pk')
    context = {'accounts': accounts}
    context.update(statistic)
    context.update(utility.new_user())

    return render(request, 'admin/account-transaction/index.html', context)


def account_transaction_filter(request, pk):
    statistic = utility.calculate_statistic()
    accounts = models.Transfer.objects.filter(account_id=pk)
    context = {'accounts': accounts}
    context.update(statistic)
    context.update(utility.new_user())

    return render(request, 'admin/account-transaction/index.html', context)


# НЕ до конца реализованно копирование
def account_transaction_copy_view(request, pk):
    instance = models.Transfer.objects.get(id=pk)
    alerts = []
    if request.method == 'POST':
        form = forms.AccountTransactionForm(request.POST, instance=instance)

        if form.is_valid():
            form.save()
            alerts.append('Успешное создание новой формы')
        else:
            alerts.append('Не успешно')

    form = forms.AccountTransactionForm(request.POST, instance=instance)
    context = {'form': form}
    context.update(utility.new_user())
    return render(request, 'admin/account-transaction/create_in.html', context)


def account_transaction_detail_view(request, pk):
    transaction = models.Transfer.objects.get(id=pk)
    if transaction.account is not None and transaction.account.get_apartment():
        username = transaction.account.get_apartment().user
    else:
        username = None
    context = {'transaction': transaction,
               'username': username,
               }
    context.update(utility.new_user())
    return render(request, 'admin/account-transaction/detail.html', context)


def account_transaction_create_in_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.AccountTransactionForm(request.POST)
        if form.is_valid():
            transfer = form.save()
            if transfer.transfer_type_id is None:
                transfer.solo_status = 1

        form.save()
        alerts.append('Запись была успешно добавлена!')
    form = forms.AccountTransactionForm(initial={'number': utility.serial_number_transaction(), 'manager': models.User.objects.filter(role__cash_box_status=1).first()})
    form.fields['manager'].queryset = models.User.objects.filter(role__cash_box_status=1)
    form.fields['transfer_type'].queryset = models.TransferType.objects.filter(status='Приход')
    context = {'form': form,
               'alerts': alerts,
               }
    context.update(utility.new_user())
    return render(request, 'admin/account-transaction/create_in.html', context)


def account_transaction_create_out_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.AccountTransactionForm(request.POST)
        if form.is_valid():
            transfer = form.save()
            transfer.solo_status = 0
        form.save()
        alerts.append('Запись была успешно добавлена!')
    form = forms.AccountTransactionForm(initial={'number': utility.serial_number_transaction(),
                                                 'manager': models.User.objects.filter(role__cash_box_status=1).first()})
    form.fields['manager'].queryset = models.User.objects.filter(role__cash_box_status=1)
    form.fields['transfer_type'].queryset = models.TransferType.objects.filter(status='Расход')

    context = {'form': form,
               'alerts': alerts,
               }
    context.update(utility.new_user())
    return render(request, 'admin/account-transaction/create_out.html', context)


def account_transaction_change_view(request, pk):
    alerts = []
    if request.method == 'POST':
        form = forms.AccountTransactionForm(request.POST or None, instance=get_object_or_404(models.Transfer, id=pk))
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    else:
        form = forms.AccountTransactionForm(initial={'number': utility.serial_number_transaction(),
                                                     'manager': models.User.objects.filter(
                                                         role__cash_box_status=1).first()})
        form.fields['manager'].queryset = models.User.objects.filter(role__cash_box_status=1)
        form.fields['transfer_type'].queryset = models.TransferType.objects.filter(status='Расход')
    transfer = get_object_or_404(models.Transfer, id=pk)
    context = {'form': form,
               'alerts': alerts,
               }
    context.update(utility.new_user())
    if transfer.transfer_type_id is not None:
        if transfer.transfer_type.status == 'Приход':
            return render(request, 'admin/account-transaction/create_in.html', context)
        else:
            return render(request, 'admin/account-transaction/create_out.html', context)
    else:
        if transfer.solo_status is True:
            return render(request, 'admin/account-transaction/create_in.html', context)
        else:
            return render(request, 'admin/account-transaction/create_out.html', context)


def account_transaction_delete_view(request, pk):
    account_transaction = get_object_or_404(models.Transfer, id=pk)

    account_transaction.delete()
    return redirect('admin_account-transaction')


def invoice_view(request):
    invoices = models.Invoice.objects.all().order_by('-pk')
    context = {'invoices': invoices}
    context.update(utility.calculate_statistic())
    context.update(utility.new_user())

    return render(request, 'admin/invoice/index.html', context)


def invoice_filter_view(request, pk):
    invoices = models.Invoice.objects.filter(apartment__account_id=pk)
    context = {'invoices': invoices}
    context.update(utility.calculate_statistic())
    context.update(utility.new_user())

    return render(request, 'admin/invoice/index.html', context)


def invoice_create_view(request):
    TariffInvoiceFormset = inlineformset_factory(
        parent_model=models.Invoice,
        model=models.TariffService,
        form=forms.TariffInvoiceForm,
        max_num=1
    )
    meter = models.Meter.objects.all()
    print(meter)
    alerts = []
    if request.method == 'POST':
        invoice_form = forms.InvoiceForm(request.POST, prefix='invoice_form',)
        tariff_invoice_formset = TariffInvoiceFormset(request.POST, prefix='tariff_invoice_form')
        if invoice_form.is_valid() and tariff_invoice_formset.is_valid():
            invoice = invoice_form.save()
            tariff_invoice_queryset = tariff_invoice_formset.save(commit=False)
            total = 0
            for tariff_invoice_form in tariff_invoice_queryset:
                tariff_invoice_form.invoice.id = invoice.id
                total += float(tariff_invoice_form.price) * float(tariff_invoice_form.amount)
                tariff_invoice_form.save()
            invoice.total_amount = total
            if invoice.apartment.account:
                invoice.save()
                alerts.append('Квитанция сохранена')
            else:
                alerts.append('У квартиры нет счёта!')

    else:
        invoice_form = forms.InvoiceForm(request.POST or None, prefix='invoice_form', initial={'number': utility.invoice_number()})
        tariff_invoice_formset = TariffInvoiceFormset(request.POST or None, prefix='tariff_invoice_form')

    context = {
        'meter': meter,
        'invoice_form': invoice_form,
        'tariff_invoice_formset': tariff_invoice_formset,
        'alerts': alerts
    }
    context.update(utility.new_user())
    return render(request, 'admin/invoice/change.html', context)


def tariff_service_del(request, pk):
    tariff_service = models.TariffService.objects.get(id=pk)
    tariff_service.delete()
    return redirect('admin_invoice')

def invoice_copy_view(request):
    return render(request, 'admin/invoice/copy.html')


def invoice_change_view(request, pk=None):
    invoice = models.Invoice.objects.get(id=pk)
    service = models.TariffService.objects.filter(invoice=invoice)
    TaroffInvoiceFormset = inlineformset_factory(
        parent_model=models.Invoice,
        model=models.TariffService,
        form=forms.TariffInvoiceForm,
        max_num=service.count() if service.count() > 0 else 1
    )
    alerts = []
    if request.method == 'POST':
        invoice_form = forms.InvoiceForm(request.POST, prefix='invoice_form', instance=invoice)
        tariff_invoice_formset = TaroffInvoiceFormset(request.POST, prefix='tariff_invoice_form', instance=invoice)
        if invoice_form.is_valid() and tariff_invoice_formset.is_valid():
            tariff_invoice_queryset = tariff_invoice_formset.save(commit=False)
            total = 0
            for tariff_invoice_form in tariff_invoice_queryset:
                tariff_invoice_form.invoice.id = invoice.id
                total += float(tariff_invoice_form.price) * float(tariff_invoice_form.amount)
                tariff_invoice_form.save()
            invoice.total_amount = total
            invoice.save()
            alerts.append('Квитанция сохранена')

    else:
        invoice_form = forms.InvoiceForm(request.POST or None, prefix='invoice_form', instance=invoice)
        tariff_invoice_formset = TaroffInvoiceFormset(request.POST or None, prefix='tariff_invoice_form', instance=invoice)

    context = {
        'invoice_form': invoice_form,
        'tariff_invoice_formset': tariff_invoice_formset,
        'alerts': alerts
    }
    context.update(utility.new_user())
    return render(request, 'admin/invoice/change.html', context)


def invoice_detail_view(request, pk):
    invoice = models.Invoice.objects.get(id=pk)
    service = models.TariffService.objects.filter(invoice=invoice)

    for el in service:
        total = float(el.amount) * float(el.price)
    context = {'invoice': invoice,
               'service': service,
               }
    context.update(utility.new_user())
    return render(request, 'admin/invoice/detail.html', context)


def invoice_delete_view(request, pk):
    invoice = models.Invoice.objects.get(id=pk)
    invoice.delete()
    return redirect('admin_invoice')


def export_account_xls_view(request):
    return utils.model_to_xls(
        xls_name='account',
        xls_columns=['Wallet', 'Money', 'Status'],
        model_rows=models.Account.objects.all().values_list(
            'wallet', 'money', 'status'),
    )


def account_view(request):
    account = models.Account.objects.all().order_by('-pk')
    total_arrears = 0
    for el in account:
        el.money = 0
        transaction_in_balance = models.Transfer.objects.filter(Q(account_id=el.id), Q(transfer_type__status='Приход'))
        transaction_out_balance = models.Transfer.objects.filter(Q(account_id=el.id), Q(transfer_type__status='Расход'))
        for transfer_in in transaction_in_balance:
            el.money += transfer_in.amount

        for transfer_out in transaction_out_balance:
            el.money -= transfer_out.amount

    statistic = utility.calculate_statistic()
    context = {'account': account}
    context.update(statistic)
    context.update(utility.new_user())
    return render(request, 'admin/account/index.html', context)


def account_detail(request, pk):
    account = models.Account.objects.get(id=pk)
    context = {'account': account}
    context.update(utility.new_user())
    return render(request, 'admin/account/detail.html', context)


def account_create_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.AccountForm(request.POST)
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно добавлена!')
    form = forms.AccountForm(initial={'wallet': utility.serial_number_account()})


    context = {'form': form,
               'alerts': alerts,
               }
    context.update(utility.new_user())
    return render(request, 'admin/account/create.html', context)


def account_change_view(request, pk):
    alerts = []
    form = forms.AccountForm(request.POST or None, instance=get_object_or_404(models.Account, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')

    context = {'form': form,
               'alerts': alerts,
               }
    context.update(utility.new_user())
    return render(request, 'admin/account/create.html', context)


def account_delete_view(request, pk):
    account = get_object_or_404(models.Account, id=pk)
    account.delete()
    return redirect('admin_account')


def apartment_view(request):
    apartment = models.Apartment.objects.all()
    context = {'apartment': apartment}
    context.update(utility.new_user())
    return render(request, 'admin/apartment/index.html', context)


def apartment_detail_view(request, pk):
    apartment = get_object_or_404(models.Apartment, id=pk)
    account = models.Account.objects.filter(appartament_related=apartment)
    context = {'apartment': apartment,
               'account': account,
               }
    context.update(utility.new_user())
    return render(request, 'admin/apartment/detail.html', context)


def apartment_create_view(request):
    form = forms.ApartmentForm(request.POST)
    form.fields['user'].queryset = models.User.objects.filter(is_superuser=0)
    alerts = []
    if request.method == 'POST' and form.is_valid():
        form.save()
        alerts.append('Запись была успешно добавлена!')

    context = {'form': form,
               'alerts': alerts,
               }
    context.update(utility.new_user())
    return render(request, 'admin/apartment/create.html', context)


def apartment_change_view(request, pk):
    alerts = []
    if request.method == 'POST':
        form = forms.ApartmentForm(request.POST or None, instance=get_object_or_404(models.Apartment, id=pk))
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    else:
        form = forms.ApartmentForm(request.POST or None, instance=get_object_or_404(models.Apartment, id=pk))
        form.fields['user'].queryset = models.User.objects.filter(is_superuser=False)


    context = {'form': form,
               'alerts': alerts,
               }
    context.update(utility.new_user())
    return render(request, 'admin/apartment/create.html', context)


def apartment_delete_view(request, pk):
    alert = []
    apartment = get_object_or_404(models.Apartment, id=pk)
    apartment.delete()
    alert.append('Запись успешно удалена')
    return redirect('admin_apart',)


def user_view(request):
    users = models.User.objects.filter(is_superuser=0)
    context = {'users': users}
    context.update(utility.new_user())
    return render(request, 'admin/user/index.html', context)


def user_create_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.UserForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно добавлена!')
        else:
            alerts.append('Неуспешно')

    form = forms.UserForm(request.POST, request.FILES, initial={'status': "Активен"})
    context = {'form': form,
               'alerts': alerts,
               }
    context.update(utility.new_user())
    return render(request, 'admin/user/create.html', context)


def user_detail_view(request, pk):
    user = get_object_or_404(models.User, id=pk)
    apartment = models.Apartment.objects.filter(user_id=pk)
    print(apartment)
    context = {'user_detail': user,
               'apartment': apartment,
               }
    context.update(utility.new_user())
    return render(request, 'admin/user/detail.html', context)


def user_change_view(request, pk):
    alerts = []
    user = models.User.objects.get(id=pk)
    if request.method == 'POST':
        form = forms.UserForm(request.POST or None, instance=get_object_or_404(models.User, id=pk))
        if form.is_valid():
            form.save()
            alerts.append('Успех')
        else:
            alerts.append('Неуспешно')

    form = forms.UserForm(request.POST or None, instance=get_object_or_404(models.User, id=pk))

    context = {'form': form,
               'alerts': alerts,
               'current_user': user,
               }
    context.update(utility.new_user())
    return render(request, 'admin/user/create.html', context)


def user_delete_view(request, pk):
    user = get_object_or_404(models.User, id=pk)
    user.delete()
    return redirect('admin_user')


def user_invite_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.UserInviteForm(request.POST)
        if form.is_valid():
            form.save()
            alerts.append('Успех')
            user_email = models.UserInvite.get_solo().email
            send_mail('Приглашение в Demo CRM 24', 'Приглашение в CRM', 'dimadjangosendemail@gmail.com',
                      [user_email])
    else:
        form = forms.UserInviteForm()
    return render(request, 'admin/user/invite.html', {'form': form,
                                                      'alerts': alerts})


def house_view(request):
    houses = models.House.objects.all()
    context = {'houses': houses}
    context.update(utility.new_user())
    return render(request, 'admin/house/index.html', context)


def house_detail_view(request, pk):
    house = models.House.objects.get(id=pk)
    floors = models.Floor.objects.all()
    sections = models.Section.objects.filter(house_id=house.id)
    floor_count = 0
    user_count = models.UserHouse.objects.filter(house_id=house)
    if sections:
        for section in sections:
            for floor in floors:
                if floor.section_id == section.id:
                    floor_count += 1

    context = {'house': house,
               'sections': sections,
               'floor_count': floor_count,
               'user_count': user_count
               }
    context.update(utility.new_user())
    return render(request, 'admin/house/detail.html', context)


def house_edit_view(request, pk):
    house = models.House.objects.get(id=pk)
    floor = models.Floor.objects.filter(section__house=house)
    FloorFormset = modelformset_factory(
        model=models.Floor,
        form=forms.FloorForm,
        max_num=floor.count() if floor.count() > 0 else 1
    )
    UserFormset = inlineformset_factory(
        parent_model=models.House,
        model=models.UserHouse,
        form=forms.UserHouseForm,
        max_num=1
    )
    SectionFormset = inlineformset_factory(
        parent_model=models.House,
        model=models.Section,
        form=forms.SectionForm,
        max_num=1
    )
    aletrs = []
    if request.method == 'POST':

        floor_formset = FloorFormset(request.POST, prefix='floor_form', queryset=models.Floor.objects.filter(section__house=house))
        user_house_formset = UserFormset(request.POST, prefix='user_form', instance=house)
        house_form = forms.HouseForm(request.POST, request.FILES, prefix='house_form', instance=house)
        section_formset = SectionFormset(request.POST, prefix='section_form', instance=house)
        if house_form.is_valid() and section_formset.is_valid() and user_house_formset.is_valid() and floor_formset.is_valid():
            house = house_form.save()
            section_queryset = section_formset.save(commit=False)
            user_house_queryset = user_house_formset.save(commit=False)

            for section in section_queryset:
                section.house.id = house.id
                section.save()

            for user_form in user_house_queryset:
                user_form.house.id = house.id
                user_form.save()

            if utils.forms_save([
                floor_formset
            ]):

                aletrs = ['Формы сохранены']

    else:
        floor_formset = FloorFormset(prefix='floor_form', queryset=models.Floor.objects.filter(section__house=house))
        for form in floor_formset:
            if house.get_section() is not None:
                form.fields['section'].queryset = models.Section.objects.filter(house=house)
            else:
                pass
        house_form = forms.HouseForm(prefix='house_form', instance=house)
        section_formset = SectionFormset(prefix='section_form', instance=house)
        user_house_formset = UserFormset(prefix='user_form', instance=house)
        for form in user_house_formset:
            form.fields['user'].queryset = models.User.objects.filter(is_superuser=1)

    context = {
        'floor_formset': floor_formset,
        'user_house_formset': user_house_formset,
        'house_form': house_form,
        'section_formset': section_formset,
        'alerts': aletrs,
        'house': house
    }
    context.update(utility.new_user())
    return render(
        request, 'admin/house/edit.html', context)


def house_create_view(request):
    SectionFormset = inlineformset_factory(
        parent_model=models.House,
        model=models.Section,
        fields=('name',),
        form=forms.SectionForm,
        max_num=1
    )
    aletrs = []
    if request.method == 'POST':
        house_form = forms.HouseForm(request.POST, request.FILES, prefix='house_form')
        section_formset = SectionFormset(request.POST, prefix='section_form')
        if house_form.is_valid() and section_formset.is_valid():
            house = house_form.save()
            section_queryset = section_formset.save(commit=False)

            for section in section_queryset:
                section.house.id = house.id
                section.save()

            aletrs = ['Формы сохранены']

    else:
        house_form = forms.HouseForm(prefix='house_form')
        section_formset = SectionFormset(prefix='section_form')

    context = {
        'house_form': house_form,
        'section_formset': section_formset,
        'alerts': aletrs
    }
    context.update(utility.new_user())
    return render(
        request, 'admin/house/create.html', context)


def section_delete_view(request, pk):
    section = get_object_or_404(models.Section, id=pk)
    section.delete()
    return HttpResponse()


def user_house_delete_view(request, pk):
    user = get_object_or_404(models.UserHouse, id=pk)
    user.delete()
    return HttpResponse()


def floor_delete_view(request, pk):
    floor = get_object_or_404(models.Floor, id=pk)
    floor.delete()
    return HttpResponse()


def house_delete_view(request, pk):
    house = get_object_or_404(models.House, id=pk)
    house.delete()
    return redirect('admin_house')


def message_view(request):
    messages = models.MessageRecipient.objects.all().order_by('-pk')
    context = {'messages': messages}
    context.update(utility.new_user())
    return render(request, 'admin/message/index.html', context)


def message_create_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.MessageCreateForm(request.POST)
        print(form.data)
        if form.is_valid():
            house = form.cleaned_data['house']
            section = form.cleaned_data['section']
            floor = form.cleaned_data['floor']
            apartment = form.cleaned_data['apartment']



            if apartment:
                instance = form.save()
            elif floor:
                apartments = models.Apartment.objects.filter(floor=floor)
                for apart in apartments:
                    instance = form.save(commit=False)
                    instance.apartment = apart
                    instance.save()
            elif section:
                floors = models.Floor.objects.filter(section=section)
                for floor in floors:
                    apartments = models.Apartment.objects.filter(floor=floor)
                    for apart in apartments:
                        instance = form.save(commit=False)
                        instance.apartment = apart
                        instance.save()
            elif house:
                sections = models.Section.objects.filter(house=house)
                for section in sections:
                    floors = models.Floor.objects.filter(section=section)
                    for floor in floors:
                        apartments = models.Apartment.objects.filter(floor=floor)
                        for apart in apartments:
                            instance = form.save(commit=False)
                            instance.apartment = apart
                            instance.save()


            alerts.append('Сообщение отправлено')
        else:
            alerts.append('Произошла ошибка')

    form = forms.MessageCreateForm()
    context = {'form': form,
               'alerts': alerts}
    context.update(utility.new_user())
    return render(request, 'admin/message/create.html', context)


def message_indebtedness_create_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.MessageCreateForm(request.POST)
        if form.is_valid():
            form.save()
            alerts.append('Сообщение отправлено')
        else:
            alerts.append('Произошла ошибка')

    form = forms.MessageCreateForm(initial={'indebtedness': True})
    context = {'form': form,
               'alerts': alerts}
    context.update(utility.new_user())
    return render(request, 'admin/message/create.html', context)


def message_detail_view(request, pk):
    message = get_object_or_404(models.MessageRecipient, id=pk)
    context = {'message': message}
    context.update(utility.new_user())
    return render(request, 'admin/message/detail.html', context)


def message_delete_view(request, pk):
    message = get_object_or_404(models.MessageRecipient, id=pk)
    message.delete()
    return redirect('admin_message')


def master_request_view(request):
    requests = models.MasterRequest.objects.all()
    context = {'requests': requests}
    context.update(utility.new_user())
    return render(request, 'admin/master-request/index.html', context)


def master_request_detail_view(request, pk):
    master_request = models.MasterRequest.objects.get(id=pk)
    context = {'master_request': master_request}
    context.update(utility.new_user())
    return render(request, 'admin/master-request/detail.html', context)


def master_request_create_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.MasterRequestForm(request.POST)
        if form.is_valid():
            form.save()
            alerts.append('Заявка создана')
        else:
            alerts.append('Произошла ошибка')
    else:
        form = forms.MasterRequestForm()
        form.fields['owner'].queryset = models.User.objects.filter(is_superuser=0)
        form.fields['master'].queryset = models.User.objects.filter(role__master_request_status=1)

    context = {'form': form,
               'alerts': alerts}
    context.update(utility.new_user())
    return render(request, 'admin/master-request/create.html', context)


def master_request_change_view(request, pk):
    alerts = []
    if request.method == 'POST':
        form = forms.MasterRequestForm(request.POST or None, instance=get_object_or_404(models.MasterRequest, id=pk))
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    else:
        form = forms.MasterRequestForm(request.POST or None, instance=get_object_or_404(models.MasterRequest, id=pk))
        form.fields['owner'].queryset = models.User.objects.filter(is_superuser=0)
        form.fields['master'].queryset = models.User.objects.filter(role__master_request_status=1)

    context = {'form': form,
               'alerts': alerts}
    context.update(utility.new_user())
    return render(request, 'admin/master-request/create.html', context)


def master_request_delete_view(request, pk):
    request = get_object_or_404(models.MasterRequest, id=pk)
    request.delete()
    return redirect('admin_master-request')


def counters_view(request):
    counters = models.Meter.objects.all()  # .order_by('service__name').distinct('service__name') POSTGRES

    context = {'counters': counters}
    context.update(utility.new_user())
    return render(request, 'admin/meter-data/counters.html', context)


def counter_filter(request, pk):
    counters = models.Meter.objects.filter(apartment__account_id=pk)
    apartment = models.Apartment.objects.get(account_id=pk)

    context = {'counters': counters,
               'apartment': apartment
               }
    context.update(utility.new_user())
    return render(request, 'admin/meter-data/apartment_detail.html', context)


def counter_house_view(request, pk):
    counters = models.Meter.objects.filter(apartment_id=pk)
    apartment = models.Apartment.objects.get(id=pk)

    context = {'counters': counters,
               'apartment': apartment
               }
    context.update(utility.new_user())
    return render(request, 'admin/meter-data/apartment_detail.html', context)


def meter_data_create_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.CounterForm(request.POST)
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно добавлена!')
        else:
            alerts.append('Неуспешно')
    form = forms.CounterForm(initial={'number': utility.counter_number()})
    form.fields['service'].queryset = models.Service.objects.filter(active=1)

    context = {'form': form,
               'alerts': alerts
               }
    context.update(utility.new_user())
    return render(request, 'admin/meter-data/create.html', context)


def meter_data_change_view(request, pk):
    alerts = []
    form = forms.CounterForm(request.POST or None, instance=get_object_or_404(models.Meter, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')

    context = {'form': form,
               'alerts': alerts
               }
    return render(request, 'admin/meter-data/create.html', context)


def meter_data_detail_view(request, pk):
    meter = models.Meter.objects.get(id=pk)

    context = {'meter': meter}
    context.update(utility.new_user())
    return render(request, 'admin/meter-data/detail.html', context)


def meter_data_delete_view(request, pk):
    meter = get_object_or_404(models.Meter, id=pk)
    meter.delete()
    return redirect('admin_counters-view')


def website_main_page_view(request):

    alerts = []
    MainPageBlockFormset = modelformset_factory(
        model=models.WebsiteMainPageBlocks,
        form=forms.WebsiteMainPageBlocksForm,
        max_num=6,
        min_num=6
    )
    main_page: models.WebsiteMainPage = models.WebsiteMainPage.get_solo()
    if request.method == 'POST':
        main_page_form = forms.WebsiteMainPageForm(
            request.POST, request.FILES,
            prefix='main_page_form',
            instance=main_page,
        )
        main_page_block_formset = MainPageBlockFormset(
            request.POST, request.FILES,
            prefix='main_page_block_form',
        )
        main_page_seo_form = forms.SEOForm(
            request.POST,
            prefix='main_page_seo_form',
        )

        if utils.forms_save([
            main_page_form,
            main_page_seo_form,
            main_page_block_formset,
        ]):
            alerts.append('Данные сохранены успешно!')

    else:
        if not main_page.seo:
            main_page.seo = models.SEO.objects.create()
            main_page.save()

        main_page_form = forms.WebsiteMainPageForm(
            instance=main_page,
            prefix='main_page_form',
        )

        main_page_block_formset = MainPageBlockFormset(
            prefix='main_page_block_form',
        )

        main_page_seo_form = forms.SEOForm(
            instance=main_page.seo,
            prefix='main_page_seo_form',
        )

    context = {
        'alerts': alerts,
        'main_page_form': main_page_form,
        'main_page_block_formset': main_page_block_formset,
        'main_page_seo_form': main_page_seo_form,
    }
    context.update(utility.new_user())
    return render(request, 'admin/website/main-page.html', context)


def website_about_gallery_delete_view(request, pk):
    entry = models.WebsiteAboutGallery.objects.get(id=pk)
    entry.delete()
    return HttpResponse()


def website_about_view(request):

    alerts = []
    about_gallery_count = models.WebsiteAboutGallery.objects.count()
    WebsiteAboutGalleryFormset = modelformset_factory(
        model=models.WebsiteAboutGallery,
        form=forms.WebsiteAboutGalleryForm,
        max_num=about_gallery_count if about_gallery_count > 0 else 1,
    )

    if request.method == 'POST':

        about_form = forms.WebsiteAboutForm(
            request.POST, request.FILES,
            prefix='about_form',
        )
        about_gallery_formset = WebsiteAboutGalleryFormset(
            request.POST, request.FILES,
            prefix='about_gallery_form',
        )
        about_seo_form = forms.SEOForm(
            request.POST,
            prefix='about_seo_form',
        )

        if utils.forms_save([
            about_form,
            about_seo_form,
            about_gallery_formset,
        ]):
            alerts.append('Данные сохранены успешно!')

    else:
        about: models.WebsiteAbout = models.WebsiteAbout.get_solo()
        if not about.seo:
            about.seo = models.SEO.objects.create()
            about.save()

        about_form = forms.WebsiteAboutForm(
            instance=about,
            prefix='about_form',
        )

        about_gallery_formset = WebsiteAboutGalleryFormset(
            prefix='about_gallery_form',
        )

        about_seo_form = forms.SEOForm(
            instance=about.seo,
            prefix='about_seo_form',
        )

    context = {
        'alerts': alerts,
        'about_form': about_form,
        'about_gallery_formset': about_gallery_formset,
        'about_seo_form': about_seo_form,
    }
    context.update(utility.new_user())
    return render(request, 'admin/website/about.html', context)


def website_services_blocks_delete_view(request, pk):
    entry = models.WebsiteServiceBlocks.objects.get(id=pk)
    entry.delete()
    return HttpResponse()


def website_services_view(request):
    service_count = models.WebsiteServiceBlocks.objects.count()
    MainPageServiceBlocksFormset = modelformset_factory(
        model=models.WebsiteServiceBlocks,
        form=forms.WebsiteServiceBlocksForm,
        fields=('image', 'name', 'description'),
        max_num=service_count if service_count > 0 else 1,
    )

    alerts = []
    if request.method == "POST":
        service_formset = MainPageServiceBlocksFormset(
            request.POST, request.FILES,
            prefix='service')
        utils.form_save(service_formset)
        seo_form = forms.SEOForm(request.POST, prefix='SEO')
        alerts.append('Услуги сохранены успешно!')

    else:
        service_formset = MainPageServiceBlocksFormset(prefix='service')
        service_instance = models.WebsiteService.get_solo()
        if not service_instance.seo:
            service_instance.seo = models.SEO.objects.create()
            service_instance.save()
        seo_form = forms.SEOForm(instance=service_instance.seo, prefix='SEO')

    context = {
        'formset': service_formset,
        'seo_form': seo_form,
        'alerts': alerts,
    }
    context.update(utility.new_user())
    return render(
        request, 'admin/website/services.html', context)


def website_tariffs_blocks_delete_view(request, pk):
    entry = models.WebsiteTariffBlocks.objects.get(id=pk)
    entry.delete()
    return HttpResponse()


def website_tariffs_view(request):
    tariffs_count = models.WebsiteTariffBlocks.objects.count()
    TariffsBlockFormset = modelformset_factory(
        model=models.WebsiteTariffBlocks,
        form=forms.WebsiteTariffsBlocksForm,
        max_num=tariffs_count if tariffs_count > 0 else 1,
    )

    alerts = []
    if request.method == 'POST':

        tariffs_form = forms.WebsiteTariffsForm(
            request.POST, request.FILES,
            prefix='tariffs_form',
        )
        tariffs_block_formset = TariffsBlockFormset(
            request.POST, request.FILES,
            prefix='tariffs_block_form',
        )
        tariffs_seo_form = forms.SEOForm(
            request.POST,
            prefix='tariffs_seo_form',
        )

        if utils.forms_save([
            tariffs_form,
            tariffs_block_formset,
            tariffs_seo_form,
        ]):
            alerts.append('Данные сохранены успешно!')

    else:
        tariffs: models.WebsiteTariffs = models.WebsiteTariffs.get_solo()

        if not tariffs.seo:
            tariffs.seo = models.SEO.objects.create()
            tariffs.save()

        tariffs_form = forms.WebsiteTariffsForm(
            instance=tariffs,
            prefix='tariffs_form',
        )

        tariffs_block_formset = TariffsBlockFormset(
            prefix='tariffs_block_form',
        )

        tariffs_seo_form = forms.SEOForm(
            instance=tariffs.seo,
            prefix='tariffs_seo_form',
        )

    context = {
        'alerts': alerts,
        'tariffs_form': tariffs_form,
        'tariffs_block_formset': tariffs_block_formset,
        'tariffs_seo_form': tariffs_seo_form,
    }
    context.update(utility.new_user())
    return render(request, 'admin/website/tariffs.html', context)


def website_contact_view(request):

    alerts = []
    if request.method == "POST":
        contact_form = forms.WebsiteContactsForm(request.POST, prefix='contacts')
        contact_seo_form = forms.SEOForm(request.POST, prefix='SEO')
        if utils.forms_save([
            contact_form,
            contact_seo_form,
        ]):
            alerts.append('Данные сохранены успешно!')

    else:
        contacts: models.WebsiteContacts = models.WebsiteContacts.get_solo()
        if not contacts.seo:
            contacts.seo = models.SEO.objects.create()
            contacts.save()
        contact_form = forms.WebsiteContactsForm(
            instance=contacts,
            prefix='contacts',
        )
        contact_seo_form = forms.SEOForm(
            instance=contacts.seo,
            prefix='SEO',
        )
    context = {
        'contact_form': contact_form,
        'contact_seo_form': contact_seo_form,
        'alerts': alerts,
    }
    context.update(utility.new_user())
    return render(request, 'admin/website/contact.html', context)


def services_view(request):
    alerts = []
    service_count = models.Service.objects.all().count()
    measure_count = models.Measure.objects.all().count()
    ServiceFormset = modelformset_factory(
        model=models.Service,
        form=forms.ServiceForm,
        max_num=service_count if service_count > 0 else 1,

    )
    MeasureFormset = modelformset_factory(
        model=models.Measure,
        form=forms.MeasureForm,
        max_num=measure_count if measure_count > 0 else 1,
    )

    if request.method == 'POST':

        service_formset = ServiceFormset(
            request.POST,
            prefix='service_form',
        )
        measure_formset = MeasureFormset(
            request.POST,
            prefix='measure_form'
        )

        if utils.forms_save([
            measure_formset,
            service_formset,
        ]):
            alerts.append('Данные сохранены успешно!')
        return redirect('admin_services')

    else:
        service_formset = ServiceFormset(
            prefix='service_form',
        )
        measure_formset = MeasureFormset(
            prefix='measure_form'
        )

    context = {
        'alerts': alerts,
        'service_formset': service_formset,
        'measure_formset': measure_formset,
    }
    context.update(utility.new_user())
    return render(request, 'admin/services/services.html', context)


def services_del_view(request, pk):
    entry = models.Service.objects.get(id=pk)
    entry.delete()
    return HttpResponse()


def measure_del_view(request, pk):
    entry = models.Measure.objects.get(id=pk)
    entry.delete()
    return HttpResponse()


def tariffs_view(request):
    context = {
        'tariff': models.Tariff.objects.all(),
    }
    context.update(utility.new_user())
    return render(request, 'admin/tariffs/index.html', context)


def tariffs_create_view(request):
    TariffServiceFormset = inlineformset_factory(
        parent_model=models.Tariff,
        model=models.TariffService,
        form=forms.TariffServiceForm,
        max_num=1
    )
    aletrs = []
    if request.method == 'POST':
        tariff_form = forms.TariffCreateForm(request.POST, prefix='tariff_form')
        tariff_service_formset = TariffServiceFormset(request.POST, prefix='tariff_service_form')
        if tariff_form.is_valid() and tariff_service_formset.is_valid():
            tariff = tariff_form.save()
            tariff_service_queryset = tariff_service_formset.save(commit=False)


            for tariff_section_form in tariff_service_queryset:
                tariff_section_form.tariff.id = tariff.id
                tariff_section_form.save()

            aletrs = ['Формы сохранены']

    else:
        tariff_form = forms.TariffCreateForm(prefix='tariff_form')
        tariff_service_formset = TariffServiceFormset(prefix='tariff_service_form')

    context = {
        'tariff_form': tariff_form,
        'tariff_service_formset': tariff_service_formset,
        'alerts': aletrs
    }
    context.update(utility.new_user())
    return render(
        request, 'admin/tariffs/create.html',
        context
    )


def tariffs_change_view(request, pk=None):
    tariff = models.Tariff.objects.get(id=pk)
    tariff_service_count = models.TariffService.objects.filter(tariff=tariff).count()
    TariffServiceFormset = inlineformset_factory(
        parent_model=models.Tariff,
        model=models.TariffService,
        fields=('price', 'service'),
        widgets={
            'price': forms.TextInput(attrs={
                'placeholder': 'Введите цену',
                'type': 'text',
                'class': 'form-control',
                'style': 'margin: 0.25rem 0',
            }),

        },
        form=forms.TariffServiceForm,
        max_num=tariff_service_count if tariff_service_count > 0 else 1
    )
    aletrs = []
    if request.method == 'POST':
        tariff_form = forms.TariffCreateForm(request.POST, prefix='tariff_form', instance=tariff)
        tariff_service_formset = TariffServiceFormset(request.POST, prefix='tariff_service_form', instance=tariff)
        if tariff_form.is_valid() and tariff_service_formset.is_valid():
            tariff = tariff_form.save()
            tariff_service_queryset = tariff_service_formset.save(commit=False)

            for tariff_section_form in tariff_service_queryset:
                tariff_section_form.tariff.id = tariff.id
                tariff_section_form.save()

            aletrs = ['Формы сохранены']

    else:
        tariff_form = forms.TariffCreateForm(prefix='tariff_form', instance=tariff)
        tariff_service_formset = TariffServiceFormset(prefix='tariff_service_form', instance=tariff)

    context = {
        'tariff_form': tariff_form,
        'tariff_service_formset': tariff_service_formset,
        'alerts': aletrs
    }
    context.update(utility.new_user())
    return render(
        request, 'admin/tariffs/create.html',
        context
    )


def tariffs_copy_view(request, pk):
    tariff = models.Tariff.objects.get(id=pk)
    tariff_service_count = models.TariffService.objects.filter(tariff=tariff).count()
    TariffServiceFormset = inlineformset_factory(
        parent_model=models.Tariff,
        model=models.TariffService,
        fields=('price', 'service'),
        widgets={
            'price': forms.TextInput(attrs={
                'placeholder': 'Введите цену',
                'type': 'text',
                'class': 'form-control',
                'style': 'margin: 0.25rem 0',
            }),

        },
        form=forms.TariffServiceForm,
        max_num=tariff_service_count if tariff_service_count > 0 else 1
    )
    aletrs = []
    if request.method == 'POST':
        tariff_form = forms.TariffCreateForm(request.POST, prefix='tariff_form', instance=tariff)
        tariff_service_formset = TariffServiceFormset(request.POST, prefix='tariff_service_form', instance=tariff)
        tariff_form.instance.pk = None
        if tariff_form.is_valid() and tariff_service_formset.is_valid():
            tariff = tariff_form.save()
            tariff_service_queryset = tariff_service_formset.save(commit=False)

            for tariff_section_form in tariff_service_queryset:
                tariff_section_form.tariff.id = tariff.id
                tariff_section_form.save()

            aletrs = ['Формы сохранены']

    else:
        tariff_form = forms.TariffCreateForm(prefix='tariff_form', instance=tariff)
        tariff_service_formset = TariffServiceFormset(prefix='tariff_service_form', instance=tariff)

    context = {
        'tariff_form': tariff_form,
        'tariff_service_formset': tariff_service_formset,
        'alerts': aletrs
    }
    context.update(utility.new_user())
    return render(
        request, 'admin/tariffs/create.html',
        context
    )


def tariff_detail_view(request, pk):
    tariff = models.Tariff.objects.get(id=pk)
    tariff_service = models.TariffService.objects.filter(tariff=tariff)

    context = {'tariff': tariff,
               'tariff_service': tariff_service
               }
    context.update(utility.new_user())
    return render(request, 'admin/tariffs/detail.html', context)


def tariffs_delete_view(request, pk):
    entry = models.Tariff.objects.get(id=pk)
    entry.delete()
    return redirect('admin_tariffs')


def tariffs_service_delete_view(request, pk):
    service = models.TariffService.objects.get(id=pk)
    invoice = models.Invoice.objects.get(id=service.invoice_id)
    invoice.total_amount = float(invoice.total_amount) - (float(service.amount) * float(service.price))
    invoice.save()
    service.delete()
    return HttpResponse()


def user_admin_role_view(request):

    alerts = []
    UserRoleFormset = modelformset_factory(
        model=models.UserRole,
        form=forms.RoleForm,
        max_num=5,
        min_num=5
    )

    if request.method == 'POST':

        user_role_formset = UserRoleFormset(
            request.POST,
            prefix='user_role_form',
        )

        if utils.forms_save([
            user_role_formset,
        ]):
            alerts.append('Данные сохранены успешно!')
        return redirect('admin_user-admin-role')

    else:
        user_role_formset = UserRoleFormset(
            prefix='user_role_form',
        )

    context = {
        'alerts': alerts,
        'user_role_formset': user_role_formset
    }
    context.update(utility.new_user())
    return render(request, 'admin/user-admin/role.html', context)


def user_admin_users_list(request):
    users_list = models.User.objects.filter(is_superuser=1)
    context = {'users_list': users_list}
    context.update(utility.new_user())
    return render(request, 'admin/user-admin/list.html', context)


def user_admin_mail_send(request, pk):
    user_email = models.User.objects.get(id=pk).email
    send_mail('Приглашение в Demo CRM 24', 'Приглашение в CRM', 'dimadjangosendemail@gmail.com',
              [user_email])
    return redirect('admin_user-users-list')


def user_admin_create_view(request):
    form = forms.UserCreateForm(request.POST or None)
    form.instance.is_superuser = 1
    if request.method == 'POST' and form.is_valid():
        form.instance.is_superuser = 1
        form.save()
        return redirect('admin_user-users-list')
    context = {'form': form}
    context.update(utility.new_user())
    return render(request, 'admin/user-admin/create.html', context)


def user_admin_change_view(request, pk):
    user = models.User.objects.get(id=pk)
    alerts = []
    form = forms.UserCreateForm(request.POST or None, instance=user)

    if request.method == 'POST' and form.is_valid():
        form.instance.is_superuser = 1
        form.save()
        alerts.append('Успех')

    context = {'form': form,
               'alerts': alerts}
    context.update(utility.new_user())
    return render(request, 'admin/user-admin/create.html', context)


def user_admin_detail_view(request, pk):
    user = models.User.objects.get(id=pk)
    context = {'current_user': user}
    context.update(utility.new_user())
    return render(request, 'admin/user-admin/detail.html', context)


def user_admin_delete_view(request, pk):
    return redirect('admin_master-request')


def pay_company_view(request):
    alerts = []
    form = forms.PaymentCompany(request.POST or None, instance=models.Requisites.get_solo())
    if request.method == 'POST' and form.is_valid():
        form.save()
        alerts.append('Успех!')
        return redirect('admin_pay-company')
    context = {'form': form,
               'alerts': alerts}
    context.update(utility.new_user())
    return render(request, 'admin/pay-company.html', context)


def transaction_purpose_view(request):
    transfer_type = models.TransferType.objects.all()
    context = {'transfer_type': transfer_type}
    context.update(utility.new_user())
    return render(request, 'admin/transaction-purpose/index.html', context)


def transaction_purpose_create_view(request):
    form = forms.TransactionPurposeForm(request.POST)
    alerts = []
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно добавлена!')
        else:
            alerts.append('Неуспешно')

    context = {'form': form,
               'alerts': alerts}
    context.update(utility.new_user())
    return render(request, 'admin/transaction-purpose/create.html', context)


def transaction_purpose_change_view(request, pk):
    alerts = []
    form = forms.TransactionPurposeForm(request.POST or None, instance=get_object_or_404(models.TransferType, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Успех')
        else:
            alerts.append('Неуспешно')

    context = {'form': form,
               'alerts': alerts}
    context.update(utility.new_user())
    return render(request, 'admin/transaction-purpose/create.html', context)


def transaction_purpose_delete_view(request, pk):
    transfer_type = get_object_or_404(models.TransferType, id=pk)
    transfer_type.delete()
    return redirect('admin_transaction-purpose')

