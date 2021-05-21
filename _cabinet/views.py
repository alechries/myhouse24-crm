from django.shortcuts import render
from _db import models
from . import forms


def index_view(request):
    user = models.User.objects.filter(id=1)[0]
    houses = models.House.objects.filter(user=user)
    apartments = models.Apartment.objects.filter(user=user)
    return render(request, 'cabinet/index.html', {'user': user,
                                                  'houses': houses,
                                                  'apartments': apartments})


def login_view(request):
    return render(request, 'cabinet/login.html')


def logout_view(request):
    return render(request, 'cabinet/logout.html')


def statistic_view(request):
    return render(request, 'cabinet/statistic.html')


def invoice_view(request):
    return render(request, 'cabinet/invoice/index.html')


def invoice_view_view(request):
    return render(request, 'cabinet/invoice/view.html')


def tariffs_view(request):
    return render(request, 'cabinet/tariffs/index.html')


def tariffs_view_view(request):
    return render(request, 'cabinet/tariffs/view.html')


def messages_index(request):
    user = models.User.objects.filter(id=1)[0]
    houses = models.House.objects.filter(user=user)
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
    user = models.User.objects.filter(id=1)[0]
    requests = models.MasterRequest.objects.filter(apartment__user=user)
    return render(request, 'cabinet/master-request/index.html', {'requests': requests})


def master_request_create_view(request):
    user = models.User.objects.filter(id=1)[0]
    houses = models.House.objects.filter(user=user)
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


def master_request_delete_view(request):
    return render(request, 'cabinet/master-request/delete.html')


def user_view(request):
    return render(request, 'cabinet/user/index.html')


def user_change_view(request):
    return render(request, 'cabinet/user/change.html')