from datetime import date

import pytest

from delivery_tracking.models import Delivery, DeliveryStatus
from delivery_tracking.delivery_rules import (
    validate_date,
    complete_delivery,
    cancel_delivery,
    get_overdue_deliveries
)

def create_delivery(
        status=DeliveryStatus.NEW,
        due_date=date(2026, 11, 10)
):
    return Delivery(
        id=1,
        recipient="Иван Иванов",
        address="Москва",
        due_date=due_date,
        status=status
    )

def test_validate_date():
    result = validate_date("2026-11-10")

    assert result == date(2026, 11, 10)

def test_invalid_date():
    with pytest.raises(ValueError):
        validate_date("2026-02-30")

def test_complete_delivery():
    delivery = create_delivery(DeliveryStatus.ASSIGNED)
    complete_delivery(delivery)
    assert delivery.status == DeliveryStatus.DELIVERED

def test_complete_new_delivery():
    delivery = create_delivery()
    with pytest.raises(ValueError):
        complete_delivery(delivery)
    assert delivery.status == DeliveryStatus.NEW

def test_cancel_delivery():
    delivery = create_delivery()
    cancel_delivery(delivery)
    assert delivery.status == DeliveryStatus.CANCELLED

def test_cancel_delivered_delivery():
    delivery = create_delivery(DeliveryStatus.DELIVERED)
    with pytest.raises(ValueError):
        cancel_delivery(delivery)
    assert delivery.status == DeliveryStatus.DELIVERED

def test_overdue_deliveries():
    deliveries = [
        create_delivery(
            DeliveryStatus.NEW,
            date(2026, 11, 9)
        ),
        create_delivery(
            DeliveryStatus.ASSIGNED,
            date(2026, 11, 10)
        ),
        create_delivery(
            DeliveryStatus.DELIVERED,
            date(2026, 11, 8)
        )
    ]

    result = get_overdue_deliveries(
        deliveries,
        date(2026, 11, 10)
    )

    assert len(result) == 1
    assert result[0].status == DeliveryStatus.NEW