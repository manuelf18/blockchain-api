import hashlib
import datetime
import random

from rest_framework import serializers
from .models import Owners


class OwnerSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(required=True, max_digits=8, decimal_places=3)

    class Meta:
        model = Owners
        fields = ('hash_id', 'amount', 'nonce',)
        read_only_fields = ('hash_id', 'nonce',)

    def _generate_hash(self):
        nonce = 1
        hash_id = hashlib.sha256(str(datetime.datetime.now()).encode('utf-8') + str(nonce).encode('utf-8') +
                                 str(random.randint(1, 100)).encode()).hexdigest()
        while(hash_id[:4] != "0000"):
            nonce += 1
            hash_id = hashlib.sha256(str(datetime.datetime.now()).encode('utf-8') + str(nonce).encode('utf-8') +
                                     str(random.randint(1, 100)).encode()).hexdigest()
        return hash_id, nonce

    def create(self, validated_data):
        """
        Create and return a new [Owner] instance, given the validated data.
        """
        # Validate that amount is larger than 0
        if(validated_data['amount'] <= 0.000):
            raise serializers.ValidationError({'message': 'amount has to be larger than 0.000'})

        validated_data['hash_id'], validated_data['nonce'] = self._generate_hash()
        return Owners.objects.create(**validated_data)
