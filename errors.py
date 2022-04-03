from typing import (
    List,
    Union,
)


class InvalidControlChangeValueError(Exception):
    def __init__(self, value: Union[str, int], acceptable_values: Union[range, List[str]]) -> None:

        if isinstance(acceptable_values, range):
            acceptable_values_str = f"{min(acceptable_values)}-{max(acceptable_values)}"
        else:
            acceptable_values_str = ', '.join(val for val in acceptable_values)

        super().__init__(
            f"Passed value \"{value}\" is not valid. \nAcceptable values "
            f"are: {acceptable_values_str}"
        )


class InvalidChannelError(Exception):
    def __init__(self, passed_channel: str) -> None:
        super().__init__(
            f"Passed value {passed_channel} is invalid."
            f"\nChannel must be between 1 and 16"
        )
