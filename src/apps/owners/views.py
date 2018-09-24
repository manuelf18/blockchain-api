from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser

from .models import Owners
from .serializers import OwnerSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Return the given [Owner].

    list:
    Return a list of all the existing [Owner].

    create:
    Creates a new [Owner] with parameters:
        {
            "amount" = (as Integer)
        }
        Notes:
            -amount has to be larger that 0.00
    """
    queryset = Owners.objects.all()
    serializer_class = OwnerSerializer
