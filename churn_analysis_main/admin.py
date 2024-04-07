from django.contrib import admin
from .models import CustomerGroup, Customer, ChurnPredictionModel, Transaction

admin.site.register(CustomerGroup)
admin.site.register(Customer)
admin.site.register(ChurnPredictionModel)
admin.site.register(Transaction)
