from __future__ import annotations

import json
from typing import Any

from .input_strategy import LoaderStrategy
from .typing import Readable


class JSONLoaderStrategy(LoaderStrategy):
    input_source: Readable

    def __init__(self, input_source: Readable) -> None:
        self.input_source = input_source

    def load(self) -> dict[str, Any]:
        # Implementation for reading JSON files or strings
        with open(self.input_source, encoding="UTF-8") as f:
            result = json.load(f)
        return result
