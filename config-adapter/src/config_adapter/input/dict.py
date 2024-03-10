from __future__ import annotations

from typing import Any

from .input_strategy import InputStrategy


class DictInputStrategy(InputStrategy):
    def read_input(self, input_source: dict[str, Any]) -> dict[str, Any]:
        return input_source
