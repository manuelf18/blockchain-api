from rest_framework import serializers
from apps.blockchain.models import Block, Transaction


class BlockSerializer(serializers.Serializer):

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
        return []

    def create(self, validated_data):
        """
        Create and return a new `Owner` instance, given the validated data.
        """
        validated_data['prev_hash_id'] = self._get_prev_hash()
        validated_data['hash_id'], validated_data['nonce'] = self._generate_hash()
        validated_data['transactions'] = self._get_transactions()
        return Block.objects.create(**validated_data)


class TransactionSerializer(serializers.Serializer):
    sender = serializers.StringRelatedField(many=True)
    receiver = serializers.StringRelatedField(many=True)
    amount = serializers.DecimalField(max_digits=8, decimal_places=3)

    class Meta:
        model = Transaction
        fields = ('sender', 'sender', 'owner',)

    def create(self, validated_data):
        """
        Create and return a new `Owner` instance, given the validated data.
        """
        return Transaction.objects.create(**validated_data)