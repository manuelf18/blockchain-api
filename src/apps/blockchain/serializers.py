from django.db.models import Count

from rest_framework import serializers
from .models import Block, Transaction
from ..owners.models import Owners


class BlockSerializer(serializers.ModelSerializer):
    transactions = serializers.StringRelatedField(many=True)

    class Meta:
        model = Block
        fields = ('prev_hash_id', 'hash_id', 'transactions', 'timestamp', 'nonce',)

    def _get_prev_hash(self):
        # Gets the hash of the previous trancsactions or NONE is there isn't one
        return Block.objects.last().hash_id

    def _generate_hash(self):
        next_nonce = Block.objects.last().nonce + 1
        next_hash_id = hash(next_nonce)
        return next_hash_id, next_nonce

    def _get_transactions(self):
        # TODO: List the first 5 transactions with mined=False
        transactions = Transaction.objects.filter(mined=False).annotate(count=Count('amount'))
        return transactions, transactions['count']

    def create(self, validated_data):
        """
        Create and return a new <Transaction> instance, given the validated data.
        """
        validated_data['transactions'], counter = self._get_transactions()
        if validated_data['transactions'] is not None and counter >= 5:
            validated_data['prev_hash_id'] = self._get_prev_hash()
            validated_data['hash_id'], validated_data['nonce'] = self._generate_hash()
            return Block.objects.create(**validated_data)
        else:
            error = {'message': 'Not enough transactions'}
            raise serializers.ValidationError(error)


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(max_length=100)
    receiver = serializers.CharField(max_length=100)
    block = serializers.RelatedField(source='block.hash_id', read_only=True)
    amount = serializers.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        model = Transaction
        fields = ('sender', 'receiver', 'amount', 'block', 'mined',)
        read_only_fields = ('mined',)

    def _validate_amount(self, amount_sent, sender_fk):
        """
        get <Owner>.amount and verify if its more than amount_sent
        """
        owner_amount = Owners.objects.get(hash_id=sender_fk).amount
        if (owner_amount > amount_sent):
            # TODO update sender (<Owner>)'s amount and receiver (<Owner>)'s amount, 
            # ask Erick if its just a normal update on the <Block> Model
            return True
        else:
            return False

    def create(self, validated_data):
        """
        Create and return a new <Transaction> instance, given the validated data.
        """
        sender_fk = validated_data['sender']
        amount_sent = validated_data['amount']
        if (self._validate_amount(amount_sent, sender_fk)) is True:
            validated_data['sender'] = Owners.objects.get(hash_id=sender_fk)
            validated_data['receiver'] = Owners.objects.get(hash_id=validated_data['receiver'])
            return Transaction.objects.create(**validated_data)
        else:
            error = {'message': 'amount not enough in Sender'}
            raise serializers.ValidationError(error)
