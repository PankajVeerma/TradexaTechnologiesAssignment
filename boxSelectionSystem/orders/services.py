
from decimal import Decimal

from boxes.models import Box
from .models import Order


class NoSuitableBoxError(Exception):
    """Raised when no available box can fit an order."""
    pass


def dimensions_fit(product, box):
    """Check whether a product fits inside a box, allowing rotation."""

    product_dimensions = sorted(
        [product.length, product.width, product.height],
        reverse=True
    )

    box_dimensions = sorted(
        [box.length, box.width, box.height],
        reverse=True
    )

    return all(
        product_dimension <= box_dimension
        for product_dimension, box_dimension
        in zip(product_dimensions, box_dimensions)
    )


def get_order_weight(order):
    """Calculate the total weight of all products in an order."""

    total_weight = Decimal("0.00")

    for item in order.items.select_related("product").all():
        total_weight += item.product.weight * item.quantity

    return total_weight


def get_order_volume(order):
    """Calculate the combined volume of all products in an order."""

    total_volume = Decimal("0.00")

    for item in order.items.select_related("product").all():
        product = item.product

        product_volume = (
            product.length * product.width * product.height
        )

        total_volume += product_volume * item.quantity

    return total_volume


def recommend_box(order):
    """Return the lowest-cost box that passes our fit checks."""

    items = list(
        order.items.select_related("product").all()
    )

    if not items:
        raise NoSuitableBoxError(
            "Cannot recommend a box for an empty order."
        )

    total_weight = get_order_weight(order)
    total_volume = get_order_volume(order)

    suitable_boxes = []

    for box in Box.objects.all():
        if box.max_weight < total_weight:
            continue

        if box.length * box.width * box.height < total_volume:
            continue

        products_fit = all(
            dimensions_fit(item.product, box)
            for item in items
        )

        if products_fit:
            suitable_boxes.append(box)

    if not suitable_boxes:
        raise NoSuitableBoxError(
            "No available box can accommodate this order."
        )

    return min(
        suitable_boxes,
        key=lambda box: (box.cost, box.pk)
    )
