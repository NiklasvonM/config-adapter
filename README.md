# config-adapter

Create data models from configuration files.

## Example Usage

```py
from config_adapter import generate_model
from pydantic import BaseModel, Field

class Money(BaseModel):
    amount: float
    currency: str

existing_models = [Money]

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
        "amount": 10.0,
        "currency": "USD",
    },
    "another_logging": {"level": "WARNING", "destination": "stdout"},
}

model_code = generate_model(source=json_data, existing_models=existing_models)

print(model_code)

```

```py
class ConfigAdapter(BaseModel):
    database: DatabaseConfig
    logging: LoggingConfig
    costs: Money
    another_logging: LoggingConfig


class DatabaseConfig(BaseModel):
    host: str
    port: int
    known_hosts: list[str]
    username: str
    password: str
    schema: str


class LoggingConfig(BaseModel):
    level: str
    destination: str
```
