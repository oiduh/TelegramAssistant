from typing import Tuple, Dict, List, Callable
from types import ModuleType
from Extensions import TutorialMethods
import inspect
from CommandManager.CommandManager import COMMAND_TYPE


class ExtensionManager:

    # basically a counter for Extensions
    init_group : int = 0

    def __init__(self):
        self.commands: Dict[str, Tuple[int, List[Callable]]] = {}

    def add_commands(self, module: ModuleType) -> Tuple[int, List[Callable]]:
        functions = [func_cls for _, func_cls in inspect.getmembers(module, inspect.isfunction)]
        commands = list(filter(lambda function: COMMAND_TYPE in dir(function), functions))
        group = ExtensionManager.init_group
        self.commands[module.__name__] = (group, commands)
        ExtensionManager.init_group += 1
        return group, commands

    def get_commands(self, module: ModuleType) -> List[Callable]:
        return self.commands[module.__name__][-1]


if __name__ == "__main__":
    em = ExtensionManager()
    em.add_commands(TutorialMethods)
    cmds = em.get_commands(TutorialMethods)
    cmd_test = cmds[-1]
    print(dir(cmd_test))
    print(cmd_test.__command_type__)

