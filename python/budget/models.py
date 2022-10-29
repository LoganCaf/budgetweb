from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class category(models.Model):
    name = models.CharField(max_length=100)
    planned = models.DecimalField(max_digits=10, decimal_places=2)
    spent = models.DecimalField(max_digits=10, decimal_places=2)
    remaining = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name

class bank(models.Model):
    name = models.CharField(max_length=100)
    bnkid = models.CharField(max_length=100)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, default=User.objects.get(id=1).pk, on_delete=models.CASCADE)
    key = models.CharField(max_length=100)
    actype = models.CharField(default= "depository", max_length=100)
    def __str__(self):
        return self.name

class transaction(models.Model):
    transid = models.CharField(max_length=100)
    cat = models.ForeignKey(category, default=category.objects.filter(name='unused').first().pk, on_delete=models.PROTECT)
    date = models.DateField(default=datetime.now)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    business = models.CharField(max_length=100)
    fromBank = models.ForeignKey(bank, on_delete=models.CASCADE)
    def __str__(self):
        return self.business

class business(models.Model):
    name = models.CharField(default='unused', max_length=100)
    cat = models.ForeignKey(category, default=category.objects.filter(name='unused').first().pk, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name