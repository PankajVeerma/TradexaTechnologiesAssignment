
from decimal import Decimal

from django.test import TestCase


from rest_framework import status
from rest_framework.test import APITestCase

from boxes.models import Box
from products.models import Product
from orders.models import Order, OrderItem, BoxRecommendation
from orders.services import recommend_box, NoSuitableBoxError


class BoxRecommendationTests(TestCase):

    def setUp(self):
        self.book = Product.objects.create(
            name="Book",
            sku="BOOK-001",
            length=Decimal("10"),
            width=Decimal("8"),
            height=Decimal("2"),
            weight=Decimal("0.50"),
        )

        self.small_box = Box.objects.create(
            name="Small",
            length=Decimal("12"),
            width=Decimal("10"),
            height=Decimal("5"),
            max_weight=Decimal("2"),
            cost=Decimal("10"),
        )

        self.medium_box = Box.objects.create(
            name="Medium",
            length=Decimal("20"),
            width=Decimal("15"),
            height=Decimal("10"),
            max_weight=Decimal("5"),
            cost=Decimal("15"),
        )

        self.order = Order.objects.create()

    def test_selects_cheapest_suitable_box(self):
        OrderItem.objects.create(
            order=self.order,
            product=self.book,
            quantity=1,
        )

        recommended_box = recommend_box(self.order)

        self.assertEqual(recommended_box, self.small_box)

    def test_rejects_box_with_insufficient_weight_capacity(self):
        self.small_box.max_weight = Decimal("0.20")
        self.small_box.save()

        OrderItem.objects.create(
            order=self.order,
            product=self.book,
            quantity=1,
        )

        recommended_box = recommend_box(self.order)

        self.assertEqual(recommended_box, self.medium_box)

    def test_rejects_order_with_no_suitable_box(self):
        self.small_box.max_weight = Decimal("0.20")
        self.small_box.save()

        self.medium_box.max_weight = Decimal("0.20")
        self.medium_box.save()

        OrderItem.objects.create(
            order=self.order,
            product=self.book,
            quantity=1,
        )

        with self.assertRaises(NoSuitableBoxError):
            recommend_box(self.order)

    def test_rejects_empty_order(self):
        with self.assertRaises(NoSuitableBoxError):
            recommend_box(self.order)

   
    def test_product_can_fit_after_rotation(self):
        # Make the Small box too short for this product.
        self.small_box.height = Decimal("1")
        self.small_box.save()
    
        product = Product.objects.create(
            name="Rotated Item",
            sku="ROTATE-001",
            length=Decimal("10"),
            width=Decimal("12"),
            height=Decimal("2"),
            weight=Decimal("0.50"),
        )
    
        OrderItem.objects.create(
            order=self.order,
            product=product,
            quantity=1,
        )
    
        recommended_box = recommend_box(self.order)
    
        self.assertEqual(recommended_box, self.medium_box)



class BoxRecommendationAPITests(APITestCase):

    def setUp(self):
        self.book = Product.objects.create(
            name="API Book",
            sku="API-BOOK-001",
            length=Decimal("10"),
            width=Decimal("8"),
            height=Decimal("2"),
            weight=Decimal("0.50"),
        )

        self.box = Box.objects.create(
            name="API Small",
            length=Decimal("12"),
            width=Decimal("10"),
            height=Decimal("5"),
            max_weight=Decimal("2"),
            cost=Decimal("10"),
        )

        self.order = Order.objects.create()

        OrderItem.objects.create(
            order=self.order,
            product=self.book,
            quantity=1,
        )

    def test_recommend_box_successfully(self):
        response = self.client.post(
            f"/api/orders/{self.order.id}/recommend-box/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["recommended_box"]["name"],
            "API Small",
        )
        self.assertTrue(response.data["recommendation_saved"])

        self.assertTrue(
            BoxRecommendation.objects.filter(
                order=self.order,
                box=self.box,
            ).exists()
        )

    def test_recommend_box_for_missing_order(self):
        response = self.client.post(
            "/api/orders/99999/recommend-box/"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_recommend_box_for_empty_order(self):
        empty_order = Order.objects.create()

        response = self.client.post(
            f"/api/orders/{empty_order.id}/recommend-box/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_422_UNPROCESSABLE_ENTITY,
        )
        self.assertIn("error", response.data)

    def test_recommendation_can_be_updated(self):
        response1 = self.client.post(
            f"/api/orders/{self.order.id}/recommend-box/"
        )
        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        more_expensive_box = Box.objects.create(
            name="API Medium",
            length=Decimal("20"),
            width=Decimal("15"),
            height=Decimal("10"),
            max_weight=Decimal("5"),
            cost=Decimal("15"),
        )

        # Make the original box too light for this order.
        self.box.max_weight = Decimal("0.20")
        self.box.save()

        response2 = self.client.post(
            f"/api/orders/{self.order.id}/recommend-box/"
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response2.data["recommended_box"]["id"],
            more_expensive_box.id,
        )

        self.assertEqual(
            BoxRecommendation.objects.get(order=self.order).box,
            more_expensive_box,
        )
