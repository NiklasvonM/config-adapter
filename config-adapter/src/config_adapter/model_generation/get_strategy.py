from .output_type import OutputType
from .strategies import (
    DataclassModelGenerator,
    DefaultModelGenerator,
    ModelGenerationStrategy,
    PydanticModelGenerator,
)


def get_model_generation_strategy(output_type: OutputType) -> type[ModelGenerationStrategy]:
    if output_type == OutputType.PYDANTIC:
        return PydanticModelGenerator
    if output_type == OutputType.DATACLASS:
        return DataclassModelGenerator
    return DefaultModelGenerator
