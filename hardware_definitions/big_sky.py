from enum import (
    Enum,
    IntEnum,
)
from typing import (
    List,
    Union,
)

from errors import (
    InvalidChannelError,
    InvalidControlChangeValueError,
)
from midi_message_types import ControlChangeMessage


class FootswitchState(IntEnum):
    FOOTSWITCH_UP = 127
    FOOTSWITCH_DOWN = 0


class ReverbTypes(IntEnum):
    ROOM = 0
    HALL = 1
    PLATE = 2
    SPRING = 3
    SWELL = 4
    BLOOM = 5
    CLOUD = 6
    CHORALE = 7
    SHIMMER = 8
    MAGNETO = 9
    NONLINEAR = 10
    REFLECTIONS = 11


class StrymonBigSkyCCEnum(Enum):
    TYPE_ENCODER = (19, ReverbTypes.__members__.values())
    DECAY = (17, range(0, 128))
    PRE_DELAY = (18, range(0, 128))
    MIX = (15, range(0, 128))
    TONE = (3, range(0, 128))
    PARAM_1 = (9, range(0, 128))
    PARAM_2 = (16, range(0, 128))
    MOD = (14, range(0, 128))

    FOOTSWITCH_A = (80, [FootswitchState.FOOTSWITCH_UP, FootswitchState.FOOTSWITCH_DOWN])
    FOOTSWITCH_B = (82, [FootswitchState.FOOTSWITCH_UP, FootswitchState.FOOTSWITCH_DOWN])
    FOOTSWITCH_C = (81, [FootswitchState.FOOTSWITCH_UP, FootswitchState.FOOTSWITCH_DOWN])

    def __init__(self, cc_number: int, acceptable_vals: Union[range, List[int]]) -> None:
        self.cc_number = cc_number
        self.acceptable_vals = acceptable_vals


def generate_message(channel: int, message: StrymonBigSkyCCEnum, val: int):

    if val not in message.acceptable_vals:
        raise InvalidControlChangeValueError(val, message.acceptable_vals)

    return ControlChangeMessage(
        channel=channel,
        control=message.cc_number,
        value=val
    ).generate_message()


class StrymonBigSky:
    def __init__(self, channel: int) -> None:
        if 1 > channel < 16:
            raise InvalidChannelError(channel)
        self.channel = channel

    @property
    def actual_channel(self):
        return self.channel - 1

    def toggle_footswitch_a(self):
        return generate_message(
            self.actual_channel,
            StrymonBigSkyCCEnum.FOOTSWITCH_A,
            FootswitchState.FOOTSWITCH_UP
        )

    def toggle_footswitch_b(self):
        return generate_message(
            self.actual_channel,
            StrymonBigSkyCCEnum.FOOTSWITCH_B,
            FootswitchState.FOOTSWITCH_UP
        )

    def toggle_footswitch_c(self):
        return generate_message(
            self.actual_channel,
            StrymonBigSkyCCEnum.FOOTSWITCH_C,
            FootswitchState.FOOTSWITCH_UP
        )
