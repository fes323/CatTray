from django.contrib import admin
from .models import ChainOfStores, Shop, Goods

admin.site.register(ChainOfStores)
admin.site.register(Shop)
admin.site.register(Goods)
