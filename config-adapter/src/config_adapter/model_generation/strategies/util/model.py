from __future__ import annotations


class UnionType:
    types: tuple[str | DataModel, ...]

    def __init__(self, *types: str | DataModel | UnionType):
        self.types = tuple()
        for type in types:
            if isinstance(type, str | DataModel):
                self.types = tuple(set(self.types) | {type})
            elif isinstance(type, UnionType):
                self.types = tuple(set(self.types) | set(type.types))

    def __str__(self) -> str:
        return " | ".join(str(t) for t in self.types)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({', '.join(repr(t) for t in self.types)})"

    def add_type(self, new_type: str | DataModel | UnionType):
        if new_type not in self.types:
            if isinstance(new_type, str | DataModel):
                self.types += (new_type,)
            elif isinstance(new_type, UnionType):
                self.types += new_type.types

    def __add__(self, new_type: str | DataModel | UnionType) -> UnionType:
        result = UnionType(*self.types)
        result.add_type(new_type=new_type)
        return result


class ModelField:
    name: str
    type: TypeSystem
    default: str | None
    """
    The default value as a string, for example `"Field(default_factory=uuid.uuid4)"`.
    If None, the field does not have a default value.
    """

    def __init__(
        self, name: str, type: str | DataModel | UnionType | TypeSystem, default: str | None = None
    ):
        self.name = name
        if isinstance(type, TypeSystem):
            self.type = type
        else:
            self.type = TypeSystem(type)
        self.default = default


class DataModel:
    name: str
    fields: list[ModelField]
    predefined: bool
    """Indicates whether the model is predefined (by the user) or generated"""

    def __init__(self, name: str, predefined: bool = False):
        self.name = name
        self.fields = []
        self.predefined = predefined

    def add_field(self, name: str, type: str | DataModel | UnionType, default: str | None = None):
        existing_field = next((field for field in self.fields if field.name == name), None)
        if existing_field:
            existing_field.type += type
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

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}"
            f"(name={self.name}, "
            f"fields=[{', '.join(repr(field) for field in self.fields)}], "
            f"predefined={self.predefined})"
        )

    def __mul__(self, other: DataModel) -> DataModel:
        """
        Merges two models by taking their "product", returning a new model with the combined fields.
        """
        new_model = DataModel(name=other.name, predefined=False)
        for field in self.fields + other.fields:
            new_model.add_field(name=field.name, type=field.type, default=field.default)
        return new_model


class TypeSystem:
    base: str | DataModel | UnionType

    def __init__(self, base: str | DataModel | UnionType | None = None):
        self.base = base

    def __add__(self, other: TypeSystem) -> TypeSystem:
        return TypeSystem(UnionType(self.base, other.base))

    def __mul__(self, other: TypeSystem) -> TypeSystem:
        if isinstance(self.base, DataModel) and isinstance(other.base, DataModel):
            return TypeSystem(self.base * other.base)
        return self + other

    def __str__(self):
        return str(self.base)
