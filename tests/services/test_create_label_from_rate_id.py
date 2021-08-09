"""Testing the create label from rate ID functionality in the ShipEngine SDK."""
import json
import unittest
import urllib.parse as urlparse

import responses

from shipengine.enums import BaseURL
from tests.util import stub_shipengine_instance


class TestCreateLabelFromRateID(unittest.TestCase):
    @responses.activate
    def test_create_label_from_rate_id_(self) -> None:
        """Test purchase label from rate_id."""
        responses.add(
            **{
                "method": responses.POST,
                "url": urlparse.urljoin(
                    BaseURL.SHIPENGINE_RPC_URL.value, "v1/labels/rates/se-799373193"
                ),
                "body": json.dumps(
                    {
                        "batch_id": "",
                        "carrier_code": "stamps_com",
                        "carrier_id": "se-656171",
                        "charge_event": "carrier_default",
                        "created_at": "2021-08-05T16:47:47.8768838Z",
                        "display_scheme": "label",
                        "form_download": None,
                        "insurance_claim": None,
                        "insurance_cost": {"amount": 0.0, "currency": "usd"},
                        "is_international": False,
                        "is_return_label": False,
                        "label_download": {
                            "href": "https://api.shipengine.com/v1/downloads/10/_EKGeA4yuEuLzLq81iOzew/label-75693596.pdf",  # noqa
                            "pdf": "https://api.shipengine.com/v1/downloads/10/_EKGeA4yuEuLzLq81iOzew/label-75693596.pdf",  # noqa
                            "png": "https://api.shipengine.com/v1/downloads/10/_EKGeA4yuEuLzLq81iOzew/label-75693596.png",  # noqa
                            "zpl": "https://api.shipengine.com/v1/downloads/10/_EKGeA4yuEuLzLq81iOzew/label-75693596.zpl",  # noqa
                        },
                        "label_format": "pdf",
                        "label_id": "se-799373193",
                        "label_image_id": None,
                        "label_layout": "4x6",
                        "package_code": "package",
                        "packages": [
                            {
                                "dimensions": {
                                    "height": 0.0,
                                    "length": 0.0,
                                    "unit": "inch",
                                    "width": 0.0,
                                },
                                "external_package_id": None,
                                "insured_value": {"amount": 0.0, "currency": "usd"},
                                "label_messages": {
                                    "reference1": None,
                                    "reference2": None,
                                    "reference3": None,
                                },
                                "package_code": "package",
                                "package_id": 80328023,
                                "sequence": 1,
                                "tracking_number": "9400111899560334651289",
                                "weight": {"unit": "ounce", "value": 1.0},
                            }
                        ],
                        "rma_number": None,
                        "service_code": "usps_first_class_mail",
                        "ship_date": "2021-08-05T00:00:00Z",
                        "shipment_cost": {"amount": 3.35, "currency": "usd"},
                        "shipment_id": "se-144794216",
                        "status": "completed",
                        "trackable": True,
                        "tracking_number": "9400111899560334651289",
                        "tracking_status": "in_transit",
                        "voided": False,
                        "voided_at": None,
                    }
                ),
                "status": 200,
                "content_type": "application/json",
            }
        )

        shipengine = stub_shipengine_instance()
        params = {
            "validate_address": "no_validation",
            "label_layout": "4x6",
            "label_format": "pdf",
            "label_download_type": "url",
            "display_scheme": "label",
        }
        result = shipengine.create_label_from_rate_id(rate_id="se-799373193", params=params)
        self.assertEqual(result["label_id"], "se-799373193")
