import typing
from typing import Any, Union, get_type_hints

from .model_generation import ModelGenerationStrategy


class PydanticModelGenerator(ModelGenerationStrategy):
    def generate_model_code(self) -> str:
        result = self.generate_recursively(data=self.data)
        return result

    def generate_recursively(
        self,
        data: dict[str, Any],
        model_name: str = "ConfigAdapter",
        defined_models: dict[str, str] | None = None,
        indent: int = 0,
    ):
        if defined_models is None:
            defined_models = {}
        base_indent = " " * indent
        model_code = f"{base_indent}class {model_name}(BaseModel):\n"
        indent += 4  # Increase indent for the fields
        for key, value in data.items():
            field_type = type(value).__name__
            if field_type == "dict":
                matched_model_name = match_model(
                    json_obj=value, existing_models=self.existing_models
                )
                if not matched_model_name:  # No match found, generate a new model
                    sub_model_name = key.capitalize() + "Config"
                    model_code += self.generate_recursively(
                        data=value,
                        model_name=sub_model_name,
                        defined_models=defined_models,
                        indent=indent,
                    )
                    field_type = sub_model_name
                else:
                    field_type = matched_model_name
            elif field_type == "list":
                field_type = f"list[{type(value[0]).__name__}]" if value else "list[Any]"
            elif field_type in {"str", "int", "float", "bool"}:
                pass  # Use the simple type name directly
            else:
                field_type = "Any"
            model_code += f"{base_indent}{' ' * 4}{key}: {field_type}\n"
        model_code += "\n"
        defined_models[model_name] = model_code
        return model_code


def is_compatible(value: Any, required_type: Any) -> bool:
    if typing.get_origin(required_type) == Union:
        return any(is_compatible(value, arg) for arg in typing.get_args(required_type))
    return isinstance(value, required_type)


def match_model(json_obj: dict, existing_models: list) -> str | None:
    for model in existing_models:
        model_hints = get_type_hints(model)
        if all(field in json_obj for field in model_hints) and all(
            is_compatible(json_obj.get(field), model_hints[field]) for field in model_hints
        ):
            return model.__name__
    return None
