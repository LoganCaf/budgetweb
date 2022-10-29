from django.shortcuts import render
from django.views.generic import ListView, UpdateView, CreateView, DeleteView
from budget.models import transaction, bank
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect

def get_new_url(request):
    # Specify the port number, you could get this dynamically
    # through a config file or something if you wish
    new_port = '8080'
    end = []
    i=3
    while str(request)[-i] != '/':
        end.append(str(request)[-i])
        i+=1
    end.reverse()
    end = ''.join(end)
    url = 'http://localhost:' + new_port + f'/api/{end}'
    print(url)
    return redirect(url)
def get_new_url_base(request):
    # Specify the port number, you could get this dynamically
    # through a config file or something if you wish
    new_port = '8080'
    url = 'http://localhost:' + new_port + '/api/'
    print(url)
    return redirect(url)
def get_new_url_basex2(request):
    # Specify the port number, you could get this dynamically
    # through a config file or something if you wish
    new_port = '8080'
    url = 'http://localhost:' + new_port
    print(url)
    return redirect(url)