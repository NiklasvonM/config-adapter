from __future__ import annotations

from .loading import Input, input_to_dict
from .model_generation import InitConfig, OutputType, get_model_generation_strategy


def generate_model(
    source: Input,
    existing_models: list[type] | None = None,
    output_type: OutputType | None = None,
) -> str:
    data = input_to_dict(source)
    generator_class = get_model_generation_strategy(output_type or OutputType.PYDANTIC)
    config = InitConfig(data=data, existing_models=existing_models or [])
    generator = generator_class(config=config)
    result = generator.generate_model_code()
    return result
