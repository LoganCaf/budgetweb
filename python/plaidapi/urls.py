from django.urls import path
from . import views

urlpatterns = [
    #path('', views.bankCreateView.as_view(), name='bank-create'),
    path('', views.get_new_url_basex2, name='bank-create'),
    #path('bank/create/', views.bankCreateView.as_view(), name='bank-create'),
]