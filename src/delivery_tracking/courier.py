from .models import Courier, Delivery, DeliveryStatus


class CourierRegistry: #объявление класса

    def __init__(self):
        self.couriers: dict[int, Courier] = {}

    def register_courier(self, courier: Courier) -> None: #регистрация курьера

        if courier.id in self.couriers:
            raise ValueError("Такой номер курьера уже существует")

        if not courier.name.strip():
            raise ValueError("Имя курьера не может быть пустым")

        self.couriers[courier.id] = courier

    def is_available( #проверка доступности курьера
        self,
        courier_id: int,
        deliveries: list[Delivery]
    ) -> bool:

        if courier_id not in self.couriers:
            raise ValueError("Курьер не найден")

        return not any(
            delivery.courier_id == courier_id
            and delivery.status == DeliveryStatus.ASSIGNED
            for delivery in deliveries
        )

    def assign_courier( #назначение курьера на заказ
        self,
        delivery: Delivery,
        courier_id: int,
        deliveries: list[Delivery]
    ) -> None:

        if delivery not in deliveries:
            raise ValueError("Заявка не найдена")

        if delivery.status != DeliveryStatus.NEW:
            raise ValueError("Заявка уже не является новой")

        if courier_id not in self.couriers:
            raise ValueError("Курьер не найден")

        if not self.is_available(courier_id, deliveries):
            raise ValueError("Курьер уже занят")

        delivery.courier_id = courier_id
        delivery.status = DeliveryStatus.ASSIGNED

    def get_all_couriers(self) -> list[Courier]: #получение всех курьеров
        return list(self.couriers.values())