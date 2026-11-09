import pytest

from delivery_tracking.csv_import import (
    import_deliveries,
    ImportValidationError
)


def test_successful_import(): #успешный импорт
    csv_text = (
        "id,recipient,address,due_date\n"
        "1,Иван Иванов,Москва,2026-11-10\n"
        "2,Петр Петров,Казань,2026-11-11\n"
    )

    result = import_deliveries(csv_text, set())

    assert len(result) == 2
    assert result[0].id == 1
    assert result[0].courier_id is None


def test_duplicate_import(): #защита от дубликатов ID
    csv_text = (
        "id,recipient,address,due_date\n"
        "1,Иван Иванов,Москва,2026-11-10\n"
        "1,Петр Петров,Казань,2026-11-11\n"
    )

    with pytest.raises(ImportValidationError):
        import_deliveries(csv_text, set())


def test_invalid_import_date(): #тест некоректной даты
    csv_text = (
        "id,recipient,address,due_date\n"
        "1,Иван Иванов,Москва,2026-02-30\n"
    )

    with pytest.raises(ImportValidationError):
        import_deliveries(csv_text, set())