from __future__ import annotations

from .model_generation import ModelGenerationStrategy
from .model_registry import Model


class DataclassModelGenerator(ModelGenerationStrategy):
    def generate_model_code(self) -> str:
        self._generate_recursively(data=self.data)
        return self._generate_code()

    def _generate_code(self) -> str:
        code_blocks = []
        for model in self.registry.models.values():
            if model.predefined:
                continue  # Skip predefined models
            model_code = f"@dataclass\nclass {model.name}:\n"
            for field in model.fields:
                field_type = field.type.name if isinstance(field.type, Model) else field.type
                model_code += f"    {field.name}: {field_type}\n"
            code_blocks.append(model_code)
        return "\n\n".join(code_blocks)
