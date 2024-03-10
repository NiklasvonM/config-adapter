from __future__ import annotations

from typing import Any

from .input_strategy import LoaderStrategy


class DictLoaderStrategy(LoaderStrategy):
    input_source: dict[str, Any]

    def __init__(self, input_source: dict[str, Any]) -> None:
        self.input_source = input_source

    def load(self) -> dict[str, Any]:
        return self.input_source
