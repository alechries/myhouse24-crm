from _db import models
from datetime import datetime
from _db import models
import datetime
import time


def serial_number_account():
    date = datetime.datetime.now().strftime('%d%m%y')
    if models.Account.objects.count() > 0:
        initial_len = '00000'
        count = int(models.Account.objects.all().count()) + 1
        initial_len = initial_len[0:(5 - (int(len(str(count)))))]
        number = f'{date}{initial_len}{count}'
    else:
        number = f'{date}00001'
    return number


def serial_number_transaction():
    date = datetime.datetime.now().strftime('%d%m%y')
    if models.Transfer.objects.count() > 0:
        initial_len = '00000'
        count = int(models.Transfer.objects.all().count()) + 1
        initial_len = initial_len[0:(5 - (int(len(str(count)))))]
        number = f'{date}{initial_len}{count}'
    else:
        number = f'{date}00001'
    return number


def invoice_number():
    date = datetime.datetime.now().strftime('%d%m%y')
    if models.Invoice.objects.count() > 0:
        initial_len = '00000'
        count = int(models.Invoice.objects.all().count()) + 1
        initial_len = initial_len[0:(5 - (int(len(str(count)))))]
        number = f'{date}{initial_len}{count}'
    else:
        number = f'{date}00001'
    return number


def counter_number():
    date = datetime.datetime.now().strftime('%d%m%y')
    if models.Meter.objects.count() > 0:
        initial_len = '00000'
        count = int(models.Meter.objects.all().count()) + 1
        initial_len = initial_len[0:(5 - (int(len(str(count)))))]
        number = f'{date}{initial_len}{count}'
    else:
        number = f'{date}00001'
    return number


def calculate_statistic():
    system_balance = 0
    account_balance = 0
    account_arrears = 0
    transfer_in_list = models.Transfer.objects.filter(solo_status=True)
    transfer_out_list = models.Transfer.objects.filter(solo_status=False)
    transaction_balance = models.Transfer.objects.filter(solo_status=None)
    account = models.Account.objects.all()
    for el in account:
        if el.get_money() < 0:
            account_arrears -= el.get_money()
        if el.get_money() > 0:
            account_balance += el.get_money()

    for el in transfer_in_list:
        if el.amount is not None:
            for account in account:
                if account.get_money() > 0:
                    system_balance += account.get_money()
        system_balance += el.amount
    for el in transfer_out_list:
        if el.amount is not None:
            system_balance -= el.amount
    return {
        'system_balance': float(system_balance),
        'account_balance': float(account_balance),
        'account_arrears': float(account_arrears)
    }


def new_user():

    new_user_slice = {}
    new_user_count = models.User.objects.filter(status='Новый'),
    if models.User.objects.filter(status='Новый').count() > 3:
        new_user_slice = models.User.objects.filter(status='Новый')[:2]
    elif 3 > models.User.objects.filter(status='Новый').count() > 0:
        new_user_slice = models.User.objects.filter(status='Новый')
    return {
        'new_user_count': new_user_count,
        'new_user_slice': new_user_slice,
    }

def time_code():
    year = datetime.date.today().year
    month = datetime.date.today().month
    if int(month) < 10:
        month = f"0{month}"
    day = datetime.date.today().day
    if int(day) < 10:
        day = f"0{day}"
    t = time.time_ns()
    code = f"{year}{month}{day}{t}"
    return code
