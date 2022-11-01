from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class category(models.Model):
    name = models.CharField(max_length=100)
    planned = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    spent = models.DecimalField(max_digits=10, decimal_places=2)
    remaining = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, default=User.objects.get(id=1).pk, on_delete=models.CASCADE)
    start = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    invest = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.name} - {self.user}'

class bank(models.Model):
    name = models.CharField(max_length=100)
    bnkid = models.CharField(default="no", max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, default=User.objects.get(id=1).pk, on_delete=models.CASCADE)
    key = models.CharField(default="no", max_length=100)
    actype = models.CharField(default= "depository", max_length=100)
    balanceCurrent = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    lastUpdated = models.DateTimeField(default=datetime.now, blank=True)
    def __str__(self):
        return f'{self.name} - {self.user}'

class transaction(models.Model):
    transid = models.CharField(default='no', max_length=100)
    cat = models.ForeignKey(category, related_name='cat', default=category.objects.filter(name='unused').first().pk, on_delete=models.PROTECT,null=True, blank=True)
    date = models.DateField(default=datetime.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    business = models.CharField(max_length=100)
    fromBank = models.ForeignKey(bank, default=None, on_delete=models.CASCADE,null=True, blank=True)
    fromCat = models.ForeignKey(category, related_name='fromCat', default=None, on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return f'{self.business} - {self.fromBank.user}'

class business(models.Model):
    name = models.CharField(default='unused', max_length=100)
    cat = models.ForeignKey(category, default=category.objects.filter(name='unused').first().pk, on_delete=models.CASCADE)
    user = models.ForeignKey(User, default=User.objects.get(id=1).pk, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.name} - {self.user}'