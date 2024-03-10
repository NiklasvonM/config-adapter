from abc import ABC, abstractmethod
from typing import Any


class ModelGenerationStrategy(ABC):
    data: dict[str, Any]
    existing_models: list[type]

    def __init__(self, data: dict[str, Any], existing_models: list[type] | None = None) -> None:
        self.data = data
        if existing_models is None:
            existing_models = []
        self.existing_models = existing_models

    @abstractmethod
    def generate_model_code(self) -> str:
        pass
