from django.test import TestCase, Client
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Gato
from .serializers import OwnerSerializer
import json

client = APIClient()


# First we are testing our Owner model.
class GatoModelTest(TestCase):
    def setUp(self):
        Gato.objects.create(nombre='pelusa', edad=10)

    def test_gato(self):
        owner = Owners.objects.get(nonce='222')
        self.assertEqual(owner.__str__(), "test_hash_id")


class OwnerGetApiTest(APITestCase):
    def setUp(self):
        Owners.objects.create(hash_id="test_hash_id", nonce="222", amount="222.22")
        Owners.objects.create(hash_id="test_hash_xd", nonce="442", amount="2220.22")

    def test_valid_get_owners(self):
        # get API response
        response = client.get("http://localhost:8000/owners/")
        # get data from db
        owners = Owners.objects.all()
        serializer = OwnerSerializer(owners, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class OwnerPostApiTest(APITestCase):

    def setUp(self):
        self.valid_owner = {
            "amount": "23.50"
        }
        self.invalid_owner = {
            "amount": "a"
        }

    def test_create_valid_owner(self):
        valid_amount = "23.50"
        owner = Owners.objects.create(hash_id="test_hash_id", nonce="222", amount=valid_amount)
        response = client.post(
            "http://localhost:8000/owners/",
            data=json.dumps(self.valid_owner),
            content_type='application/json'
        )
        serializer = OwnerSerializer(owner)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, serializer.data)

    def test_create_invalid_owner(self):
        response = client.post(
            "http://localhost:8000/owners/",
            data=json.dumps(self.invalid_owner),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
