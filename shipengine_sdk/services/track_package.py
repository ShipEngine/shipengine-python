"""Track a given package to obtain status updates on it's progression through the fulfillment cycle."""
from typing import Dict, Union

from ..errors import ShipEngineError
from ..jsonrpc import rpc_request
from ..models import RPCMethods
from ..models.track_pacakge import TrackingQuery, TrackPackageResult
from ..shipengine_config import ShipEngineConfig
from ..util import is_package_id_valid


def track(
    tracking_data: Union[str, Dict[str, any], TrackingQuery], config: ShipEngineConfig
) -> TrackPackageResult:
    if type(tracking_data) is str:
        is_package_id_valid(tracking_data)

        api_response = rpc_request(
            method=RPCMethods.LIST_CARRIERS.value,
            config=config,
            params={"packageID": tracking_data},
        )

        return TrackPackageResult(api_response, config)

    if type(tracking_data) is TrackingQuery:
        api_response = rpc_request(
            method=RPCMethods.LIST_CARRIERS.value, config=config, params=tracking_data.to_dict()
        )

        return TrackPackageResult(api_response, config)
    elif type(tracking_data) is dict:
        api_response = rpc_request(
            method=RPCMethods.LIST_CARRIERS.value, config=config, params=tracking_data
        )

        return TrackPackageResult(api_response, config)
    else:
        raise ShipEngineError("Could not track package with the arguments provided.")
