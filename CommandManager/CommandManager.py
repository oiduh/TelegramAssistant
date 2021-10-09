from enum import Enum, auto
from typing import List

COMMAND_TYPE_ATTR = "__command_type__"
ALIASES_ATTR = "__aliases__"


class CommandType(Enum):
    COMMAND_HANDLER = auto()
    MESSAGE_HANDLER = auto()  # think if this needs an own decorator -> no aliases
    COMMAND_HANDLER_JOB = auto()
    CALLBACK_QUERY_HANDLER = auto()


def command(command_type: CommandType, aliases: List[str] = None):
    """decorator to set a command type for the handler adder; can add aliases as well"""
    def decorator_command_type(func):
        # TODO: think about handling this in a cleaner way, same goes for getattr
        setattr(func, COMMAND_TYPE_ATTR, command_type)
        if aliases:
            setattr(func, ALIASES_ATTR, aliases)
        return func

    return decorator_command_type


if __name__ == "__main__":
    pass