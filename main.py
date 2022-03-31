from typing import (
    List,
    Union,
)

import mido
from enum import IntEnum, Enum
from dataclasses import dataclass


@dataclass
class ControlChange:
    id: int
    val_range: Union[range, List[int]]


class FootswitchState(IntEnum):
    FOOTSWITCH_UP = 127
    FOOTSWITCH_DOWN = 0

class StrymonBigSkyControlChangeEnum(Enum):
    TYPE_ENCODER = (19, range(0, 12))
    FOOTSWITCH_A = (80, [FootswitchState.FOOTSWITCH_UP, FootswitchState.FOOTSWITCH_DOWN])
    FOOTSWITCH_B = (82, [FootswitchState.FOOTSWITCH_UP, FootswitchState.FOOTSWITCH_DOWN])
    FOOTSWITCH_C = (81, [FootswitchState.FOOTSWITCH_UP, FootswitchState.FOOTSWITCH_DOWN])

    def __init__(self, cc_number: int, acceptable_vals: Union[range, List[int]]) -> None:
        self.cc_number = cc_number
        self.acceptable_vals = acceptable_vals


def generate_message(channel: int, control_change: StrymonBigSkyControlChangeEnum, val: int) -> mido.Message:
    if val not in control_change.acceptable_vals:
        print(val)
        print(control_change.acceptable_vals)
        raise ValueError("You passed an unacceptable value")

    return mido.Message(
        "control_change",
        channel=channel,
        control=control_change.cc_number,
        value=val
    )


class StrymonBigSky:
    ...

if __name__ == "__main__":
    usb_midi = mido.open_output('UM-ONE:UM-ONE MIDI 1 20:0')

    message = generate_message(0, StrymonBigSkyControlChangeEnum.FOOTSWITCH_A, FootswitchState.FOOTSWITCH_UP)
    usb_midi.send(message)
