from django.db import models


class ExchangeRate(models.Model):
    currency = models.CharField(null=True, blank=True, max_length=5)
    rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.currency + '-' + str(self.rate)
