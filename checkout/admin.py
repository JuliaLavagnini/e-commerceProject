from django.contrib import admin
from .models import Payment, PurchaseHistory


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ('payment_reference',)
    list_display = ('user', 'payment_date','plan_name', 'plan_price', 'plan_duration','country', 'postcode', 'town_or_city', 'street_address1', 'street_address2', 'county', 'email')


class PurchaseHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'plan_name', 'plan_price', 'plan_duration', 'purchase_date')

admin.site.register(Payment, PaymentAdmin)
admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)
