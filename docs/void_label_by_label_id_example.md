Void Label by Label ID Documentation
====================================
[ShipEngine](www.shipengine.com) allows you to attempt to void a previously purchased label.

Please see [our docs](https://www.shipengine.com/docs/labels/voiding/) to learn more about voiding a label.


Input Parameters
----------------
The `void_label_by_label_id` method accepts a string that contains the label ID that is being voided.


Output
------
The `void_label_by_label_id` method returns an object that indicates the status of the void label request.


Example
=======
```python
import os

from shipengine import ShipEngine
from shipengine.errors import ShipEngineError


def void_label_by_label_id_demo():
    api_key = os.getenv("SHIPENGINE_API_KEY")

    shipengine = ShipEngine(
        {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
    )
    try:
        result = shipengine.void_label_by_label_id(label_id="se-75449505")
        print("::SUCCESS::")
        print(result)
    except ShipEngineError as err:
        print("::ERROR::")
        print(err.to_json())


void_label_by_label_id_demo()
```

Example Output
==============
```python
{
    "approved": True,
    "message": "Request for refund submitted.  This label has been voided.",
}
```

Exceptions
==========

- This method will only throw an exception that is an instance/extension of
  ([ShipEngineError](../shipengine/errors/__init__.py)) if there is a problem if a problem occurs, such as a network
  error or an error response from the API.
