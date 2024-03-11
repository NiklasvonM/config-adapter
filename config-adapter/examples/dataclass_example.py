from dataclasses import dataclass

from config_adapter import OutputType, generate_model


def main() -> None:
    @dataclass
    class Money:
        amount: float
        currency: str

    existing_models = [Money]

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
        "logging": {"level": "INFO", "destination": "file"},
        "costs": {
            "amount": 10.0,  # Adjusted to float to match MoneyWithoutMissing
            "currency": "USD",
        },
        "another_logging": {"level": "WARNING", "destination": "stdout"},
    }

    model_code = generate_model(
        source=json_data, existing_models=existing_models, output_type=OutputType.DATACLASS
    )

    print(model_code)


if __name__ == "__main__":
    main()
