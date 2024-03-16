from __future__ import annotations

from pathlib import Path
from typing import Any

from .default import DefaultLoaderStrategy
from .dict import DictLoaderStrategy
from .input_strategy import LoaderStrategy
from .json import JSONLoaderStrategy
from .typing import Input
from .yaml import YAMLLoaderStrategy


def get_strategy(input_source: Input) -> LoaderStrategy:
    if isinstance(input_source, dict):
        return DictLoaderStrategy(input_source)
    if isinstance(input_source, str):
        input_source = Path(input_source)
    # TODO: Add support for list[dict]
    if input_source.suffix == ".json":
        return JSONLoaderStrategy(input_source)
    if input_source.suffix == ".yaml":
        return YAMLLoaderStrategy(input_source)
    if input_source.suffix == ".yml":
        return YAMLLoaderStrategy(input_source)
    return DefaultLoaderStrategy(input_source)


def load_input(input_source: Input) -> dict[str, Any]:
    strategy = get_strategy(input_source)
    result = strategy.load()
    return result
