from django.shortcuts import render
from _db import models
from . import forms
from _db import models, utils, auth
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, get_object_or_404, redirect


def index_view(request):
    user = models.User.objects.get(id=1)
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user=user)
    return render(request, 'cabinet/index.html', {'user': user,
                                                  'houses': houses,
                                                  'apartments': apartments})


def login_view(request):
    alerts = []
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = auth.EmailAuthBackend.authenticate(email=form.cleaned_data['email'],
                                                      password=form.cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('cabinet_index')
                else:
                    alerts.append('User is not active')
            else:
                alerts.append('User does not exist')
        else:
            alerts.append('Data is incorrect')
    else:
        alerts.append('Please, Sign in')
    return render(request, 'cabinet/login.html', {'form': forms.LoginForm(), 'alerts': alerts})


def logout_view(request):
    logout(request)
    return redirect('cabinet_login')


def statistic_view(request):
    return render(request, 'cabinet/statistic.html')


def invoice_view(request, pk=None):
    user = models.User.objects.get(id=1)
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user=user)
    if pk == 0:
        invoice = models.Invoice.objects.filter(apartment=apartments)
    else:
        invoice = models.Invoice.objects.filter(apartment__user=user)
    return render(request, 'cabinet/invoice/index.html', {'user': user,
                                                          'invoice': invoice,
                                                          'houses': houses,
                                                          'apartments': apartments})


def invoice_view_view(request):
    return render(request, 'cabinet/invoice/view.html')


def tariffs_view(request):
    return render(request, 'cabinet/tariffs/index.html')


def tariffs_view_view(request):
    return render(request, 'cabinet/tariffs/view.html')


def messages_index(request):
    user = models.User.objects.get(id=1)
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user=user)
    messages = models.Message.objects.filter(destination_id=user)[::-1]
    return render(request, 'cabinet/messages/index.html', {'user': user,
                                                           'houses': houses,
                                                           'apartments': apartments,
                                                           'messages': messages
                                                           })


def messages_view(request):
    return render(request, 'cabinet/messages/view.html')


def messages_create_view(request):
    return render(request, 'cabinet/messages/create.html')


def messages_delete_view(request):
    return render(request, 'cabinet/messages/delete.html')


def master_request_view(request):
    user = models.User.objects.get(id=1)
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user=user)
    requests = models.MasterRequest.objects.filter(apartment__user=user)
    return render(request, 'cabinet/master-request/index.html', {'requests': requests,
                                                                 'houses': houses,
                                                                 'apartments': apartments})


def master_request_create_view(request):
    user = models.User.objects.get(id=1)
    houses = models.House.objects.filter(userhouse__user=user)
    apartments = models.Apartment.objects.filter(user=user)
    form = forms.MasterRequestForm(request.POST)
    form.owner = 1
    alerts = []
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            alerts.append('Запись была успешно добавлена!')
    return render(request, 'cabinet/master-request/create.html', {'form': form,
                                                                  'user': user,
                                                                  'houses': houses,
                                                                  'apartments': apartments})


def master_request_delete_view(request, pk):
    master_request = models.MasterRequest.objects.get(apartment_id=pk)
    master_request.delete()
    return redirect('cabinet_master-request')


def user_view(request):
    return render(request, 'cabinet/user/index.html')


def user_change_view(request):
    return render(request, 'cabinet/user/change.html')