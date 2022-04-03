import os
import typing
from dataclasses import dataclass

import mido
from typing_extensions import Literal
from typing import (
    Dict,
    Union,
    List
)

from pydantic import (
    BaseModel,
    parse_file_as,
    validator,
)

from errors import InvalidControlChangeValueError
from midi_message_types import ControlChangeMessage


class ContinuousHardwareValues(BaseModel):
    min: int
    max: int
    default: int


class BaseHardware(BaseModel):
    name: str
    type: str
    cc_number: int
    values: Union[ContinuousHardwareValues, Dict[str, int]]

    def get_message(self, value: Union[str, int]) -> ControlChangeMessage:
        ...

    def _generate_midi_cc_message(self, value: int) -> ControlChangeMessage:
        return ControlChangeMessage(control=self.cc_number, value=value)


class ContinuousHardware(BaseHardware):
    type: Literal["continuous"]
    values: ContinuousHardwareValues

    def get_message(self, value: int) -> ControlChangeMessage:
        if not self.values.min <= value <= self.values.max:
            raise InvalidControlChangeValueError(
                value, range(self.values.min, self.values.max + 1)
            )
        print(f"Setting {self.name}: {value}")
        return self._generate_midi_cc_message(value)


class DiscreteHardware(BaseHardware):
    type: Literal["discrete"]
    values: Dict[str, int]

    def get_message(self, value: str) -> ControlChangeMessage:
        if value not in self.values:
            raise InvalidControlChangeValueError(
                value, list(self.values.keys())
            )
        print(f"Setting {self.name}: {value}")
        return self._generate_midi_cc_message(self.values[value])


class StrymonPedal(BaseModel):
    name: str
    hardware: Dict[str, Union[DiscreteHardware, ContinuousHardware]]

    @validator("hardware", pre=True)
    def add_name_to_hardware(cls, hardware_defs):
        for name, hardware in hardware_defs.items():
            hardware["name"] = name
        return hardware_defs

    def get_hardware_names(self) -> List[str]:
        return list(self.hardware.keys())

    def get_hardware(self, hardware_name: str) -> BaseHardware:
        return self.hardware[hardware_name]

    def get_message(self, hardware_name: str, value: Union[str, int]) -> ControlChangeMessage:
        return self.get_hardware(hardware_name).get_message(value)



@dataclass
class BigSkyPedal:
    channel: int
    definition: StrymonPedal = parse_file_as(
        StrymonPedal, os.path.join(os.path.dirname(__file__), "big_sky.json")
    )

    @property
    def actual_channel(self):
        return self.channel - 1

    def get_message(self, hardware_name: str, value: Union[str, int]) -> mido.Message:
        return self.definition.get_message(hardware_name, value).get_message(self.actual_channel)
