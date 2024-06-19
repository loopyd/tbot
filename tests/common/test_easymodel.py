from src.common.easymodel import EasyModel

class SampleModel(EasyModel):
    name: str
    value: int

def test_to_dict():
    model = SampleModel(name="test", value=123)
    assert model.to_dict() == {"name": "test", "value": 123}

def test_to_json():
    model = SampleModel(name="test", value=123)
    assert model.to_json() == '{"name": "test", "value": 123}'

def test_from_dict():
    data = {"name": "test", "value": 123}
    model = SampleModel.from_dict(data)
    assert model.name == "test"
    assert model.value == 123

def test_from_json():
    json_str = '{"name": "test", "value": 123}'
    model = SampleModel.from_json(json_str)
    assert model.name == "test"
    assert model.value == 123
