from time import sleep

import mido
import os
from pydantic import parse_file_as
from hardware_definitions.states import StrymonPedal

if __name__ == "__main__":
    usb_midi = mido.open_output('UM-ONE:UM-ONE MIDI 1 20:0')
    big_sky_path = os.path.join(os.path.dirname(__file__), "hardware_definitions", "big_sky.json")
    big_sky = parse_file_as(StrymonPedal, big_sky_path)
    print(big_sky.get_hardware_names())
    big_sky.set_hardware_value("Decay Knob", 0)
    big_sky.set_hardware_value("Reverb Type", "Hall")
