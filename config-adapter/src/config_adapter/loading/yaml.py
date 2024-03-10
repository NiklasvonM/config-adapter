from __future__ import annotations

from typing import Any

import yaml

from .input_strategy import LoaderStrategy
from .typing import Readable


class YAMLLoaderStrategy(LoaderStrategy):
    input_source: Readable

    def __init__(self, input_source: Readable) -> None:
        self.input_source = input_source

    def load(self) -> dict[str, Any]:
        # Implementation for reading YAML files
        with open(self.input_source, encoding="UTF-8") as f:
            result = yaml.safe_load(f)
        return result
