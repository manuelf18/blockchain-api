from django.db import models


class Owners(models.Model):
    hash_id = models.CharField(max_length=100, blank=True, default='')
    amount = models.DecimalField(max_digits=8, decimal_places=3)

    @property
    def refresh_amount():
        pass