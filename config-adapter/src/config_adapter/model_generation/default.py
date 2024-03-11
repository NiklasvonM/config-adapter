from .model_generation import ModelGenerationStrategy


class DefaultModelGenerator(ModelGenerationStrategy):
    def generate_model_code(self) -> str:
        raise ValueError("Output type not supported.")
