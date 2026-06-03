from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Product


class ProductAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="tester", password="StrongPass123!")
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")

    def test_create_product(self):
        response = self.client.post(
            reverse("v1:product-list"),
            {"name": "Laptop", "description": "Dev machine", "price": "1299.99", "stock": 5},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(response.data["data"]["name"], "Laptop")

    def test_list_products_supports_search(self):
        Product.objects.create(name="Laptop", description="Portable", price="1200.00", stock=4)
        Product.objects.create(name="Desk", description="Office", price="300.00", stock=2)

        response = self.client.get(reverse("v1:product-list"), {"search": "lap"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["results"][0]["name"], "Laptop")
