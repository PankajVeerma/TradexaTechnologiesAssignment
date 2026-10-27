from django.contrib import admin
from .models import Order, OrderItem, BoxRecommendation
# Register your models here.

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(BoxRecommendation)