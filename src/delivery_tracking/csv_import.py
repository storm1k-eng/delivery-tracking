import csv
import io

from datetime import date

from .models import Delivery
from .delivery_rules import validate_date


class ImportValidationError(Exception):
    pass


def import_deliveries(
    csv_text: str,
    existing_ids: set[int]
) -> list[Delivery]:

    reader = csv.DictReader(io.StringIO(csv_text))

    required_headers = {
        "id",
        "recipient",
        "address",
        "due_date"
    }

    if not reader.fieldnames or set(reader.fieldnames) != required_headers:
        raise ImportValidationError(
        )

    imported = []
    errors = []
    seen_ids = set(existing_ids)

    for row in reader:
        line_number = reader.line_num

        try:
            delivery_id = int(row["id"])

            if delivery_id in seen_ids:
                raise ValueError("Дублирующийся номер заявки")

            if not row["recipient"].strip():
                raise ValueError("Не указано имя получателя")

            if not row["address"].strip():
                raise ValueError("Не указан адрес")

            due_date = validate_date(row["due_date"])

            imported.append(
                Delivery(
                    id=delivery_id,
                    recipient=row["recipient"].strip(),
                    address=row["address"].strip(),
                    due_date=due_date
                )
            )

            seen_ids.add(delivery_id)

        except (ValueError, TypeError) as error:
            errors.append(
                f"Строка {line_number}: {error}"
            )

    if errors:
        raise ImportValidationError("\n".join(errors))

    return imported