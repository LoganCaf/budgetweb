from django.urls import path
from . import views

urlpatterns = [
    path('', views.categoryListView.as_view(), name='budget-home'),
    path('category/create/', views.categoryCreateView.as_view(), name='category-create'),
    path('category/<int:pk>/update/', views.categoryUpdateView.as_view(), name='category-update'),
    path('category/<int:pk>/delete/', views.categoryDeleteView.as_view(), name='category-delete'),
    path('transaction/', views.transactionListView.as_view(), name='transaction-home'),
    path('transaction/create/', views.transactionCreateView.as_view(), name='transaction-create'),
    path('transaction/<int:pk>/update/', views.transactionUpdateView.as_view(), name='transaction-update'),
    path('transaction/<int:pk>/delete/', views.transactionDeleteView.as_view(), name='transaction-delete'),
    path('bank/', views.bankListView.as_view(), name='bank-home'),
    path('bank/create/', views.bankCreateView.as_view(), name='bank-create'),
    path('bank/<int:pk>/delete/', views.bankDeleteView.as_view(), name='bank-delete'),
]