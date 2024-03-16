from dataclasses import dataclass

from config_adapter import OutputType, generate_data_models


def main() -> None:
    @dataclass
    class Money:
        amount: float
        currency: str

    existing_models: list[type] = [Money]

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
        "logging": {
            "first_logging": {"level": "INFO", "destination": "file"},
            "second_logging": {"level": "WARNING", "destination": "stdout"},
        },
        "none_type": None,
        "list_type": [{"field1": 1.0}, {"field1": "str"}],
        "costs": {
            "amount": 10.0,
            "currency": "USD",
        },
    }

    model_code = generate_data_models(
        source=json_data, existing_models=existing_models, output_type=OutputType.DATACLASS
    )

    print(model_code)


if __name__ == "__main__":
    main()
