from rest_framework import serializers
from .models import Owners


class OwnerSerializer(serializers.Serializer):
    hash_id = serializers.CharField(required=True, max_length=100)
    amount = serializers.DecimalField(required=True, max_digits=8, decimal_places=3)

    def create(self, validated_data):
        """
        Create and return a new `Owner` instance, given the validated data.
        """
        return Vocabulario.objects.create(**validated_data)