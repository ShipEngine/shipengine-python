"""Testing the create label from shipment functionality."""
import json
import unittest
import urllib.parse as urlparse

import responses

from shipengine.enums import BaseURL, Endpoints
from tests.util import stub_shipengine_instance


class TestCreateLabelFromShipment(unittest.TestCase):
    def test_create_label_from_shipment(self) -> None:
        """Test purchase label from shipment."""
        responses.add(
            **{
                "method": responses.POST,
                "url": urlparse.urljoin(
                    BaseURL.SHIPENGINE_RPC_URL.value, Endpoints.GET_RATE_FROM_SHIPMENT.value
                ),
                "body": json.dumps(
                    {
                        "label_id": "se-75714944",
                        "status": "completed",
                        "shipment_id": "se-144835189",
                        "ship_date": "2021-08-05T00:00:00Z",
                        "created_at": "2021-08-05T18:01:46.0013168Z",
                        "shipment_cost": {"currency": "usd", "amount": 27.98},
                        "insurance_cost": {"currency": "usd", "amount": 0.0},
                        "tracking_number": "1Z63R0960311549776",
                        "is_return_label": False,
                        "rma_number": None,
                        "is_international": False,
                        "batch_id": "",
                        "carrier_id": "se-656172",
                        "service_code": "ups_ground",
                        "package_code": "package",
                        "voided": False,
                        "voided_at": None,
                        "label_format": "pdf",
                        "display_scheme": "label",
                        "label_layout": "4x6",
                        "trackable": True,
                        "label_image_id": None,
                        "carrier_code": "ups",
                        "tracking_status": "in_transit",
                        "label_download": {
                            "pdf": "https://api.shipengine.com/v1/downloads/10/nRpNbEgTzkaBB1HitZNfjQ/label-75714944.pdf",  # noqa
                            "png": "https://api.shipengine.com/v1/downloads/10/nRpNbEgTzkaBB1HitZNfjQ/label-75714944.png",  # noqa
                            "zpl": "https://api.shipengine.com/v1/downloads/10/nRpNbEgTzkaBB1HitZNfjQ/label-75714944.zpl",  # noqa
                            "href": "https://api.shipengine.com/v1/downloads/10/nRpNbEgTzkaBB1HitZNfjQ/label-75714944.pdf",  # noqa
                        },
                        "form_download": None,
                        "insurance_claim": None,
                        "packages": [
                            {
                                "package_id": 80350838,
                                "package_code": "package",
                                "weight": {"value": 20.0, "unit": "ounce"},
                                "dimensions": {
                                    "unit": "inch",
                                    "length": 24.0,
                                    "width": 12.0,
                                    "height": 6.0,
                                },
                                "insured_value": {"currency": "usd", "amount": 0.0},
                                "tracking_number": "1Z63R0960311549776",
                                "label_messages": {
                                    "reference1": None,
                                    "reference2": None,
                                    "reference3": None,
                                },
                                "external_package_id": None,
                                "sequence": 1,
                            }
                        ],
                        "charge_event": "carrier_default",
                    }
                ),
                "status": 200,
                "content_type": "application/json",
            }
        )

        shipengine = stub_shipengine_instance()
        result = shipengine.create_label_from_shipment(
            shipment={
                "shipment": {
                    "service_code": "ups_ground",
                    "ship_to": {
                        "name": "Jane Doe",
                        "address_line1": "525 S Winchester Blvd",
                        "city_locality": "San Jose",
                        "state_province": "CA",
                        "postal_code": "95128",
                        "country_code": "US",
                        "address_residential_indicator": "yes",
                    },
                    "ship_from": {
                        "name": "John Doe",
                        "company_name": "Example Corp",
                        "phone": "555-555-5555",
                        "address_line1": "4009 Marathon Blvd",
                        "city_locality": "Austin",
                        "state_province": "TX",
                        "postal_code": "78756",
                        "country_code": "US",
                        "address_residential_indicator": "no",
                    },
                    "packages": [
                        {
                            "weight": {"value": 20, "unit": "ounce"},
                            "dimensions": {
                                "height": 6,
                                "width": 12,
                                "length": 24,
                                "unit": "inch",
                            },
                        }
                    ],
                }
            }
        )
        self.assertEqual(result["status"], "completed")
