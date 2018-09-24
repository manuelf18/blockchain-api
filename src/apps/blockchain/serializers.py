import hashlib
import datetime
import random

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Block, Transaction
from ..owners.models import Owners


class BlockSerializer(serializers.ModelSerializer):
    transactions = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Block
        fields = ('prev_hash_id', 'hash_id', 'transactions', 'timestamp', 'nonce',)
        read_only_fields = ('prev_hash_id', 'hash_id', 'transactions', 'timestamp', 'nonce',)

    def _generate_hash(self):
        nonce = 1
        hash_id = hashlib.sha256(str(datetime.datetime.now()).encode('utf-8') + str(nonce).encode('utf-8') +
                                 str(random.randint(1, 100)).encode()).hexdigest()
        if Block.objects.last() is not None:
            prev_hash_id = Block.objects.last().hash_id
        else:
            prev_hash_id = None
        while(hash_id[:4] != "0000"):
            nonce += 1
            hash_id = hashlib.sha256(str(datetime.datetime.now()).encode('utf-8') + str(nonce).encode('utf-8') +
                                     str(random.randint(1, 100)).encode()).hexdigest()
        return hash_id, nonce, prev_hash_id

    def _validate_mined(self, trans):
        if trans.count() == 5:
            return True, trans.values_list('id', flat=True), {"message": "Success."}
        elif trans.count() > 5:
            trans = trans.values_list('id', flat=True)[:5]
            return True, trans, {"message": "Success Sliced."}
        else:
            return False, trans.values_list('id', flat=True), {"message": "Not enough Transactions."}

    def _get_transactions(self):
        # TODO: List the first 5 transactions with mined=False
        return self._validate_mined(Transaction.objects.filter(mined=False).order_by('timestamp'))

    def create(self, data):
        """
        Create and return a new [Block] instance, given the validated data.
        """
        data = {}
        flag, trans_ids, error = self._get_transactions()
        if flag is True:
            data['hash_id'], data['nonce'], data['prev_hash_id'] = self._generate_hash()
            trans = Transaction.objects.filter(id__in=trans_ids).order_by('timestamp')
            for t in trans:
                t.mined = True
                t.save(update_fields=['mined', ])
            created = Block.objects.create(**data)
            created.transactions.set(trans)
            return created
        else:
            raise serializers.ValidationError(error)


class TransactionSerializer(serializers.ModelSerializer):
    sender = serializers.CharField(max_length=100)
    receiver = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        model = Transaction
        fields = ('sender', 'receiver', 'amount', 'mined', 'timestamp',)
        read_only_fields = ('mined', 'timestamp',)

    def _validate_owner(self, id):
        try:
            data = Owners.objects.get(hash_id=id)
        except Exception as e:
            raise serializers.ValidationError({'message': 'no Owner of id'})
        return data

    def _update_amount(self, amount_sent, sender, receiver):
        sender.amount -= amount_sent
        receiver.amount += amount_sent
        sender.save()
        receiver.save()

    def create(self, validated_data):
        """
        Create and return a new [Transaction] instance, given the validated data.
        """

        # Validate that amount is larger than 0
        if(validated_data['amount'] <= 0.000):
            raise serializers.ValidationError({'message': 'amount has to be larger than 0.000'})

        # Validate that the two accounts are not the same
        if(validated_data['sender'] == validated_data['receiver']):
            raise serializers.ValidationError({'message': 'cant send to yourself'})

        # Validate that sender exits
        validated_data['sender'] = self._validate_owner(validated_data['sender'])

        sender_amount = validated_data['sender'].amount
        amount_sent = validated_data['amount']
        # Validate that sender has enough amount to create the transaction
        if sender_amount > amount_sent:
            # Validate that receiver exists
            validated_data['receiver'] = self._validate_owner(validated_data['receiver'])

            # Update the amounts of both sender and receiver
            self._update_amount(amount_sent, validated_data['sender'], validated_data['receiver'])

            # Create the transaction
            return Transaction.objects.create(**validated_data)
        else:
            error = {'message': 'amount not enough in Sender'}
            raise serializers.ValidationError(error)
