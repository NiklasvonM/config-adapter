# config-adapter

Automatically create data models from configuration files, taking already defined data models into account.

Currently, `dataclass` as well as Pydantic `BaseModel` generation is supported.

## Example Usage

```py
from config_adapter import generate_model
from pydantic import BaseModel, Field

class Money(BaseModel):
    amount: float
    currency: str

configuration = {
    "database": {
        "host": "localhost",
        "port": 5432,
        "known_hosts": ["*"],
        "username": "user",
    },
    "logging": {
        "first_logging": {"level": "INFO", "destination": "file"},
        "second_logging": {"level": "WARNING", "destination": "stdout"},
    },
    "costs": {
        "amount": 10.0,
        "currency": "USD",
    },
}
model_code = generate_data_models(source=configuration, existing_models=[Money])
print(model_code)
```

```py
from __future__ import annotations

from pydantic import BaseModel

class ConfigAdapter(BaseModel):
    database: DatabaseConfig
    logging: LoggingConfig
    list_type: list[ListTypeConfig]
    costs: Money

class DatabaseConfig(BaseModel):
    host: str
    port: int
    known_hosts: list[str]
    username: str

class LoggingConfig(BaseModel):
    first_logging: FirstLoggingConfig
    second_logging: FirstLoggingConfig

class FirstLoggingConfig(BaseModel):
    level: str
    destination: str

class ListTypeConfig(BaseModel):
    field1: float
```
