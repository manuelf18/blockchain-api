from django.urls import path
from rest_framework import routers

from .views import BlockViewSet, TransactionViewSet

router_block = routers.DefaultRouter()
router_block.register('', BlockViewSet, base_name='blockchain')
router_transaction = routers.SimpleRouter()
router_transaction.register('', TransactionViewSet, base_name='transactions')
