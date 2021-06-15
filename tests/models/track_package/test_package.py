"""Testing the Package class object."""
from typing import Any, Dict

from shipengine_sdk.models import Package


def stub_package_data() -> Dict[str, Any]:
    return {
        "packageID": "pkg_1FedExAccepted",
        "trackingNumber": "5fSkgyuh3GkfUjTZSEAQ8gHeTU29tZ",
        "trackingURL": "https://www.fedex.com/track/5fSkgyuh3GkfUjTZSEAQ8gHeTU29tZ",
        "weight": {"value": 76, "unit": "kilogram"},
        "dimensions": {"length": 36, "width": 36, "height": 23, "unit": "inch"},
    }


def stub_package() -> Package:
    """Return a valid stub Package object."""
    return Package(stub_package_data())


class TestPackage:
    def test_package_to_dict(self) -> None:
        package = stub_package()
        assert type(package.to_dict()) is dict

    def test_package_to_json(self) -> None:
        package = stub_package()
        assert type(package.to_json()) is str
