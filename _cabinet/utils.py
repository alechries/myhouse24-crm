from _db import models
from django.db.models import Q


def calculate_statistic(account_id):
    account_balance = 0
    transaction_in_balance = models.Transfer.objects.filter(Q(account_id=account_id), Q(transfer_type__status='Приход'))
    transaction_out_balance = models.Transfer.objects.filter(Q(account_id=account_id), Q(transfer_type__status='Расход'))
    for el in transaction_in_balance:
        account_balance += el.amount

    for el in transaction_out_balance:
        account_balance -= el.amount

    return {'account_balance': float(account_balance)}
