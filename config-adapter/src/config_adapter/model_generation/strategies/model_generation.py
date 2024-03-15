from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel

from .util.model_registry import Model, ModelRegistry
from .util.to_pascal_case import to_pascal_case


class InitConfig(BaseModel):
    data: dict[str, Any]
    existing_models: list[type] = []


class ModelGenerationStrategy(ABC):
    data: dict[str, Any]
    registry: ModelRegistry
    dependencies: set[tuple[str, str | None]]
    """
    Set of dependencies, where each element is a tuple of (model_name, field_name).
    `(model_name, field_name)` becomes `from model_name import field_name`.
    `(mode_name, None)` becomes `import model_name`.
    """

    def __init__(self, config: InitConfig) -> None:
        self.data = config.data
        self.existing_models = config.existing_models
        self.registry = ModelRegistry(existing_models=self.existing_models)
        self.dependencies = set()

    def generate_model_code(self) -> str:
        self._generate_recursively(data=self.data)
        dependencies_code = self._generate_dependency_code()
        models_code = self._generate_code()
        result = dependencies_code + models_code
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
            sub_model_name = to_pascal_case(key) + "Config"
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

    def _generate_dependency_code(self) -> str:
        dependency_code = ""
        for module_name, field_name in self.dependencies:
            if field_name:
                dependency_code += f"from {module_name} import {field_name}\n"
            else:
                dependency_code += f"import {module_name}\n"
        if dependency_code:
            dependency_code += "\n"
        return dependency_code
