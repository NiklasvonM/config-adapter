from __future__ import annotations

from .model_generation import InitConfig, ModelGenerationStrategy
from .util.model_registry import Model


class DataclassModelGenerator(ModelGenerationStrategy):
    def __init__(self, config: InitConfig) -> None:
        super().__init__(config=config)
        self.dependencies.add(("dataclasses", "dataclass"))

    def _generate_code(self) -> str:
        code_blocks = []
        model_code = self._generate_dependency_code()
        for model in self.registry.models.values():
            if model.predefined:
                continue  # Skip predefined models
            model_code = f"@dataclass\nclass {model.name}:\n"
            for field in model.fields:
                field_type = field.type.name if isinstance(field.type, Model) else field.type
                model_code += (" " * 4) + f"{field.name}: {field_type}\n"
            code_blocks.append(model_code)
        return "\n\n".join(code_blocks)
