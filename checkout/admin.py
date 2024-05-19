from django.contrib import admin
from .models import Payment


class PaymentAdmin(admin.ModelAdmin):
    readonly_fields = ('payment_reference',)
    list_display = ('user', 'payment_date','plan_name', 'plan_price', 'plan_duration','country', 'postcode', 'town_or_city', 'street_address1', 'street_address2', 'county', 'email')

admin.site.register(Payment, PaymentAdmin)
