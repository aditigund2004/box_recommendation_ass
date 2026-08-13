from django.test import TestCase
from rest_framework.test import APIClient

from .models import Box, Order, OrderItem, Product
from .services import recommend_box_for_order


def make_product(sku, l, w, h, weight):
    return Product.objects.create(sku=sku, name=sku, length_cm=l, width_cm=w, height_cm=h, weight_kg=weight)


def make_box(name, l, w, h, max_weight, cost):
    return Box.objects.create(
        name=name,
        internal_length_cm=l,
        internal_width_cm=w,
        internal_height_cm=h,
        max_weight_kg=max_weight,
        cost=cost,
    )


class RecommendationAlgorithmTests(TestCase):
    def setUp(self):
        # Three box sizes: small, medium, large — medium and large both
        # *could* fit a small order, so the "pick cheapest" rule gets tested.
        self.small_box = make_box("Small", 20, 20, 20, 2, cost=1.00)
        self.medium_box = make_box("Medium", 40, 30, 30, 8, cost=2.50)
        self.large_box = make_box("Large", 60, 50, 50, 20, cost=5.00)

    def test_picks_cheapest_box_that_fits(self):
        order = Order.objects.create(order_number="O-1")
        product = make_product("P1", 15, 15, 15, weight=1)
        OrderItem.objects.create(order=order, product=product, quantity=1)

        result = recommend_box_for_order(order)

        self.assertTrue(result.fits_single_box)
        self.assertEqual(result.box, self.small_box)

    def test_skips_box_that_is_too_small_even_if_cheaper_would_be_ideal(self):
        order = Order.objects.create(order_number="O-2")
        product = make_product("P2", 35, 25, 25, weight=1)
        OrderItem.objects.create(order=order, product=product, quantity=1)

        result = recommend_box_for_order(order)

        self.assertTrue(result.fits_single_box)
        self.assertEqual(result.box, self.medium_box)

    def test_respects_weight_limit_not_just_size(self):
        order = Order.objects.create(order_number="O-3")
        # Physically tiny, but too heavy for the small/medium box's weight cap.
        product = make_product("P3", 5, 5, 5, weight=10)
        OrderItem.objects.create(order=order, product=product, quantity=1)

        result = recommend_box_for_order(order)

        self.assertTrue(result.fits_single_box)
        self.assertEqual(result.box, self.large_box)

    def test_allows_rotation_to_make_item_fit(self):
        order = Order.objects.create(order_number="O-4")
        # 18x18x38 doesn't fit the small box (20x20x20) upright, but does on
        # its side inside the medium box (40x30x30) once rotated.
        product = make_product("P4", 18, 18, 38, weight=1)
        OrderItem.objects.create(order=order, product=product, quantity=1)

        result = recommend_box_for_order(order)

        self.assertTrue(result.fits_single_box)
        self.assertEqual(result.box, self.medium_box)

    def test_falls_back_to_multiple_boxes_when_nothing_fits_it_all(self):
        order = Order.objects.create(order_number="O-5")
        # Two items that each fit the large box alone but together exceed
        # every box's weight capacity.
        product = make_product("P5", 10, 10, 10, weight=15)
        OrderItem.objects.create(order=order, product=product, quantity=2)

        result = recommend_box_for_order(order)

        self.assertFalse(result.fits_single_box)
        self.assertIsNotNone(result.bins)
        total_units_packed = sum(len(b.units) for b in result.bins)
        self.assertEqual(total_units_packed, 2)
        for b in result.bins:
            self.assertLessEqual(b.used_weight, float(b.box.max_weight_kg))

    def test_raises_when_item_fits_no_box_at_all(self):
        order = Order.objects.create(order_number="O-6")
        product = make_product("P6", 100, 100, 100, weight=1)
        OrderItem.objects.create(order=order, product=product, quantity=1)

        with self.assertRaises(ValueError):
            recommend_box_for_order(order)


class RecommendBoxAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        make_box("Small", 20, 20, 20, 2, cost=1.00)
        make_box("Medium", 40, 30, 30, 8, cost=2.50)

    def test_recommend_box_endpoint_returns_expected_shape(self):
        order = Order.objects.create(order_number="API-1")
        product = make_product("PA1", 15, 15, 15, weight=1)
        OrderItem.objects.create(order=order, product=product, quantity=1)

        response = self.client.get(f"/api/orders/{order.id}/recommend-box/")

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["fits_single_box"])
        self.assertEqual(data["recommended_box"]["name"], "Small")
