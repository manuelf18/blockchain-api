from django.urls import path
from rest_framework import routers

from .views import OwnerViewSet

router = routers.DefaultRouter()
router.register(r'owners', OwnerViewSet, base_name='owners')