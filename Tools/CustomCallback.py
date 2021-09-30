import functools
from typing import Callable
from Tools.MedicationTools import Medicine


def custom_medication_message(function: Callable, medicine: Medicine):
    custom_callable = functools.partial(function, medicine=medicine)
    custom_callable.__name__ = function.__name__
    return custom_callable
