import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django_countries.fields import CountryField

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    plan_price = models.DecimalField(max_digits=6, decimal_places=2)
    plan_duration = models.CharField(max_length=20)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_reference = models.CharField(max_length=32, null=False, editable=False)
    status = models.CharField(max_length=10, default='Active')
    
    email = models.EmailField(null=True, blank=True)
    country = CountryField(blank_label='Country', null=False, blank=False)
    postcode = models.CharField(max_length=20, null=True, blank=True)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    county = models.CharField(max_length=80, null=True, blank=True)

    def _generate_payment_reference(self):
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        if not self.payment_reference:
            self.payment_reference = self._generate_payment_reference()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment #{self.payment_reference} - {self.user.username} - {self.plan_name} - {self.status}"
