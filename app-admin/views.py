from django.shortcuts import render, get_object_or_404
from _db import models, utils
from . import forms
from django.forms import modelformset_factory
from .utils import serial_number_transfer


def index_view(request):
    return render(request, 'admin/index.html')


def update_me_view(request):
    return render(request, 'admin/update-me.html')


def login_view(request):
    return render(request, 'admin/login.html')


def logout_view(request):
    return render(request, 'admin/logout.html')


def account_transaction_view(request):
    accounts = models.Transfer.objects.all()
    return render(request, 'admin/account-transaction/index.html', {'accounts':accounts})


def account_transaction_detail_view(request, pk):
    transaction = models.Transfer.objects.filter(id=pk)
    return render(request, 'admin/account-transaction/detail.html', {'transaction':transaction})


def account_transaction_create_in_view(request):
    form = forms.AccountTransactionForm(request.POST)
    serial_number = serial_number_transfer()
    print(serial_number)
    alerts = []
    if request.method == 'POST' and form.is_valid():
        form.transfer_type = 1
        form.save()
        alerts.append('Запись была успешно добавлена!')

    return render(request, 'admin/account-transaction/create_in.html', {'form': form,
                                                                        'serial_number': serial_number,
                                                                        'alerts': alerts,
                                                                        })


def account_transaction_create_out_view(request):
    form = forms.AccountTransactionForm(request.POST)
    form.transfer_type = 0
    print(form.transfer_type)
    alerts = []
    if request.method == 'POST' and form.is_valid():
        form.type = 0
        print(form.is_valid())
        form.save()
        alerts.append('Запись была успешно добавлена!')

    return render(request, 'admin/account-transaction/create_out.html', {'form': form,
                                                                         'alerts': alerts,
                                                                          })


