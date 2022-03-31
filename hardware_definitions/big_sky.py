from enum import (
    Enum,
    IntEnum,
)
from typing import (
    List,
    Union,
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




class StrymonBigSky(Enum):
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

    @staticmethod
    def _generate_message(channel: int, message):
        return ControlChangeMessage(
            channel=channel,
            control=message.cc_number,
            value=FootswitchState.FOOTSWITCH_UP
        ).generate_message()

    @classmethod
    def footswitch_a(cls, channel: int):
        return cls._generate_message(channel, cls.FOOTSWITCH_A)

    @classmethod
    def footswitch_b(cls, channel: int):
        return cls._generate_message(channel, cls.FOOTSWITCH_B)
