from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from .input_strategy import InputStrategy


class YAMLInputStrategy(InputStrategy):
    def read_input(self, input_source: str | Path) -> dict[str, Any]:
        # Implementation for reading YAML files
        with open(input_source, encoding="UTF-8") as f:
            result = yaml.safe_load(f)
        return result
