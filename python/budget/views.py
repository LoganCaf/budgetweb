import http
from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DeleteView, DetailView
from .models import category, transaction, bank, business
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.forms import ModelForm
from datetime import datetime

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
    transaction.objects.filter(cat__name='unused',fromBank__user=User.objects.get(username='Emma')).update(cat=category.objects.get(name='unused',user=User.objects.get(username='Emma')))
    nowMonth = datetime.now().month
    for trans in transaction.objects.all():
        if len(business.objects.filter(name=trans.business)) == 0:
            business(name=trans.business)
        elif len(business.objects.filter(name=trans.business,user=trans.fromBank.user).exclude(cat__name='unused')) > 0:
            transaction.objects.filter(id=trans.id).update(cat=business.objects.filter(name=trans.business,user=trans.fromBank.user).first().cat)
    for cat in category.objects.all():
        if len(transaction.objects.filter(cat__name=cat.name, fromBank__user=cat.user)) == 0:
            category.objects.filter(id=cat.id).update(remaining=cat.start)
        else:
            category.objects.filter(id=cat.id).update(remaining=cat.start-sum([t.amount for t in transaction.objects.filter(cat__name=cat.name, fromBank__user=cat.user)]))
        if len(transaction.objects.filter(fromCat__name=cat.name, fromBank__user=cat.user)) != 0:
            category.objects.filter(id=cat.id).update(remaining=cat.remaining+sum([t.amount for t in transaction.objects.filter(fromCat__name=cat.name, fromBank__user=cat.user)]))
        if len(transaction.objects.filter(cat__name=cat.name, fromBank__user=cat.user, date__month=nowMonth)) == 0:
            category.objects.filter(id=cat.id).update(spent=0)
        else:
            category.objects.filter(id=cat.id).update(spent=-sum([t.amount for t in transaction.objects.filter(cat__name=cat.name, fromBank__user=cat.user, date__month=nowMonth)]))
        if len(transaction.objects.filter(fromCat__name=cat.name, fromBank__user=cat.user, date__month=nowMonth)) != 0:
            category.objects.filter(id=cat.id).update(spent=cat.spent+sum([t.amount for t in transaction.objects.filter(fromCat__name=cat.name, fromBank__user=cat.user, date__month=nowMonth)]))
    
    def get_queryset(self):
        if sum(self.request.user.category_set.filter(name='income').values_list('remaining', flat=True)) > 0 and sum(self.request.user.category_set.all().values_list('planned', flat=True))>0:
            allPlanned = self.request.user.category_set.all().values_list('planned', flat=True)
            sumPlanned = sum(allPlanned)
            inRemaining = sum(self.request.user.category_set.filter(name='income').values_list('remaining', flat=True))
            moneyPer = [(ip/sumPlanned)*inRemaining for ip in allPlanned[:-1]]
            moneyPer.append(inRemaining - sum(moneyPer))
            for i,c in enumerate(self.request.user.category_set.all()):
                self.request.user.category_set.filter(id=c.pk).update(start=c.start+moneyPer[i])
                transaction(cat_id=c.pk, amount=moneyPer[i],business=self.request.user.username,fromCat=self.request.user.category_set.filter(name='income'))
        return category.objects.filter(user=self.request.user)
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        allBalance = sum(self.request.user.bank_set.exclude(actype="credit").values_list('balance', flat=True)) - sum(self.request.user.bank_set.filter(actype="credit").values_list('balanceCurrent', flat=True))
        allRemaining = sum(self.request.user.category_set.all().values_list('remaining', flat=True))
        context['allBalance'] = allBalance
        context['allRemaining'] = allBalance - allRemaining
        return context

class categoryCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = category
    fields = ['name', 'planned','start']
    success_url = '/'
    def form_valid(self, form):
        form.instance.spent = 0.00
        form.instance.remaining = 0.00
        form.instance.user = self.request.user
        return super().form_valid(form)
class categoryUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = category
    success_url = '/'
    fields = []
    def test_func(self):
        cat = self.get_object()
        if cat.name != 'unused' and cat.name != 'income':
            self.fields.append('id')
            self.fields.append('name')
            self.fields.append('planned')
            self.fields.append('start')
        else:
            self.fields = []
        if self.request.user == cat.user:
            return True
        return False
class categoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/login/'
    model = category
    success_url = '/'
    def test_func(self):
        cat = self.get_object()
        if self.request.user == cat.user and cat.name != 'unused' and cat.name != 'income':
            return True
        return False
class transactionListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    def get_queryset(self):
        return transaction.objects.filter(fromBank__in=self.request.user.bank_set.all()).order_by('-date')
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
        bank.objects.filter(user=User.objects.first()).update(user=self.request.user)
        return bank.objects.filter(user=self.request.user)
class bankCreateView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    model = bank
    fields = ['name', 'balance']
    success_url = '/bank/'
    fail_url = '/bank/create/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
class bankDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/login/'
    model = bank
    success_url = '/'
    def test_func(self):
        bnk = self.get_object()
        if self.request.user == bnk.user and bnk.name != self.request.user.username:
            return True
        return False
class bankDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    login_url = '/login/'
    model = bank
    success_url = '/'
    def test_func(self):
        bnk = self.get_object()
        if self.request.user == bnk.user:
            return True
        return False
class businessListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    for bus in business.objects.all():
        if bus.cat != category.objects.filter(name='unused').first():
            transaction.objects.filter(business=bus,fromBank__user=bus.user).update(cat=bus.cat)
    def get_queryset(self):
        return business.objects.filter(user=self.request.user)
class businessUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    login_url = '/login/'
    model = business
    success_url = '/'
    fields = ['cat']
    def test_func(self):
        bus = self.get_object()
        if self.request.user == bus.user:
            return True
        return False
class businessDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    login_url = '/login/'
    model = business
    success_url = '/'
    def test_func(self):
        bus = self.get_object()
        if self.request.user == bus.user:
            return True
        return False
