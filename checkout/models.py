import uuid
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    plan_price = models.IntegerField()
    plan_duration = models.CharField(max_length=20)
    payment_date = models.DateTimeField(default=timezone.now)
    payment_reference = models.CharField(max_length=32, null=False, editable=False)

    def _generate_payment_reference(self):
        """
        Generate a random, unique payment reference using UUID
        """
        return uuid.uuid4().hex.upper()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the payment reference
        if it hasn't been set already.
        """
        if not self.payment_reference:
            self.payment_reference = self._generate_payment_reference()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Payment #{self.payment_reference} - {self.user.username} - {self.plan_name}"

class PurchaseHistory(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    plan_name = models.CharField(max_length=100)
    plan_price = models.IntegerField()
    plan_duration = models.CharField(max_length=20)
    purchase_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.plan_name} - {self.purchase_date}"