def account_transaction_change_view(request, pk):
    alerts = []
    form = forms.AccountTransactionForm(request.POST or None, instance=get_object_or_404(models.Transfer, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    transfer = get_object_or_404(models.Transfer, id=pk)
    if transfer.transfer_type.status == 0:
        return render(request, 'admin/account-transaction/create_in.html', {'form': form,
                                                                            'alerts': alerts,
                                                                            })
    else:
        return render(request, 'admin/account-transaction/create_out.html', {'form': form,
                                                                             'alerts': alerts,
                                                                             })


def account_transaction_delete_view(request, pk):
    account_transaction = get_object_or_404(models.Transfer, id=pk)
    account_transaction.delete()
    return render(request, 'admin/account-transaction/index.html')


def invoice_view(request):
    return render(request, 'admin/invoice/index.html')


def invoice_create_view(request):
    return render(request, 'admin/invoice/create.html')


def invoice_copy_view(request):
    return render(request, 'admin/invoice/copy.html')


def invoice_change_view(request):
    return render(request, 'admin/invoice/change.html')


def invoice_delete_view(request):
    return render(request, 'admin/invoice/delete.html')


def account_view(request):
    account = models.Account.objects.all()
    return render(request, 'admin/account/index.html', {'account': account})


def account_detail(request, pk):
    account = models.Account.objects.filter(id=pk)
    print(account)
    return render(request, 'admin/account/detail.html', {'account': account})


def account_create_view(request):
    form = forms.AccountForm(request.POST)
    alerts = []
    if request.method == 'POST' and form.is_valid():
        form.save()
        alerts.append('Запись была успешно добавлена!')

    return render(request, 'admin/account/create.html', {'form': form,
                                                         'alerts': alerts
                                                         })


def account_change_view(request, pk):
    alerts = []
    form = forms.AccountForm(request.POST or None, instance=get_object_or_404(models.Account, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    return render(request, 'admin/account/create.html', {'form': form,
                                                         'alerts': alerts})


def account_delete_view(request, pk):
    account = get_object_or_404(models.Account, id=pk)
    account.delete()
    return render(request, 'admin/account/delete.html')


def apartment_view(request):
    apartment = models.Apartment.objects.all()
    return render(request, 'admin/apartment/index.html',{'apartment': apartment})


def apartment_detail_view(request, pk):
    apartment = get_object_or_404(models.Apartment, id=pk)
    return render(request, 'admin/apartment/detail.html', {'apartment': apartment})


def apartment_create_view(request):
    form = forms.ApartmentForm(request.POST)
    alerts = []
    if request.method == 'POST' and form.is_valid():
        form.save()
        alerts.append('Запись была успешно добавлена!')

    return render(request, 'admin/apartment/create.html', {'form': form,
                                                           'alerts': alerts})


def apartment_change_view(request, pk):
    alerts = []
    form = forms.ApartmentForm(request.POST or None, instance=get_object_or_404(models.Apartment, id=pk))
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно редактирована!')
    return render(request, 'admin/apartment/create.html', {'form': form,
                                                           'alerts': alerts})


def apartment_delete_view(request, pk):
    alert = []
    apartment = get_object_or_404(models.Apartment, id=pk)
    apartment.delete()
    alert.append('Запись успешно удалена')
    return render(request, 'admin/apartment/delete.html',)


def user_view(request):
    users = models.User.objects.all()
    return render(request, 'admin/user/index.html', {'users': users})


def user_create_view(request):
    form = forms.UserForm(request.POST, request.FILES)
    alerts = []
    if request.method == 'POST':
        print(form.data)
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно добавлена!')
        else:
            alerts.append('Неуспешно')

    return render(request, 'admin/user/create.html', {'form': form,
                                                      'alerts': alerts
                                                      })


def user_detail_view(request, pk):
    user = get_object_or_404(models.User, id=pk)
    return render(request, 'admin/user/detail.html', {'user': user})


def user_change_view(request, pk):
    alerts = []
    form = forms.UserForm(request.POST or None, instance=get_object_or_404(models.User, id=pk))
    if request.method == 'POST':
        print(form.data)
        if form.is_valid():
            form.save()
            alerts.append('Успех')
        else:
            alerts.append('Неуспешно')
    return render(request, 'admin/user/create.html', {'form': form,
                                                      'alerts': alerts})



def user_delete_view(request):
    return render(request, 'admin/user/delete.html')


def house_view(request):
    houses = models.House.objects.all()
    return render(request, 'admin/house/index.html', {'houses': houses})


def house_create_view(request):
    form = forms.HouseForm(request.POST, request.FILES)
    alerts = []
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Форма сохранена успешно')
        else:
            alerts.append('Произошла ошибка')

    return render(request, 'admin/house/create.html', {'form': form,
                                                       'alerts': alerts})


def house_change_view(request):
    return render(request, 'admin/house/change.html')


def house_delete_view(request):
    return render(request, 'admin/house/delete.html')


def message_view(request):
    messages = models.Message.objects.all()
    return render(request, 'admin/message/index.html', {'messages': messages})


def message_create_view(request):
    form = forms.MessageCreateForm(request.POST)
    alerts = []
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Сообщение отправлено')
        else:
            alerts.append('Произошла ошибка')
    return render(request, 'admin/message/create.html', {'form': form,
                                                         'alerts': alerts})


def message_change_view(request):
    return render(request, 'admin/message/change.html')


def message_delete_view(request):
    return render(request, 'admin/message/delete.html')


def master_request_view(request):
    requests = models.MasterRequest.objects.all()
    return render(request, 'admin/master-request/index.html', {'requests': requests})


def master_request_create_view(request):
    form = forms.MasterRequestForm(request.POST)
    alerts = []
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Сообщение отправлено')
        else:
            alerts.append('Произошла ошибка')
    return render(request, 'admin/master-request/create.html', {'form': form,
                                                                'alerts': alerts})


def master_request_change_view(request):
    return render(request, 'admin/master-request/change.html')


def master_request_delete_view(request):
    return render(request, 'admin/master-request/delete.html')


def meter_data_view(request):
    return render(request, 'admin/meter-data/index.html')


def meter_data_create_view(request):
    return render(request, 'admin/meter-data/create.html')


def meter_data_change_view(request):
    return render(request, 'admin/meter-data/change.html')


def meter_data_delete_view(request):
    return render(request, 'admin/meter-data/delete.html')


def website_main_page_view(request):

    alerts = []
    MainPageBlockFormset = modelformset_factory(
        model=models.WebsiteMainPageBlocks,
        form=forms.WebsiteMainPageBlocksForm,
        max_num=6,
        min_num=6
    )

    if request.method == 'POST':

        main_page_form = forms.WebsiteMainPageForm(
            request.POST, request.FILES,
            prefix='main_page_form',
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
        main_page: models.WebsiteMainPage = models.WebsiteMainPage.get_solo()
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
    return render(request, 'admin/website/main-page.html', context)


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
    return render(request, 'admin/website/about.html', context)


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
    return render(
        request, 'admin/website/services.html', context)


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
    return render(request, 'admin/website/contact.html', context)


def services_view(request):
    return render(request, 'admin/services/services.html')


def services_del_view(request):
    return render(request, 'admin/services/services.html')


def services_measurement_view(request):
    return render(request, 'admin/services/measurement.html')


def services_measurement_del_view(request):
    return render(request, 'admin/services/measurement.html')


def tariffs_view(request):
    context = {
        'rates': models.Rate.objects.all(),
    }
    return render(request, 'admin/tariffs/index.html', context)


def tariffs_change_view(request, pk):
    alerts = []

    # Форма тарифа
    # Формсет услуги

    if request.method == "POST":

        form = forms.RateForm(request.POST, prefix='tariffs')
        if utils.forms_save([
            form,
        ]):
            alerts.append('Данные сохранены успешно!')

    else:
        form = forms.RateForm(
            instance=get_object_or_404(models.Rate, pk) if pk else None,
            prefix='tariffs',
        )
    context = {
        'form': form,
        'alerts': alerts,
    }
    return render(request, 'admin/tariffs/change.html', context)


def tariffs_create_view(request):
    return tariffs_change_view(request, pk=None)


def tariffs_copy_view(request):
    return render(request, 'admin/tariffs/copy.html')


def tariffs_delete_view(request):
    return render(request, 'admin/tariffs/delete.html')


def user_admin_role_view(request):
    return render(request, 'admin/user-admin/role.html')


def user_admin_users_list(request):
    return render(request, 'admin/user-admin/list.html')


def user_admin_create_view(request):
    return render(request, 'admin/user-admin/create.html')


def user_admin_change_view(request):
    return render(request, 'admin/user-admin/change.html')


def user_admin_delete_view(request):
    return render(request, 'admin/user-admin/delete.html')


def pay_company_view(request):
    return render(request, 'admin/pay-company.html')


def transaction_purpose_view(request):
    return render(request, 'admin/transaction-purpose/index.html')


def transaction_purpose_create_view(request):
    return render(request, 'admin/transaction-purpose/create.html')


def transaction_purpose_change_view(request):
    return render(request, 'admin/transaction-purpose/change.html')


def transaction_purpose_delete_view(request):
    return render(request, 'admin/transaction-purpose/delete.html')
