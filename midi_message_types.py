import mido
import pydantic
from pydantic import Field


class ControlChangeMessage(pydantic.BaseModel):

    channel: int = Field(..., ge=0, le=15)
    control: int
    value: int

    def generate_message(self) -> mido.Message:
        return mido.Message(
            "control_change",
            channel=self.channel,
            control=self.control,
            value=self.value
        )
