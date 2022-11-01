from django.contrib import admin
from .models import category, bank, transaction, business

admin.site.register(category)
admin.site.register(bank)
admin.site.register(transaction)
admin.site.register(business)