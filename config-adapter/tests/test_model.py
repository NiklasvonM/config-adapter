from config_adapter.model_generation.strategies.util.model import Model, UnionType


def test_model_creation():
    model = Model(name="TestModel", predefined=True)
    assert model.name == "TestModel"
    assert model.predefined is True
    assert len(model.fields) == 0


def test_add_field_to_model():
    model = Model(name="TestModel")
    model.add_field(name="name", type="str")
    assert len(model.fields) == 1
    assert model.fields[0].name == "name"
    assert model.fields[0].type.types == ("str",)


def test_add_duplicate_field_with_same_type():
    model = Model(name="TestModel")
    model.add_field("name", "str")
    model.add_field("name", "str")  # Attempt to add a duplicate field with the same type
    assert len(model.fields) == 1  # Ensure no duplicate field is added


def test_add_duplicate_field_with_different_type_creates_union():
    model = Model(name="TestModel")
    model.add_field("name", "str")
    model.add_field("name", "int")  # Add a duplicate field with a different type
    assert len(model.fields) == 1
    field_type = model.fields[0].type
    assert isinstance(field_type, UnionType)
    assert "str" in field_type.types
    assert "int" in field_type.types


def test_union_type_representation():
    union = UnionType("str", "int")
    assert repr(union) == "str | int"


def test_model_addition_creates_combined_fields():
    model1 = Model(name="User")
    model1.add_field("name", "str")
    model2 = Model(name="Admin")
    model2.add_field("level", "int")
    combined_model = model1 + model2
    assert len(combined_model.fields) == 2
    assert combined_model.field_exists("name")
    assert combined_model.field_exists("level")
