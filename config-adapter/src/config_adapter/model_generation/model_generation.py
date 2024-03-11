from abc import ABC, abstractmethod
from typing import Any

from .model_registry import Model, ModelRegistry


class ModelGenerationStrategy(ABC):
    data: dict[str, Any]
    registry: ModelRegistry

    def __init__(self, data: dict[str, Any], existing_models: list[type] | None = None) -> None:
        self.data = data
        if existing_models is None:
            existing_models = []
        self.registry = ModelRegistry(existing_models=existing_models)

    def generate_model_code(self) -> str:
        self._generate_recursively(data=self.data)
        result = self._generate_code()
        return result

    def _generate_recursively(self, data: dict, model_name: str = "ConfigAdapter"):
        model = self.registry.get_or_create_model(model_name)
        for key, value in data.items():
            field_type = self._determine_field_type(value, key)
            model.add_field(key, field_type)

    def _determine_field_type(self, value: Any, key: str) -> str | Model:
        if isinstance(value, dict):
            # Attempt to find a matching model
            matching_model = self.registry.find_matching_model(value)
            if matching_model:
                return matching_model
            # Create a new model
            sub_model_name = key.capitalize() + "Config"
            self._generate_recursively(data=value, model_name=sub_model_name)
            return self.registry.get_or_create_model(sub_model_name)
        if isinstance(value, list):
            list_type = "Any" if not value else self._determine_field_type(value[0], key)
            return f"list[{list_type}]"
        if isinstance(value, str | int | float | bool):
            return type(value).__name__
        return "Any"

    @abstractmethod
    def _generate_code(self) -> str:
        pass
