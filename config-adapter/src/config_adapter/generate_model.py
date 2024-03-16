from __future__ import annotations

from .loading import Input, load_input
from .model_generation import InitConfig, OutputType, get_model_generation_strategy


def generate_data_models(
    source: Input,
    existing_models: list[type] | None = None,
    output_type: OutputType = OutputType.PYDANTIC,
) -> str:
    """
    Generate data models based on the provided source, existing models, and output type.

    Args:
        source (Input): Either something that can be read (file name/path) or a dictionary.
        existing_models (list[type], optional): A list of existing models to be used.
        Defaults to None. Their type should match the output type.
        output_type (OutputType, optional): The type of output for the generated models.
        Defaults to OutputType.PYDANTIC.

    Returns:
        str: The generated model code.
    """
    data = load_input(input_source=source)
    generator_class = get_model_generation_strategy(output_type=output_type)
    config = InitConfig(data=data, existing_models=existing_models or [])
    generator = generator_class(config=config)
    result = generator.generate_model_code()
    return result
