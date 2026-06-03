from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from apps.products.models import Product


class Command(BaseCommand):
    help = "Create sample users and products for local development."

    def handle(self, *args, **options):
        user, created = get_user_model().objects.get_or_create(
            username="admin",
            defaults={"email": "admin@example.com", "is_staff": True, "is_superuser": True},
        )
        if created:
            user.set_password("AdminPass123!")
            user.save()

        Token.objects.get_or_create(user=user)

        products = [
            {"name": "Laptop", "description": "Production-grade developer laptop.", "price": Decimal("1299.99"), "stock": 12},
            {"name": "Keyboard", "description": "Mechanical keyboard.", "price": Decimal("149.99"), "stock": 30},
            {"name": "Monitor", "description": "27-inch 4K display.", "price": Decimal("399.99"), "stock": 8},
        ]
        for product in products:
            Product.objects.get_or_create(name=product["name"], defaults=product)

        self.stdout.write(self.style.SUCCESS("Sample data created. Admin login: admin / AdminPass123!"))
