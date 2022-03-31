from time import sleep

import mido
from hardware_definitions.big_sky import StrymonBigSky, FootswitchState, ReverbTypes


def generate_message(channel: int, control_change: StrymonBigSky, val: int) -> mido.Message:
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


if __name__ == "__main__":
    usb_midi = mido.open_output('UM-ONE:UM-ONE MIDI 1 20:0')

    message = StrymonBigSky.footswitch_a(0)
    usb_midi.send(message)
    sleep(1)
    message = StrymonBigSky.footswitch_b(0)
    usb_midi.send(message)
