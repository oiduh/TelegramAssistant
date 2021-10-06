from enum import Enum, auto
from typing import List

COMMAND_TYPE = "__command_type__"
ALIASES = "__alias__"


class CommandType(Enum):
    COMMAND_HANDLER = auto()
    MESSAGE_HANDLER = auto()  # think if this needs an own decorator -> no aliases
    COMMAND_HANDLER_JOB = auto()
    CALLBACK_QUERY_HANDLER = auto()


def command(command_type: CommandType, alias: List[str] = None):
    """decorator to set a command type for the handler adder; can add aliases as well"""
    def decorator_command_type(func):
        func.__command_type__ = command_type
        func.__alias__ = alias
        return func

    return decorator_command_type
