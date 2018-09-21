from django.db import models
from apps.owners.models import Owners


class Block(models.Model):
    prev_hash_id = models.CharField(max_length=100, blank=True, default='', verbose_name='hash previo')
    hash_id = models.CharField(max_length=100, blank=True, default='', verbose_name='hash')
    timestamp = models.DateField(auto_now=True, verbose_name='fecha') 
    nonce = models.IntegerField(verbose_name='cantidad')

    class Meta:
        ordering = ['hash_id']

    @property
    def calculate_hash(self):
        pass

    @property
    def validate_hash(self):
        pass


class Transaction(models.Model):
    sender = models.ForeignKey(Owners, null=True, blank=True,
                               on_delete=models.SET_NULL,
                               verbose_name="Enviador", related_name="owner_sender")

    receiver = models.ForeignKey(Owners, null=True, blank=True,
                                 on_delete=models.SET_NULL,
                                 verbose_name="Receptor", related_name="owner_receiver")
    amount = models.DecimalField(max_digits=8, decimal_places=3, verbose_name='cantidad')
    mined = models.BooleanField(verbose_name='minado', default=False)

    @property
    def calculate_valid(self, sender_amount,   transaction):
        if(sender_amount < transaction):
            return True
        else:
            return False
