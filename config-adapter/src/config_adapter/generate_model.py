from __future__ import annotations

from pydantic import BaseModel

from .loading import Input, input_to_dict
from .model_generation import OutputType, get_model_generation_strategy


def generate_model(
    source: Input,
    existing_models: list[type[BaseModel]] | None = None,
    output_type: OutputType | None = None,
) -> str:
    data = input_to_dict(source)
    generator_class = get_model_generation_strategy(output_type or OutputType.PYDANTIC)
    generator = generator_class(data=data, existing_models=existing_models)
    result = generator.generate_model_code()
    return result
