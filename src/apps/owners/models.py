from django.db import models


class Owners(models.Model):
    hash_id = models.CharField(max_length=100, blank=True, default='', primary_key=True)
    nonce = models.IntegerField(verbose_name='cantidad', blank=True, default=0)
    amount = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        return self.hash_id

