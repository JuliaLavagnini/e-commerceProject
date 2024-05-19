from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    monthly_price = models.DecimalField(max_digits=6, decimal_places=2)
    yearly_price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name