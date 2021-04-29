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
