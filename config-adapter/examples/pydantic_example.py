from config_adapter import generate_model
from pydantic import BaseModel, Field


def main() -> None:
    class MoneyWithMissing(BaseModel):
        amount: float | None = Field(default=None)
        currency: str

    class MoneyWithoutMissing(BaseModel):
        amount: float
        currency: str

    existing_models: list[type] = [MoneyWithMissing, MoneyWithoutMissing]

    # Sample JSON data with elements to match the existing models
    json_data = {
        "database": {
            "host": "localhost",
            "port": 5432,
            "known_hosts": ["*"],
            "username": "user",
            "password": "pass",
            "schema": "public",
        },
        "first_logging": {"level": "INFO", "destination": "file"},
        "second_logging": {"level": "WARNING", "destination": "stdout"},
        "costs": {
            "amount": 10.0,
            "currency": "USD",
        },
    }

    model_code = generate_model(source=json_data, existing_models=existing_models)

    print(model_code)


if __name__ == "__main__":
    main()
