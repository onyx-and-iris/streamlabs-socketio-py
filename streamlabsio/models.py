import keyword
import re
from dataclasses import dataclass


def to_snake_case(s: str) -> str:
    return re.sub(r'(?<!^)(?=[A-Z])', '_', s).lower()


def safe_field_name(name: str) -> str:
    return name + '_' if keyword.iskeyword(name) else name


def as_dataclass(name: str, data: dict):
    def attrs(self) -> list:
        return list(self.__annotations__.keys())

    dc_CLS = dataclass(
        type(
            f'{name}Dataclass',
            (),
            {
                '__annotations__': {
                    safe_field_name(to_snake_case(k)): type(v) for k, v in data.items()
                },
                'attrs': attrs,
            },
        )
    )
    return dc_CLS(**{safe_field_name(to_snake_case(k)): v for k, v in data.items()})
