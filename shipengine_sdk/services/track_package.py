"""Track a given package to obtain status updates on it's progression through the fulfillment cycle."""
from typing import Union

from ..jsonrpc import rpc_request
from ..models import RPCMethods, TrackingQuery, TrackPackageResult
from ..shipengine_config import ShipEngineConfig
from ..util import is_package_id_valid


def track(tracking_data: Union[str, TrackingQuery], config: ShipEngineConfig) -> TrackPackageResult:
    if type(tracking_data) is str:
        is_package_id_valid(tracking_data)

        api_response = rpc_request(
            method=RPCMethods.TRACK_PACKAGE.value,
            config=config,
            params={"packageId": tracking_data},
        )

        return TrackPackageResult(api_response, config)

    if type(tracking_data) is TrackingQuery:
        api_response = rpc_request(
            method=RPCMethods.TRACK_PACKAGE.value, config=config, params=tracking_data.to_dict()  # type: ignore
        )

        return TrackPackageResult(api_response, config)
