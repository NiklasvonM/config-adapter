from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

import isort
from pydantic import BaseModel

from .util.model import DataModel, UnionType
from .util.model_registry import ModelRegistry
from .util.to_pascal_case import to_pascal_case


class FieldTypeStrategy(ABC):
    @abstractmethod
    def determine_field_type(self, value: Any, key: str) -> str | DataModel:
        pass


class SimpleTypeStrategy(FieldTypeStrategy):
    def determine_field_type(self, value: Any, key: str) -> str:
        if value is None:
            return "None"
        return type(value).__name__


class DictTypeStrategy(FieldTypeStrategy):
    generator_strategy: ModelGenerationStrategy

    def __init__(self, generator_strategy: ModelGenerationStrategy):
        self.generator_strategy = generator_strategy

    def determine_field_type(self, value: dict[str, Any], key: str) -> DataModel:
        matching_model = self.generator_strategy.registry.find_matching_model(data=value)
        if matching_model:
            return matching_model
        # Assume existence of a method to handle dictionary type model generation
        return self.generator_strategy.generate_model_from_dict(
            value, to_pascal_case(key) + "Config"
        )


class ListTypeStrategy(FieldTypeStrategy):
    generator_strategy: ModelGenerationStrategy

    def __init__(self, generator_strategy: ModelGenerationStrategy):
        self.generator_strategy = generator_strategy

    def determine_field_type(self, value: list, key: str) -> str | DataModel:
        unique_types: set[str | DataModel] = set()
        for item in value:
            item_type = self.generator_strategy._determine_field_type(value=item, key=key)
            unique_types.add(item_type)

        if len(unique_types) == 1:
            return f"list[{get_type_string(unique_types.pop())}]"
        if all(isinstance(t, str) for t in unique_types):
            # Create a union of basic types or a single type if all are the same
            return (
                f"list[{' | '.join(get_type_string(unique_type) for unique_type in unique_types)}]"
            )

        # Handle complex scenarios or mixed basic and complex types
        new_model_name = to_pascal_case(key) + "ListItem"
        for item in value:
            self.generator_strategy._populate_model_registry(
                data={key: item}, model_name=new_model_name
            )
        return f"list[{new_model_name}]"


def get_type_string(type_obj: str | DataModel | UnionType) -> str:
    if isinstance(type_obj, str):
        return type_obj  # Assuming `str` types are already in the correct format
    if isinstance(type_obj, DataModel):
        return type_obj.name  # Use the model's name for representation
    if isinstance(type_obj, UnionType):
        # Assuming UnionType has a method to generate a human-readable string of its types
        return str(type_obj)
    return "Any"  # Fallback for unrecognized types


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
        self.registry = ModelRegistry(existing_models=config.existing_models)
        self.dependencies = {("__future__", "annotations")}

    def generate_model_code(self) -> str:
        """
        Generate the model code by populating the model registry with abstract data model
        presentations and then generating the code from them.
        """
        self._populate_model_registry(data=self.data)
        dependencies_code = self._generate_dependency_code()
        models_code = self._generate_code()
        result = dependencies_code + models_code
        return result

    def generate_model_from_dict(self, data: dict[str, Any], model_name: str) -> DataModel:
        model = self.registry.get_or_create_model(name=model_name)
        for key, value in data.items():
            field_type = self._determine_field_type(value=value, key=key)
            model.add_field(name=key, type=field_type)
        return model

    def _populate_model_registry(
        self, data: dict[str, Any], model_name: str = "ConfigAdapter"
    ) -> None:
        """
        Iterate over the data and populate the model registry with matching data models.
        """
        model = self.registry.get_or_create_model(name=model_name)
        for key, value in data.items():
            field_type = self._determine_field_type(value, key)
            model.add_field(name=key, type=field_type)

    def _determine_field_type(self, value: Any, key: str) -> str | DataModel:
        strategy: FieldTypeStrategy
        if isinstance(value, list):
            strategy = ListTypeStrategy(self)
        elif isinstance(value, dict):
            strategy = DictTypeStrategy(self)
        else:
            strategy = SimpleTypeStrategy()
        return strategy.determine_field_type(value=value, key=key)

    @abstractmethod
    def _generate_code(self) -> str:
        """
        Generate the code from the model registry.
        """
        pass

    def _generate_dependency_code(self) -> str:
        """
        Generate code for the import statements of the dependencies.
        """
        dependency_code = ""
        for module_name, field_name in self.dependencies:
            if field_name:
                dependency_code += f"from {module_name} import {field_name}\n"
            else:
                dependency_code += f"import {module_name}\n"

        dependency_code = isort.code(code=dependency_code)

        if dependency_code:
            dependency_code += "\n\n"
        return dependency_code
