from CommandManager.CommandManager import CommandType
from typing import List


def command(command_type: CommandType, alias: List[str] = None):
    def decorator_command_type(func):
        func.__command_type__ = command_type
        func.__alias__ = alias
        return func

    return decorator_command_type


@command(CommandType.COMMAND_HANDLER)
def say_hello():
    print("hey")


@command(CommandType.MESSAGE_HANDLER)
def echo():
    print("echo")


def helper():
    print("helper")


def print_type(func):
    if "__command_type" in dir(func):
        print(func.__command_type.name)


def filter_commands(funcs):
    filter_list = filter(lambda func: "__command_type" in dir(func), funcs)
    return list(filter_list)


if __name__ == "__main__":
    func_1 = say_hello
    func_2 = echo
    func_1
    print(func_1.__command_type__)
    func_2
    print(func_2.__command_type__)

    func_3 = helper
    func_3()
    func_3_attr = set(dir(func_3))
    func_1_attr = set(dir(func_1))
    print(func_1_attr.difference(func_3_attr))

    print_type(func_1)
    print_type(func_2)
    print_type(func_3)

    func_list = [command, func_1, func_2, func_3]

    print(func_list)
    print(filter_commands(func_list))