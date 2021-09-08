from django.contrib import admin
from .models import Provider, Currency, Pair, Trade

admin.site.register(Provider)
admin.site.register(Currency)
admin.site.register(Pair)
admin.site.register(Trade)
