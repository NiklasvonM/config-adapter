from __future__ import annotations

import typing
from typing import Any, Union, get_args, get_origin, get_type_hints

from .model import DataModel


class ModelRegistry:
    """
    A registry for abstract data models.
    """

    models: dict[str, DataModel]

    def __init__(self, existing_models: list[type]):
        """
        Initialize the class with existing models.

        Parameters:
            existing_models (list[type]): A list of existing model types.

        Example:
            ```
            class ExistingModel(BaseModel):
                ...

            model_registry = ModelRegistry(existing_models=[ExistingModel])
            ```
        """
        self.models = {}
        for model_cls in existing_models:
            self._add_existing_model(model_cls)

    def _add_existing_model(self, model_cls: type):
        model_name = model_cls.__name__
        model = DataModel(name=model_name, predefined=True)
        type_hints = get_type_hints(model_cls)
        for field_name, field_type in type_hints.items():
            model.add_field(field_name, self._simplify_type(field_type))
        self.models[model_name] = model

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

    def get_or_create_model(self, name: str) -> DataModel:
        """
        Get or create a model by name.

        Args:
            name (str): The name of the model.

        Returns:
            Model: The model object. If the model does not exist, it will be created.
        """
        if name not in self.models:
            self.models[name] = DataModel(name=name)
        return self.models[name]

    def find_matching_model(self, data: dict[str, Any]) -> DataModel | None:
        """
        Find the model that matches the data. If no model matches it, return None.
        """
        # TODO: find the best (i.e., the most restrictive) matching model, not just any
        for model in self.models.values():
            model_field_names = {field.name for field in model.fields}
            # TODO: Match types as well: Type has to be supertype of the data type.
            # If the types don't match, perhaps log this as an almost matching model.
            if model_field_names == set(data.keys()):
                return model
        return None
