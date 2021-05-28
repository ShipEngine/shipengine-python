"""Initial Docstring"""
from shipengine_sdk.util import snake_to_camel


class TestSnakeToCamelCase:
    def test_snake_to_camel(self):
        camel_case = snake_to_camel("python_is_awesome")
        assert camel_case == "pythonIsAwesome"
