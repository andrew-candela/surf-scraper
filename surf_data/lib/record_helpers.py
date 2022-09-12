from typing import Union
from dataclasses import dataclass
from decimal import Decimal


UNIT_TO_DESCRIPTION_MAP = {
    "yr": "year",
    "mo": "month",
    "dy": "day",
    "hr": "hour",
    "mn": "minute",
    "m": "meters",
    "sec": "seconds",
    "degT": "degrees true",
    "m/s": "meters per second",
    "hPa": "hPa",
    "degC": "degrees celcius",
    "nmi": "nautical miles",
    "ft": "feet",
    "-": "",
}


@dataclass
class DataPoint:
    measure: Union[str, Decimal]
    unit: str

    def __repr__(self) -> str:
        return f"{self.measure} {UNIT_TO_DESCRIPTION_MAP.get(self.unit, '')}"

    def __str__(self) -> str:
        return self.__repr__()
