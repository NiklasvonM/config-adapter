from __future__ import annotations

from typing import Any

from .input_strategy import LoaderStrategy
from .typing import Input


class DefaultLoaderStrategy(LoaderStrategy):
    input_source: Input

    def __init__(self, input_source: Input) -> None:
        self.input_source = input_source

    def load(self) -> dict[str, Any]:
        raise ValueError(f"Input source {self.input_source} is not supported")
