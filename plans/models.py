from django.db import models

class Plan(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    monthly_price = models.IntegerField()
    yearly_price = models.IntegerField()

    def __str__(self):
        return self.name