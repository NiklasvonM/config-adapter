from __future__ import annotations

from pydantic import BaseModel

from .loading import Input, input_to_dict
from .model_generation import PydanticModelGenerator
from .output_type import OutputType


def generate_model(
    source: Input,
    existing_models: list[type[BaseModel]] | None = None,
    output_type: OutputType | None = None,
) -> str:
    data = input_to_dict(source)
    generator = PydanticModelGenerator(data=data, existing_models=existing_models)
    result = generator.generate_model_code()
    return result
