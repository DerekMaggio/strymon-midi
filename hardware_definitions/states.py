import typing
from typing_extensions import Literal
from typing import (
    Dict,
    Union,
    List
)

from pydantic import BaseModel

from errors import InvalidControlChangeValueError


class ContinuousHardwareValues(BaseModel):
    min: int
    max: int
    default: int


class BaseHardware(BaseModel):
    type: str
    cc_number: int
    values: Union[ContinuousHardwareValues, Dict[str, int]]

    def set_hardware_value(self, value: Union[str, int]) -> None:
        ...


class ContinuousHardware(BaseHardware):
    type: Literal["continuous"]
    values: ContinuousHardwareValues

    def set_hardware_value(self, value: int) -> None:
        if not self.values.min <= value <= self.values.max:
            raise InvalidControlChangeValueError(
                value, range(self.values.min, self.values.max + 1)
            )
        print(f"Setting value to {value}")


class DiscreteHardware(BaseHardware):
    type: Literal["discrete"]
    values: Dict[str, int]

    def set_hardware_value(self, value: str) -> None:
        if value not in self.values:
            raise InvalidControlChangeValueError(
                value, list(self.values.keys())
            )
        print(f"Setting value to {value}")


class StrymonPedal(BaseModel):
    name: str
    hardware: Dict[str, Union[DiscreteHardware, ContinuousHardware]]

    def get_hardware_names(self) -> List[str]:
        return list(self.hardware.keys())

    def get_hardware(self, hardware_name: str) -> BaseHardware:
        return self.hardware[hardware_name]

    def set_hardware_value(self, hardware_name: str, value: Union[str, int]) -> None:
        hardware = self.get_hardware(hardware_name)
        hardware.set_hardware_value(value)
