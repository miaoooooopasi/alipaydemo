from django.contrib import admin

# Register your models here.
from .models import OrderInfo, PayInfo

admin.site.register(OrderInfo)
admin.site.register(PayInfo)
