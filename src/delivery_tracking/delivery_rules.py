from datetime import date

from .models import Delivery, DeliveryStatus

def validate_date(date_string: str) -> date:
    try:
        return date.fromisoformat(date_string)
    except ValueError:
        raise ValueError("Некорректная календарная дата")
    
def complete_delivery(delivery: Delivery) -> None:
    if delivery.status != DeliveryStatus.ASSIGNED:
        raise ValueError("Завершить можно только назначенную доставку")
    delivery.status = DeliveryStatus.DELIVERED

def cancel_delivery(delivery: Delivery) -> None:
    if delivery.status not in (
        DeliveryStatus.NEW,
        DeliveryStatus.ASSIGNED
    ):
        raise ValueError("Эту доставку нельзя отменить")
    delivery.status = DeliveryStatus.CANCELLED

def get_overdue_deliveries(
        deliveries: list[Delivery],
        control_date: date
) -> list[Delivery]:
    
    return [
        delivery
        for delivery in deliveries
        if delivery.status in (
            DeliveryStatus.NEW,
            DeliveryStatus.ASSIGNED
        )
        and delivery.due_date < control_date
    ]