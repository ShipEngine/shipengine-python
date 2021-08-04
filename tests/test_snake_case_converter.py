"""Test test conversion helper function. snake_case -> camelCase."""
from shipengine.util import snake_to_camel


class TestSnakeToCamelCase:
    def test_snake_to_camel(self):
        """Test conversion of snake_case to camelCase."""
        camel_case = snake_to_camel("python_is_awesome")
        assert camel_case == "pythonIsAwesome"
