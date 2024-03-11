from .default import DefaultModelGenerator
from .model_generation import ModelGenerationStrategy
from .output_type import OutputType
from .pydantic import PydanticModelGenerator


def get_model_generation_strategy(output_type: OutputType) -> type[ModelGenerationStrategy]:
    if output_type == OutputType.PYDANTIC:
        return PydanticModelGenerator
    return DefaultModelGenerator
