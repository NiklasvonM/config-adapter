from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .input_strategy import InputStrategy


class JSONInputStrategy(InputStrategy):
    def read_input(self, input_source: str | Path) -> dict[str, Any]:
        # Implementation for reading JSON files or strings
        with open(input_source, encoding="UTF-8") as f:
            result = json.load(f)
        return result
