
from django.contrib.auth.models import Permission

from django.test import TestCase
from django.urls import reverse
from .models import User, Order


class OrderExportTestCase(TestCase):
    fixtures = [
        "products-fixture.json",
        "users-fixture.json",
        "orders-fixture.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="Test_user", password="qwerty", is_staff=True)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)

    def test_get_orders_view(self):
        response = self.client.get(
            reverse("shopapp:orders-export"),
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.id,
                "products": [product.id for product in order.products.all()]
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data["orders"],
            expected_data,
        )


class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username="Test_user", password="qwerty")
        permission_order = Permission.objects.get(codename='view_order')
        cls.user.user_permissions.add(permission_order)
        cls.user.save()

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
                delivery_address="Test address",
                promocode="sale_1",
                user_id=self.user.pk,
        )

    def tearDown(self) -> None:
        self.order.delete()

    def test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_details", kwargs={"pk": self.order.pk}),
        )
        received_data = response.context["order"].pk
        expected_data = self.order.pk
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertEqual(received_data, expected_data)

