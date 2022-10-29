import os

"""Run administrative tasks."""
with os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djWebMoney.settings'):
    import django
    django.setup()

    from budget.models import bank, transaction
    bnk = bank(name="Logan", balance=0, key='frgrthdthdfthjyj')
    bnk.save()