from __future__ import annotations

import typing
from typing import Any, Union, get_args, get_origin, get_type_hints


class ModelField:
    name: str
    type: str | Model

    def __init__(self, name: str, type: str | Model):
        self.name = name
        self.type = type


class Model:
    name: str
    fields: list[ModelField]
    predefined: bool
    """Indicates whether the model is predefined (by the user) or generated"""

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
                return model
        return None
