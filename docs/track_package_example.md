Package Tracking
================
[ShipEngine](www.shipengine.com) allows you to get real-time tracking and delivery information for *any* package, regardless of
whether you created the package label through ShipEngine, so you know exactly where your package is and when it will arrive.

The `track_package` Method
--------------------------
The `track_package` method gives you information about a package and details about each of the tracking events that
have occurred, such as when the package is scanned by the carrier and when it is delivered.

If you created the package label through ShipEngine, we recommend that you use the package's `package_id` to track the
package so that we can provide as many details as possible about the package and its status.

If you only have the tracking number and shipping carrier, ShipEngine can still retrieve the information you need
to ensure your package's whereabouts.

## **Table of Contents**
  * [Input Parameters](#input-parameters)
    + [Track by package_id](#track-by--package-id-)
    + [Track by tracking_number and carrier_code](#track-by--tracking-number--and--carrier-code-)
      - [Carrier Codes](#carrier-codes)
  * [Output](#output)
- [Example](#example)
  * [Example Output (JSON object)](#example-output--json-object-)
- [Errors](#errors)

Input Parameters
----------------
The `track_package` method can accept either the `package_id` that was generated when you created the package label using
ShipEngine *OR* it can accept a `tracking_number` and `carrier_code`.

### Track by `package_id`
* `package_id` *required* <br>
A *string* containing a valid ShipEngine package ID.

### Track by `tracking_number` and `carrier_code`
* `tracking_number` *required* <br>
A *string* containing the tracking number provided by the carrier.

* `carrier_code` *required* <br>
A string containing the ShipEngine carrier code for the carrier that provided the tracking number.


#### Carrier Codes

| Carrier Name  | `carrier_code` |
|--------------|--------------|
|Access Worldwide | `access_worldwide`|
Amazon Buy Shipping | `amazon_buy_shipping`|
Amazon Shipping UK | `amazon_shipping_uk`|
APC | `apc`|
Asendia | `asendia`|
Australia Post | `australia_post`|
Canada Post | `canada_post`|
DHL Ecommerce | `dhl_ecommerce`|
DHL Express | `dhl_express`|
DHL Express Australia | `dhl_express_australia`|
DHL Express Canada | `dhl_express_canada`|
DHL Express UK | `dhl_express_uk`|
DPD | `dpd`|
Endicia | `endicia`|
FedEx | `fedex`|
FedEx UK | `fedex_uk`|
First Mile | `first_mile`|
Globegistics | `globgistics`|
Imex | `imex`|
Newgistics | `newgistics`|
OnTrac | `on_trac`|
Purolator Canada | `purolator_canada`|
Royal Mail | `royal_mail`|
RR Donnelley | `rr_donnelley`|
Seko | `seko`|
Sendle | `sendle`|
Stamps.com | `stamps_com`|
|UPS | `ups`|
|USPS | `usps`|


Output
------
The `track_package` method returns a tracking result object containing the properties listed below.
You can import the [track_packageResult]()
type into your project to take advantage of your IDE's code completion functionality.

* `shipment`
  An *object* representing the shipment details associated with this package.
    <br> <br>
    *  `shipment_id` <br>
    A *string* containing the ShipEngine ID for the shipment associated with this package.
       <br> <br>
       This property
       will be *undefined* if you are tracking by `tracking_number` and `carrier_code`.
       <br>
    *  `carrier_id` <br>
    A *string* containing the ShipEngine ID for the shipping carrier who is delivering this package.
    <br>
    This property
       will be *undefined* if you are tracking by `tracking_number` and `carrier_code`.
       <br>
       <br>
    *  `carrier_account`
    An *object* containing information about the carrier who is delivering this package.
   <br>
   This property will be *undefined* if you are tracking by `tracking_number` and `carrier_code`.
       <br>
       * `id`  <br>
       A *string* containing the ShipEngine ID for this carrier.
       <br> <br>
       *  `carrier`
       An *object* identifying the carrier.
       <br> <br>
          * `name`
           A *string* containing the name of the carrier (i.e. FedEx).<br> <br>
          * `code`
         A *string* containing the ShipEngine `carrier_code` associated with this carrier.
        <br> <br>
       * `account_number`
      A *string* containing your account number with the carrier.
        <br> <br>
       * `name`
    A *string* containing the nickname you gave to this account when you connected the carrier to your ShipEngine account.
    <br> <br>
  * `estimated_delivery_date` <br>
    An *object* representing the estimated delivery date and time.
      <br> <br>
      * `value` <br>
      The [ISOString](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString) value of this date.
  * `actual_delivery_date` <br>
    An *object* representing the actual delivery date and time.
    <br>
    <br>
    This property will be *undefined* if the package is still
    in transit.
    <br> <br>
    * `value` <br>
      The [ISOString](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString) value of this date.
* `package` <br>
An *object* containing information about the physical package.
  <br> <br>
  * `package_id` <br>
  A *string* containing the ShipEngine ID for this package.
    <br><br>
    This property will be *undefined* if you
    are tracking by `tracking_number` and `carrier_code`.
    <br> <br>
  * `tracking_number` <br>
  A *string* containing the carrier's tracking number for this package.
    <br> <br>
  `tracking_url` <br>
  A *string* containing a URL you can use to get the latest tracking information directly from the carrier.
    <br> <br>
 * `weight` <br>
  An *object* representing the weight of the package.
  <br>
  This property will be *undefined* if you
  are tracking by `tracking_number` and `carrier_code`.
   <br><br>
    * `value`
    A *number* containing the value of the weight in the specified `unit`.
    <br><br>
    * `unit`
    A *string* containing the unit of measure for the specified `value`.
      Possible values include the following:
      * `lb` - pound
      * `oz` - ounce
      * `gram`- gram
      * `kg` - kilogram
  <br><br>
  * `dimensions`
  An *object* representing the dimensions of this package.
  <br><br>
  This property will be *undefined* if you
  are tracking by `tracking_number` and `carrier_code`.
  <br><br>
    * `length`
    A *number* containing the length of this package.
    <br><br>
    * `width`
    A *number* containing the width of this package.
    <br><br>
    * `height`
    A *number* containing the height of this package.
    <br>
    * `unit`
    A *string* containing the unit of measure for the dimensions .
    Possible values include the following:
      * `in` - inch
      * `cm` - centimeter
    <br><br>
* `events[]` <br>
An *array of objects* representing the individual tracking events that have occurred for this package.
<br><br>
  * `date_time`
  An *object* representing the date and time that this event occurred.
    <br><br>
    * `value` <br>
    The [ISOString](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString) value of this date.
    <br>
  * `carrier_date_time`
  An *object* representing the date and time the carrier recorded this event.
    <br><br>
    * `value` <br>
      The [ISOString](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Date/toISOString) value of this date.
      <br>
  * `status`
  A *string* containing ShipEngine's status for this event (i.e. Delivered).
  <br><br>
  * `description`
  A *string* containing ShipEngine's description of this event. May be `undefined`.
  <br><br>
  * `carrier_status_code`
  A *string* containing the carrier's status for this event. (i.e. IN TRANSIT). May be `undefined`.
  <br><br>
  * `carrier_detail_code`
  A *string* containing the carrier's detail code for this event.
  <br><br>
  * `signer`
  A *string* containing the name of the person who signed for this package, if any. May be `undefined`.
  <br><br>
  * `location`
  An *object* representing the location where this event occurred. May be `undefined`.
  <br><br>
    * `cityLocality`
    A *string* containing the city or locality where this event occurred. May be `undefined`.
    <br><br>
    * `stateProvince`
    A *string* containing the state or province where this event occurred. May be `undefined`.
    <br><br>
    * `postal_code`
    A *string* containing the postal code where this event occurred. May be `undefined`.
    <br><br>
    * `countryCode`
   A *string* containing the [ISO 3166](https://en.wikipedia.org/wiki/List_of_ISO_3166_country_codes) country code
     <br><br>

    * `latitude`
     A *number* containing the latitude for the coordinates.
     <br><br>

    * `longitude` A *string* containing the longitude for the coordinates. May be `undefined`.
     <br><br>
 <br><br>
 * `errors[]`
 An *array* containing tracking error events. May be empty.


Example
=======
```python
import os

from shipengine_sdk import ShipEngine
from shipengine_sdk.models import TrackingQuery

api_key = os.getenv("SHIPENGINE_API_KEY")

shipengine = ShipEngine(
    {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
)

tracking_query = TrackingQuery(carrier_code="fedex", tracking_number="abc123")

tracking_data = shipengine.track_package(tracking_data=tracking_query)
print(
    tracking_data.to_json()
)  # OR print(tracking_data.to_dict()) to get a python dictionary.
```

Example Output (JSON object)
----------------------------
```json5
{
  "events": [
    {
      "date_time": {
        "iso_string": "2021-06-12T15:00:00.000Z"
      },
      "carrier_date_time": {
        "iso_string": "2021-06-12T21:00:00"
      },
      "status": "accepted",
      "description": "Picked up from shipper's warehouse",
      "carrier_status_code": "PU7W",
      "signer": null,
      "location": null
    },
    {
      "date_time": {
        "iso_string": "2021-06-13T14:00:00.000Z"
      },
      "carrier_date_time": {
        "iso_string": "2021-06-13T20:00:00"
      },
      "status": "in_transit",
      "description": "En-route to distribution center hub",
      "carrier_status_code": "ER00P",
      "signer": null,
      "location": null
    },
    {
      "date_time": {
        "iso_string": "2021-06-13T21:00:00.000Z"
      },
      "carrier_date_time": {
        "iso_string": "2021-06-14T03:00:00"
      },
      "status": "in_transit",
      "description": "Arrived at distribution center",
      "carrier_status_code": "DD00914",
      "signer": null,
      "location": {
        "city_locality": "Columbus",
        "state_province": "OH",
        "postal_code": "48223",
        "country_code": "US",
        "latitude": 39.948298,
        "longitude": -83.047395
      }
    },
    {
      "date_time": {
        "iso_string": "2021-06-14T18:00:00.000Z"
      },
      "carrier_date_time": {
        "iso_string": "2021-06-15T00:00:00"
      },
      "status": "in_transit",
      "description": "On vehicle for delivery",
      "carrier_status_code": "OFD-22",
      "signer": null,
      "location": null
    },
    {
      "date_time": {
        "iso_string": "2021-06-15T01:00:00.000Z"
      },
      "carrier_date_time": {
        "iso_string": "2021-06-15T07:00:00"
      },
      "status": "attempted_delivery",
      "description": "First delivery attempt. Signer not available.",
      "carrier_status_code": "EX026",
      "signer": null,
      "location": {
        "city_locality": "Pittsburgh",
        "state_province": "PA",
        "postal_code": "15218",
        "country_code": "US"
      }
    }
  ],
  "shipment": {
    "shipment_id": "shp_pPTdaK8cpFYroU2",
    "account_id": "car_kfUjTZSEAQ8gHeT",
    "carrier_account": {
      "carrier": {
        "name": "FedEx",
        "code": "fedex"
      },
      "name": "FedEx",
      "account_id": "car_kfUjTZSEAQ8gHeT",
      "account_number": "41E-4928-29314AAX"
    },
    "carrier": {
      "name": "FedEx",
      "code": "fedex"
    },
    "estimated_delivery_date": {
      "iso_string": "2021-06-16T21:00:00.000Z"
    },
    "actual_delivery_date": {
      "iso_string": "2021-06-15T01:00:00.000Z"
    }
  },
  "package": {
    "package_id": "pkg_Attempted",
    "weight": {
      "value": 84,
      "unit": "kilogram"
    },
    "dimensions": {
      "length": 36,
      "width": 36,
      "height": 26,
      "unit": "inch"
    },
    "tracking_number": "AN6LwpPTdaK8cpFYroU29tZU9udmFs",
    "tracking_url": "https://www.fedex.com/track/AN6LwpPTdaK8cpFYroU29tZU9udmFs"
  }
}
```

Errors
======
The `track_package` method may throw a [`ShipEngineError`]()
if there are issues with the input data, a network error, or a server error from the backend API.
