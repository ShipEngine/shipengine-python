[![ShipEngine](https://shipengine.github.io/img/shipengine-logo-wide.png)](https://shipengine.com)

ShipEngine Python SDK
=====================

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/ShipEngine/shipengine-python/CI.yml?branch=main&label=shipengine-python&logo=github&logoColor=white)
[![Coverage Status](https://coveralls.io/repos/github/ShipEngine/shipengine-python/badge.svg?branch=main)](https://coveralls.io/github/ShipEngine/shipengine-python?branch=main)
![GitHub](https://img.shields.io/github/license/shipengine/shipengine-python?color=blue)
![OS Compatibility](https://shipengine.github.io/img/badges/os-badges.svg)

- The official Python module for ShipEngine API.

Quick Start
===========

Install `shipengine` via `pip`:
```bash
pip install shipengine
```

- The only configuration requirement is providing an [API Key](https://www.shipengine.com/docs/auth/#api-keys "ShipEngine Authentication Docs").

> The following assumes that you have already set the `SHIPENGINE_API_KEY` environment variable with your API Key using `os.environ["SHIPENGINE_API_KEY"] = "<YOUR_API_KEY_HERE>"`.

Instantiate ShipEngine Class
----------------------------

```python
import os

from shipengine import ShipEngine

api_key = os.getenv("SHIPENGINE_API_KEY")

shipengine = ShipEngine(api_key)
```
- You can also pass in a `dictionary` containing configuration options instead of just passing in a string that is your `API Key`.

```python
import os

from shipengine import ShipEngine

api_key = os.getenv("SHIPENGINE_API_KEY")

shipengine = ShipEngine(
    {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
)
```

Methods
-------
- [addresses_validate](./docs/addresses_validate_example.md) - Indicates whether the provided address is valid. If the
  address is valid, the method returns a normalized version of the address based on the standards of the country in
  which the address resides.
- [create_label_from_rate_id](./docs/create_label_from_rate_id_example.md) - Purchase a label by `rate_id`. When using the `get_rates_from_shipment` method, you can use one of the returned `rate_id` values with this method to purchase a label against a given rate.
- [create_label_from_shipment](./docs/create_label_from_shipment.md) - Purchase a label created from shipment details.
- [get_rates_from_shipment](./docs/get_rates_from_shipment_example.md) - Fetch rates from shipment details to shop the best shipping rate for your package.
- [list_carriers](./docs/list_carriers_example.md) - Lists the carrier accounts connected to your ShipEngine account.
- [track_package_by_label_id](./docs/track_package_by_label_id_example.md) - Track a package by `label_id`, the preferred way to track shipments if you create shipping labels using ShipEngine. This method returns
the all tracking events for a given shipment.
- [track_package_by_carrier_code_and_tracking_number](./docs/track_package_by_carrier_code_and_tracking_number_example.md) - Track a package by `carrier_code` and `tracking_number`. This method returns
the all tracking events for a given shipment.
- [void_label_by_label_id](./docs/void_label_by_label_id_example.md) - Void a shipping label you created using ShipEngine by its `label_id`. This method returns an object that indicates the status of the void label request.
- [list_labels_by_tracking_number] (./docs/list_labels_by_tracking_number.md) - List the labels associated with the inputted tracking number.

Class Objects
-------------
- [ShipEngine](./) - A configurable entry point to the ShipEngine API SDK, this class provides convenience methods
  for various ShipEngine API Services.

Contributing
============

Local Development
-----------------
> You will need to install `Python3.7` if you do not have it locally, before working on this project.

This project uses [Poetry]() to manage project dependencies, build steps, and publishing to [PYPI]().

You can use the following `curl` command to download **Poetry** from your terminal is you are
on `osx / linux / bashonwindows`:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

- Once you have **Poetry** installed you need to install the projects dependencies with this command from the project root:

```bash
bin/setup
```
- This script will install all dependencies specified in `pyproject.toml` via `Poetry` and install the `pre-commit` hooks
this project uses.

## Adding dependencies to the project
If your changes require you to install a python package/module using `poetry add <some package>` or
`poetry add <some package> -D` for a dev dependency. You will also need to run the following command to
regenerate a `requirements.txt` file that includes the newly added dependencies:
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes --dev
```

## Pre-Commit Hooks
We are using [Pre-Commit](https://pre-commit.com/) to enforce formatting, lint rules, and code analysis so that
this repo is always in good health.
- `Pre-Commit` is installed and initialized when you run `bin/setup` from the project root as outlined above.

- If you choose not to use `Poetry` and prefer `pip` you can simply run `pip install -r requirements.txt`
To be able to commit & push a PR to the repo after making changes locally, you will need to install `pre-commit` which
is a tool that runs tests, linting, formatting, and code analysis on your changes.
```bash
pre-commit install
```
> Note: The checks run in pre-commit hooks are the same checks run in CI in our GitHub Actions.

Testing
-------
You can run the tests in the `tests/` directory using [Pytest]() in the **Poetry** environment like this:

```bash
poetry run pytest
```

OR via `Tox`:

```bash
poetry run tox
```

Linting
-------
You can run the `linting environment` in **Tox** using this command:

```bash
poetry tox -e lint
```
