from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Block, Transaction
from .serializers import BlockSerializer, TransactionSerializer


class BlockViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given [Transaction].

    list:
    Return a list of all the existing [Block].

    create:
    Creates a new [Block] takes no parameters:
        Notes:
            - There has to be at least 5 mined=False transactions in order to proceed.
    """
    queryset = Block.objects.all().order_by('-timestamp')
    serializer_class = BlockSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given [Transaction].

    list:
    Return a list of all the existing [Transaction].

    create:
    Creates a new [Transaction] with parameters:
        {
            "sender" = Owner hash 1 (as String)
            "receiver" = Owner hash 2 (as String)
            "amount" = (as Integer)
        }
        Notes:
            -sender and receiver have to be different
            -sender should have enough amount to proceed with the transaction
            -amount has to be larger that 0.00
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
