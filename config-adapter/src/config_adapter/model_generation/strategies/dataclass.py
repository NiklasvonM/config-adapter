from __future__ import annotations

from .model_generation import InitConfig, ModelGenerationStrategy


class DataclassModelGenerator(ModelGenerationStrategy):
    def __init__(self, config: InitConfig) -> None:
        super().__init__(config=config)
        self.dependencies.add(("dataclasses", "dataclass"))

    def _generate_code(self) -> str:
        code_blocks = []
        for model in self.registry.models.values():
            if model.predefined:
                continue  # Skip predefined models
            model_code = f"@dataclass\nclass {model.name}:\n"
            for field in model.fields:
                field_type = field.type
                model_code += (" " * 4) + f"{field.name}: {field_type}"
                if field.default is not None:
                    model_code += f" = {field.default}"
                model_code += "\n"
            code_blocks.append(model_code)
        return "\n\n".join(code_blocks)
