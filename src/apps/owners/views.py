from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework import viewsets, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser


from .models import Owners
from .serializers import OwnerSerializer


class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owners.objects.all()
    serializer_class = OwnerSerializer
