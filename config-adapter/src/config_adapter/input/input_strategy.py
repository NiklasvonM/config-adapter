from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any


class InputStrategy(ABC):
    @abstractmethod
    def read_input(self, input_source: str | Path | dict[str, Any]) -> dict[str, Any]:
        pass
