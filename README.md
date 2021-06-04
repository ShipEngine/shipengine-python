[![ShipEngine](https://shipengine.github.io/img/shipengine-logo-wide.png)](https://shipengine.com)

ShipEngine Python SDK
=====================

![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ShipEngine/shipengine-python/Python%20package?label=shipengine-python&logo=github&logoColor=white)
[![Coverage Status](https://coveralls.io/repos/github/ShipEngine/shipengine-python/badge.svg?branch=main)](https://coveralls.io/github/ShipEngine/shipengine-python?branch=main)
![GitHub](https://img.shields.io/github/license/shipengine/shipengine-python?color=blue)
![OS Compatibility](https://shipengine.github.io/img/badges/os-badges.svg)

> ATTN: This project is under development and not ready for consumer use.

- The official Python module for ShipEngine API.

Quick Start
===========

Install `shipengine` via pip (not yet published):
```bash
pip install shipengine
```

- The only configuration requirement is providing an [API Key](https://www.shipengine.com/docs/auth/#api-keys "ShipEngine Authentication Docs").

> The following assumes that you have already set the `SHIPENGINE_API_KEY` environment variable with your API Key using `os.environ["SHIPENGINE_API_KEY"] = "<YOUR_API_KEY_HERE>"`.

Methods
-------
- [validate_address](./docs/address_validation_example.md "Validate Address method documentation") - Indicates whether the provided address is valid. If the
  address is valid, the method returns a normalized version of the address based on the standards of the country in
  which the address resides.
- [normalize_address](./docs/normalize_address_example.md "Normalize Address method documentation") - Returns a normalized, or standardized, version of the
  address. If the address cannot be normalized, an error is returned.

Class Objects
-------------
- [ShipEngine]() - A configurable entry point to the ShipEngine API SDK, this class provides convenience methods
  for various ShipEngine API Services.

Instantiate ShipEngine Class
----------------------------
```python
import os

from shipengine_sdk import ShipEngine

api_key = os.getenv("SHIPENGINE_API_KEY")

shipengine = ShipEngine(api_key)
```
- You can also pass in a `dictionary` containing configuration options instead of just passing in a string that is your `API Key`.
```python
import os

from shipengine_sdk import ShipEngine

api_key = os.getenv("SHIPENGINE_API_KEY")

shipengine = ShipEngine(
    {"api_key": api_key, "page_size": 75, "retries": 3, "timeout": 10}
)
```

Local Development
=================
> You will need to install `Python3.7` if you do not have it locally, before working on this project.

This project uses [Poetry]() to manage project dependencies, build steps, and publishing to [PYPI]().

You can use the following `curl` command to download **Poetry** from your terminal is you are
on `osx / linux / bashonwindows`:

```bash
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
```

- Once you have **Poetry** installed you need to install the projects dependencies with this command:

```bash
poetry install
```

- After you have installed **Poetry**, you need to start the python environment managed by Poetry by
  running `poetry shell` in your terminal.

```bash
poetry shell
 ```

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
