import mido
import pydantic
from pydantic import Field


class ControlChangeMessage(pydantic.BaseModel):

    control: int
    value: int

    def get_message(self, channel: int) -> mido.Message:
        return mido.Message(
            "control_change",
            channel=channel,
            control=self.control,
            value=self.value
        )
