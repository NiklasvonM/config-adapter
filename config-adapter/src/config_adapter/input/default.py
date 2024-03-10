from __future__ import annotations

from pathlib import Path
from typing import Any

from .input_strategy import InputStrategy


class DefaultInputStrategy(InputStrategy):
    def read_input(self, input_source: str | Path) -> dict[str, Any]:
        raise ValueError(f"Input source {input_source} is not supported")
