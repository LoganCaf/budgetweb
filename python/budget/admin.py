from django.contrib import admin
from .models import category, bank, transaction

admin.site.register(category)
admin.site.register(bank)
admin.site.register(transaction)