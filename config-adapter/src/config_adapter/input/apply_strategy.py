from typing import Any

from .default import DefaultInputStrategy
from .dict import DictInputStrategy
from .input_strategy import InputStrategy
from .json import JSONInputStrategy
from .typing import Input
from .yaml import YAMLInputStrategy


def get_strategy(input_source: Input) -> InputStrategy:
    if isinstance(input_source, dict):
        return DictInputStrategy()
    # TODO: Add support for list[dict]
    if input_source.endswith(".json"):
        return JSONInputStrategy()
    if input_source.endswith(".yaml"):
        return YAMLInputStrategy()
    if input_source.endswith(".yml"):
        return YAMLInputStrategy()
    return DefaultInputStrategy()


def input_to_dict(input_source: Input) -> dict[str, Any]:
    strategy = get_strategy(input_source)
    result = strategy.read_input(input_source)
    return result
