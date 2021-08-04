"""Test data as functions and common assertion helper functions."""
from typing import Any, Dict, List

from shipengine import ShipEngine, ShipEngineConfig
from shipengine.enums import Constants


def stub_config(
    retries: int = 1,
) -> Dict[str, Any]:
    """
    Return a test configuration dictionary to be used
    when instantiating the ShipEngine object.
    """
    return dict(
        api_key=Constants.STUB_API_KEY.value,
        page_size=50,
        retries=retries,
        timeout=15,
    )


def stub_shipengine_config() -> ShipEngineConfig:
    """Return a valid test ShipEngineConfig object."""
    return ShipEngineConfig(config=stub_config())


def configurable_stub_shipengine_instance(config: Dict[str, any]) -> ShipEngine:
    """"""
    return ShipEngine(config=config)


def stub_shipengine_instance() -> ShipEngine:
    """Return a test instance of the ShipEngine object."""
    return ShipEngine(config=stub_config())


def valid_commercial_address() -> List[Dict[str, Any]]:
    return [
        {
            "name": "ShipEngine",
            "company": "Auctane",
            "phone": "1-123-123-1234",
            "address_line1": "3800 N Lamar Blvd",
            "address_line2": "ste 220",
            "city_locality": "Austin",
            "state_province": "TX",
            "postal_code": "78756",
            "country_code": "US",
            "address_residential_indicator": "unknown",
        }
    ]
