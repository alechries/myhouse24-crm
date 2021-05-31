from _db import models
"""from datetime import datetime
from _db import models


def serial_number_account():
    date = datetime.now().strftime('%Y%m%d')
    if models.Account.objects.count() > 0 and models.Account.objects.all().last():
        last_order = models.Account.objects.all().last()
        if last_order.wallet[0:8] == date:
            num = last_order.wallet[8::]
            print(num)
        else:
            num = 1
        date = f'{date}{num}'
    else:
        date = f'{date}001'
    return date


def serial_number_transfer():
    date = datetime.now().strftime('%Y%m%d')
    print(date)
    if models.Transfer.objects.count() > 0 and models.Transfer.objects.all().last():
        last_order = models.Transfer.objects.all().last()
        if last_order.number[0:8] == date:
            num = int(last_order.number[8::])
            num += 1
            print(last_order.number)
            print(num)
        else:
            num = 1
        date = f'{date}{num}'
    else:
        date = f'{date}001'
    return date
"""


def calculate_statistic():
    system_balance = 0
    account_balance = 0
    account_arrears = 0
    transfer_in_list = models.Transfer.objects.filter(solo_status=True)
    transfer_out_list = models.Transfer.objects.filter(solo_status=False)
    invoice_arrears = models.Invoice.objects.filter(type='Неоплачена')
    transaction_balance = models.Transfer.objects.filter(solo_status=None)
    for el in invoice_arrears:
        if el.total_amount is not None:
            account_arrears += el.total_amount

    for el in transaction_balance:
        if el.amount is not None:
            account_balance += el.amount
    for el in transfer_in_list:
        if el.amount is not None:
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

