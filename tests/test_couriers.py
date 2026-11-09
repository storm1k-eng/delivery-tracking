from datetime import date

import pytest

from delivery_tracking.models import (
    Courier,
    Delivery,
    DeliveryStatus
)

from delivery_tracking.couriers import CourierRegistry


def test_register_courier(): #регистрация курьера
    registry = CourierRegistry()

    registry.register_courier(Courier(1, "Алексей"))

    assert len(registry.get_all_couriers()) == 1


def test_duplicate_courier(): #тест на дубликат курьера
    registry = CourierRegistry()

    registry.register_courier(Courier(1, "Алексей"))

    with pytest.raises(ValueError):
        registry.register_courier(Courier(1, "Иван"))


def test_assign_courier(): #тест назначения на заказ
    registry = CourierRegistry()

    courier = Courier(1, "Алексей")
    delivery = Delivery(
        1, "Иван", "Москва", date(2026, 11, 10)
    )

    registry.register_courier(courier)

    deliveries = [delivery]

    registry.assign_courier(delivery, 1, deliveries)

    assert delivery.courier_id == 1
    assert delivery.status == DeliveryStatus.ASSIGNED


def test_courier_cannot_take_second_delivery(): #защита от перегрузки курьера
    registry = CourierRegistry()
    registry.register_courier(Courier(1, "Алексей"))

    first = Delivery(
        1, "Иван", "Москва", date(2026, 11, 10),
        DeliveryStatus.ASSIGNED, 1
    )

    second = Delivery(
        2, "Пётр", "Казань", date(2026, 11, 11)
    )

    deliveries = [first, second]

    with pytest.raises(ValueError):
        registry.assign_courier(second, 1, deliveries)

    assert second.status == DeliveryStatus.NEW
    assert second.courier_id is None