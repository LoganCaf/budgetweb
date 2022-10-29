import http
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from .models import category, transaction, bank, business
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms import ModelForm

class MyForm(ModelForm):
    class Meta:
        model = bank
        fields = []
    def form_valid(self, form):
        return super().form_valid(form)
    def cleaned_data(self):
        return super().cleaned_data()
class categoryListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    def get_queryset(self):
        return category.objects.filter(user=self.request.user)
class categoryCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = category
    fields = ['name', 'planned']
    success_url = '/'
    def form_valid(self, form):
        form.instance.spent = 0.00
        form.instance.remaining = form.instance.planned
        form.instance.user = self.request.user
        return super().form_valid(form)
class categoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = category
    fields = ['name', 'planned']
    success_url = '/'
    def test_func(self):
        cat = self.get_object()
        if self.request.user == cat.user:
            return True
        return False
class categoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/login/'
    model = category
    success_url = '/'
    def test_func(self):
        cat = self.get_object()
        if self.request.user == cat.user:
            return True
        return False
class transactionListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    for trans in transaction.objects.all():
        if len(business.objects.filter(name=trans.business)) == 0:
            business(name=trans.business)
        elif business.objects.filter(name=trans.business).first().cat != category.objects.filter(name='unused').first():
            transaction.objects.filter(id=trans.id).update(cat=business.objects.filter(name=trans.business).first().cat)
    def get_queryset(self):
        return transaction.objects.filter(fromBank__in=self.request.user.bank_set.all())
class transactionCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = transaction
    fields = ['amount', 'date', 'cat']
    success_url = '/'
    def form_valid(self, form):
        form.instance.business = self.request.user.username
        form.instance.fromBank = self.request.user.bank_set.filter(name=self.request.user.username).first() 
        if self.request.user == form.instance.fromBank.user and self.request.user == form.instance.cat.user:
            return super().form_valid(form)
        return super().form_invalid(form)
class transactionUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = transaction
    success_url = '/'
    fields = ['cat']
    def test_func(self):
        trans = self.get_object()
        if self.request.user == trans.fromBank.user:
            if self.request.user.username == trans.business:
                self.fields.append('amount')
                self.fields.append('date')
            return True
        return False
class transactionDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/login/'
    model = transaction
    success_url = '/'
    def test_func(self):
        trans = self.get_object()
        if self.request.user == trans.fromBank.user and self.request.user == trans.cat.user and self.request.user.username == trans.business:
            return True
        return False
class bankListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    def get_queryset(self):
        for i, bnk in enumerate(bank.objects.all()):
            if bnk.user == User.objects.first():
                instance = bank.objects.get(id=bnk.id)
                form = MyForm(None, instance=instance)
                form.instance.user = self.request.user
                print(form.instance.user,form.instance.name,form.instance.balance,form.instance.key,form.instance.actype)
                form.save()
        return bank.objects.filter(user=self.request.user)
class bankCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = bank
    fields = ['name', 'balance']
    success_url = '/'
    fail_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
class bankDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/login/'
    model = bank
    success_url = '/'
    def test_func(self):
        bnk = self.get_object()
        if self.request.user == bnk.user and bnk.fromBank.name != self.request.user.username:
            return True
        return False
class businessListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    for bus in business.objects.all():
        if bus.cat != category.objects.filter(name='unused').first():
            transaction.objects.filter(business=bus.name).update(cat=bus.cat)
    def get_queryset(self):
        return bus.objects.filter(cat__in=[*self.request.user.bank_set.all()])
class businessUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = transaction
    success_url = '/'
    fields = ['cat']
    def test_func(self):
        trans = self.get_object()
        if self.request.user == trans.fromBank.user:
            if self.request.user.username == trans.business:
                self.fields.append('amount')
                self.fields.append('date')
            return True
        return False
class businessDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/login/'
    model = transaction
    success_url = '/'
    def test_func(self):
        trans = self.get_object()
        if self.request.user == trans.fromBank.user and self.request.user == trans.cat.user and self.request.user.username == trans.business:
            return True
        return False