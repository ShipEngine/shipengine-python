"""The global configuration object for the ShipEngine SDK."""
import json
from typing import Any, Dict, Optional

from .enums import BaseURL
from .util import is_api_key_valid, is_retries_valid, is_timeout_valid


class ShipEngineConfig:
    DEFAULT_BASE_URI: str = BaseURL.SHIPENGINE_RPC_URL.value
    """A ShipEngine API Key, sandbox API Keys start with `TEST_`."""

    DEFAULT_PAGE_SIZE: int = 50
    """Default page size for responses from ShipEngine API."""

    DEFAULT_RETRIES: int = 1
    """Default number of retries the ShipEngineClient should make before returning an exception."""

    DEFAULT_TIMEOUT: int = 5
    """Default timeout for the ShipEngineClient in seconds."""

    def __init__(self, config: Dict[str, Any]) -> None:
        """
        This is the configuration object for the ShipEngine object and it"s properties are
        used throughout this SDK.
        """
        is_api_key_valid(config)
        self.api_key: str = config["api_key"]

        is_timeout_valid(config)
        if "timeout" in config:
            self.timeout: int = config["timeout"]
        else:
            self.timeout: int = self.DEFAULT_TIMEOUT

        if "base_uri" in config:
            self.base_uri: str = config["base_uri"]
        else:
            self.base_uri: str = self.DEFAULT_BASE_URI

        if "page_size" in config:
            self.page_size: int = config["page_size"]
        else:
            self.page_size: int = self.DEFAULT_PAGE_SIZE

        is_retries_valid(config)
        if "retries" in config:
            self.retries: int = config["retries"]
        else:
            self.retries: int = self.DEFAULT_RETRIES

    def merge(self, new_config: Optional[Dict[str, Any]] = None):
        """
        The method allows the merging of a method-level configuration
        adjustment into the current configuration.
        """
        if new_config is None:
            return self
        else:
            config = dict()

            config.update(
                {"api_key": new_config["api_key"]}
            ) if "api_key" in new_config else config.update({"api_key": self.api_key})

            config.update(
                {"base_uri": new_config["base_uri"]}
            ) if "base_uri" in new_config else config.update({"base_uri": self.base_uri})

            config.update(
                {"page_size": new_config["page_size"]}
            ) if "page_size" in new_config else config.update({"page_size": self.page_size})

            config.update(
                {"retries": new_config["retries"]}
            ) if "retries" in new_config else config.update({"retries": self.retries})

            config.update(
                {"timeout": new_config["timeout"]}
            ) if "timeout" in new_config else config.update({"timeout": self.timeout})

            return ShipEngineConfig(config)

    def to_dict(self):
        return (lambda o: o.__dict__)(self)

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=2)
