from __future__ import annotations


class UnionType:
    types: tuple[str | Model, ...]

    def __init__(self, *types: str | Model | UnionType):
        self.types = tuple()
        for type in types:
            if isinstance(type, str | Model):
                self.types = tuple(set(self.types) | {type})
            elif isinstance(type, UnionType):
                self.types = tuple(set(self.types) | set(type.types))

    def __str__(self):
        return " | ".join(str(t) for t in self.types)

    def add_type(self, new_type: str | Model | UnionType):
        if new_type not in self.types:
            if isinstance(new_type, str | Model):
                self.types += (new_type,)
            elif isinstance(new_type, UnionType):
                self.types += new_type.types

    def __add__(self, new_type: str | Model | UnionType) -> UnionType:
        result = UnionType(*self.types)
        result.add_type(new_type=new_type)
        return result


class ModelField:
    name: str
    type: UnionType
    default: str | None
    """
    The default value as a string, for example `"Field(default_factory=uuid.uuid4)"`.
    If None, the field does not have a default value.
    """

    def __init__(self, name: str, type: str | Model | UnionType, default: str | None = None):
        self.name = name
        self.type = UnionType(type)
        self.default = default


class Model:
    name: str
    fields: list[ModelField]
    predefined: bool
    """Indicates whether the model is predefined (by the user) or generated"""

    def __init__(self, name: str, predefined: bool = False):
        self.name = name
        self.fields = []
        self.predefined = predefined

    def add_field(self, name: str, type: str | Model | UnionType, default: str | None = None):
        existing_field = next((field for field in self.fields if field.name == name), None)
        if existing_field:
            existing_field.type.add_type(new_type=type)
            # TODO: Handle the case when there are two default values.
            if existing_field.default is None:
                existing_field.default = default
        else:
            self.fields.append(ModelField(name=name, type=type, default=default))

    def field_exists(self, name: str) -> bool:
        """Checks if a field with the given name exists in the model."""
        return any(field.name == name for field in self.fields)

    def __str__(self) -> str:
        return self.name

    def __mul__(self, other: Model) -> Model:
        """
        Merges two models by taking their "product", returning a new model with the combined fields.
        """
        new_model = Model(name=other.name, predefined=False)
        for field in self.fields + other.fields:
            new_model.add_field(name=field.name, type=field.type, default=field.default)
        return new_model
