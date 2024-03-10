from config_adapter.loading.dict import DictLoaderStrategy


def test_dict_loader() -> None:
    data = {"key": "value"}
    loader = DictLoaderStrategy(data)
    assert loader.load() == data
