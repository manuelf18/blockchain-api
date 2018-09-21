from django.urls import path
from rest_framework import routers

from .views import BlockViewSet, TransactionViewSet

router = routers.DefaultRouter()
router.register(r'blockchain', BlockViewSet, base_name='blockchain')
router.register(r'transactions', TransactionViewSet, base_name='transactions')
