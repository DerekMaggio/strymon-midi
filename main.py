from time import sleep

import mido
import os
from pydantic import parse_file_as
from hardware_definitions.states import BigSkyPedal

if __name__ == "__main__":
    usb_midi = mido.open_output('UM-ONE:UM-ONE MIDI 1 20:0')
    big_sky = BigSkyPedal(channel=1)
    usb_midi.send(big_sky.get_message("Reverb Type", "Bloom"))
