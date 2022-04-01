from time import sleep

import mido
from hardware_definitions.big_sky import StrymonBigSky, FootswitchState, ReverbTypes


if __name__ == "__main__":
    usb_midi = mido.open_output('UM-ONE:UM-ONE MIDI 1 20:0')
    big_sky = StrymonBigSky(1)
    message = big_sky.toggle_footswitch_a()
    usb_midi.send(message)
    sleep(1)
    message = big_sky.toggle_footswitch_b()
    usb_midi.send(message)
    sleep(1)
    message = big_sky.toggle_footswitch_c()
    usb_midi.send(message)
