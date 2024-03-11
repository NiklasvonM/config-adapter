from __future__ import annotations

import typing
from typing import Any, Union, get_args, get_origin, get_type_hints

from .model_generation import ModelGenerationStrategy


class ModelField:
    name: str
    type: str | Model

    def __init__(self, name: str, type: str | Model):
        self.name = name
        self.type = type


class Model:
    name: str
    fields: list[ModelField]
    predefined: bool  # Indicates whether the model is predefined or generated

    def __init__(self, name: str, predefined: bool = False):
        self.name = name
        self.fields = []
        self.predefined = predefined

    def add_field(self, name: str, type: str | Model):
        self.fields.append(ModelField(name=name, type=type))


class ModelRegistry:
    models: dict[str, Model]

    def __init__(self, existing_models: list[type]):
        self.models = {}
        for model_cls in existing_models:
            self._add_existing_model(model_cls)

    def _add_existing_model(self, model_cls: type):
        model_name = model_cls.__name__
        if model_name not in self.models:
            model = Model(name=model_name, predefined=True)
            self.models[model_name] = model
        else:
            model = self.models[model_name]
        type_hints = get_type_hints(model_cls)
        for field_name, field_type in type_hints.items():
            # Simplified type handling, might need to handle more complex cases
            model.add_field(field_name, self._simplify_type(field_type))

    def _simplify_type(self, field_type: Any) -> str:
        if get_origin(field_type) in {Union, typing.Union}:
            args = get_args(field_type)
            simplified_types = (self._simplify_type(arg) for arg in args)
            return " | ".join(simplified_types)

        # Handle generic types (List, Dict, etc.)
        if hasattr(field_type, "__origin__"):
            # Simplify the arguments of the generic type
            args_simplified = (self._simplify_type(arg) for arg in get_args(field_type))
            origin_type_name = field_type.__origin__.__name__
            return f'{origin_type_name}[{", ".join(args_simplified)}]'

        # Handle simple types
        if hasattr(field_type, "__name__"):
            return field_type.__name__

        # Fallback for unsupported types
        return "Any"

    def get_or_create_model(self, name: str) -> Model:
        if name not in self.models:
            self.models[name] = Model(name=name)
        return self.models[name]

    def find_matching_model(self, data: dict[str, Any]) -> Model | None:
        # TODO: find the best (i.e., the most restrictive) matching model, not just any
        for model in self.models.values():
            model_field_names = {field.name for field in model.fields}
            if model_field_names == set(data.keys()):
                # Optionally, add further type compatibility checks here
                return model
        return None


class PydanticModelGenerator(ModelGenerationStrategy):
    registry: ModelRegistry

    def __init__(self, data: dict[str, Any], existing_models: list[type] | None = None) -> None:
        super().__init__(data=data, existing_models=existing_models)
        self.registry = ModelRegistry(existing_models=self.existing_models)

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

    def _generate_code(self) -> str:
        code_blocks = []
        for model in self.registry.models.values():
            if model.predefined:
                continue  # Skip predefined models
            model_code = f"class {model.name}(BaseModel):\n"
            for field in model.fields:
                field_type = field.type.name if isinstance(field.type, Model) else field.type
                model_code += f"    {field.name}: {field_type}\n"
            code_blocks.append(model_code)
        return "\n\n".join(code_blocks)
