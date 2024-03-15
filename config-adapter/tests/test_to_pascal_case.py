from config_adapter.model_generation.strategies.util.to_pascal_case import to_pascal_case


def test_underscores():
    assert to_pascal_case("hello_world") == "HelloWorld"
    assert to_pascal_case("hello-world") == "HelloWorld"
    assert to_pascal_case("hello_world_test") == "HelloWorldTest"
    assert to_pascal_case("hello_world_test2") == "HelloWorldTest"


def test_whitespace():
    assert to_pascal_case("hello world") == "HelloWorld"
    assert to_pascal_case("hello world test") == "HelloWorldTest"
    assert to_pascal_case("hell0 w0rld test2") == "HellWRldTest"
    assert to_pascal_case("\nhello\tworld test2\n") == "HelloWorldTest"


def test_dash():
    assert to_pascal_case("hello-world") == "HelloWorld"
    assert to_pascal_case("hello-world-test") == "HelloWorldTest"
    assert to_pascal_case("hello-world-test2") == "HelloWorldTest"


def test_camel_case():
    assert to_pascal_case("helloWorld") == "HelloWorld"
    assert to_pascal_case("helloWorldTest") == "HelloWorldTest"
    assert to_pascal_case("helloWorldTest2") == "HelloWorldTest"


def test_empty():
    assert to_pascal_case("") == ""


def test_multiple():
    assert to_pascal_case("hello-world test2") == "HelloWorldTest"


def test_special_characters():
    assert to_pascal_case("hello$ world€ ?!") == "HelloWorld"
