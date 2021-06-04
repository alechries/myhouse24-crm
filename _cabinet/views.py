from django.shortcuts import render
from _db import models
from . import utils as utility
from django.db.models import Q
from . import forms
from _db import models, utils, auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect


def index_view(request):
    apartments = models.Apartment.objects.filter(user_id=request.user.id)
    if apartments.count() != 0:
        return redirect('cabinet_statistic', pk=apartments[0].id)
    else:
        return redirect('non_view')


def non_view(request):
    return render(request, 'cabinet/index.html')


def login_view(request):
    alerts = []

    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.EmailAuthBackend.authenticate(email=form.cleaned_data['email'],
                                                      password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active and user.is_superuser == 0:
                    login(request, user)
                    return redirect('cabinet_index')
                else:
                    alerts.append('User is not active')
            else:
                alerts.append('User does not exist')
        else:
            alerts.append('Data is incorrect')
    else:
        alerts.append('')
    return render(request, 'cabinet/login.html', {'form': forms.LoginForm(), 'alerts': alerts})


def logout_view(request):
    print(request.user)
    logout(request)
    return redirect('cabinet_login')


def statistic_view(request, pk):
    user = request.user
    apartments = models.Apartment.objects.filter(user=user)
    houses = models.House.objects.filter(userhouse__user=user)
    apartment = models.Apartment.objects.get(id=pk)
    month_arrears = apartment.get_arrears()
    context = {'user': user,
               'houses': houses,
               'apartment': apartment,
               'apartments': apartments,
               'arrears': month_arrears}
    return render(request, 'cabinet/statistic.html', context)


def invoice_view(request, pk=None):
    user = request.user
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user=user)
    if pk == 0:
        invoice = models.Invoice.objects.filter(apartment__user=user)
    else:
        invoice = models.Invoice.objects.filter(apartment_id=pk)
    return render(request, 'cabinet/invoice/index.html', {'user': user,
                                                          'invoice': invoice,
                                                          'houses': houses,
                                                          'apartments': apartments})


def invoice_detail_view(request, pk):
    user = request.user
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user=user)
    invoice = models.Invoice.objects.get(id=pk)
    service = models.TariffService.objects.filter(invoice=invoice)
    return render(request, 'cabinet/invoice/detail.html', {'user': user,
                                                           'service': service,
                                                           'invoice': invoice,
                                                           'houses': houses,
                                                           'apartments': apartments})


def tariffs_view(request):
    houses = models.House.objects.filter(userhouse__user=request.user)
    apartments = models.Apartment.objects.filter(user=request.user)
    return render(request, 'cabinet/tariffs/index.html', {'houses': houses,
                                                          'apartments': apartments})


def tariffs_view_view(request, pk):
    houses = models.House.objects.filter(userhouse__user=request.user)
    apartments = models.Apartment.objects.filter(user=request.user)
    tariff = models.TariffService.objects.filter(tariff=pk)
    print(tariff)
    return render(request, 'cabinet/tariffs/view.html', {'tariff': tariff,
                                                         'houses': houses,
                                                         'apartments': apartments})


def messages_index(request):
    user = request.user
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user=user)
    messages = models.Message.objects.filter(Q(apartment__user=user) | Q(indebtedness=1) | Q(addressee='NULL'))
    print(messages)
    return render(request, 'cabinet/messages/index.html', {'user': user,
                                                           'houses': houses,
                                                           'apartments': apartments,
                                                           'messages': messages
                                                           })


def messages_view(request):
    return render(request, 'cabinet/messages/view.html')


def messages_create_view(request):
    return render(request, 'cabinet/messages/create.html')


def messages_detail(request, pk):
    message = models.Message.objects.get(id=pk)
    return render(request, 'cabinet/messages/detail.html', {'message': message})


def messages_delete_view(request):
    return render(request, 'cabinet/messages/delete.html')


def master_request_view(request):
    user = request.user
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user_id=user.id)
    master_request = models.MasterRequest.objects.filter(apartment__user_id=user.id)
    print(user.id)
    print(master_request)
    return render(request, 'cabinet/master-request/index.html', {'requests': master_request,
                                                                 'houses': houses,
                                                                 'apartments': apartments})


def master_request_create_view(request):
    user = request.user
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user=user)
    alerts = []
    if request.method == 'POST':
        form = forms.MasterRequestForm(request.POST)
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно добавлена!')
        else:
            alerts.append('Неуспешно')
    form = forms.MasterRequestForm()
    form.fields['apartment'].queryset = models.Apartment.objects.filter(user_id=user.id)
    return render(request, 'cabinet/master-request/create.html', {'form': form,
                                                                  'user': user,
                                                                  'houses': houses,
                                                                  'apartments': apartments,
                                                                  'alerts': alerts})


def master_request_delete_view(request, pk):
    master_request = models.MasterRequest.objects.get(apartment_id=pk)
    master_request.delete()
    return redirect('cabinet_master-request')


def user_view(request):
    user = request.user
    apartments = models.Apartment.objects.filter(user=user)
    print(apartments)
    return render(request, 'cabinet/user/index.html', {'user': user,
                                                       'apartments': apartments})


def user_change_view(request):
    user = models.User.objects.get(id=request.user.id)
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user=user)
    alerts = []
    if request.method == 'POST':
        form = forms.UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            alerts.append('Успех')
        else:
            alerts.append('Неуспешно')
    form = forms.UserForm(instance=user)
    return render(request, 'cabinet/user/change.html', {'form': form,
                                                        'houses': houses,
                                                        'apartments': apartments,
                                                        'alerts': alerts
                                                        })
