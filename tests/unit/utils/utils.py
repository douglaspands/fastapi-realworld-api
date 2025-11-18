from typing import Any

from pydash import camel_case


def snake_to_camel(d: dict[str, Any]) -> dict[str, Any]:
    r: dict[str, Any] = {}
    for k, v in d.items():
        if isinstance(v, (list, set, tuple)):
            il = []
            for i in v:
                il.append(snake_to_camel(i) if isinstance(i, dict) else i)
            r[camel_case(k)] = il
        else:
            r[camel_case(k)] = snake_to_camel(v) if isinstance(v, dict) else v
    return r
