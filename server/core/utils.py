from typing import Any


def repository_columns_can_update(values: dict[str, Any]) -> dict[str, Any]:
    for k in ("id", "created_at"):
        values.pop(k, None)
    return values
