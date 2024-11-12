from django.contrib import admin
from .models import SalesRecord, Inventory, Data

# Register your models here.

admin.site.register(SalesRecord)
admin.site.register(Inventory)
admin.site.register(Data)
