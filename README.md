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
- [track_package](./docs/track_package_example.md "Track Package method documentation") - Track a package by `packageId` or by `carrierCode` and `trackingNumber`. This method returns
the all tracking events for a given shipment.

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

### Pre-Commit Hooks
We are using [Pre-Commit](https://pre-commit.com/) to enforce formatting, lint rules, and code analysis so that
this repo is always in good health.
 - If you choose not to globally install `pre-commit`, then you can skip installing via `pip` or `homebrew` directly.
   You can simply run either `pip install -r requirements.txt` or `poetry install`
To be able to push a PR to the repo after making changes locally, you will need to install `pre-commit` which
is a tool that runs linting, formatting, and code analysis on your changes.
```bash
pip install pre-commit  # Install via pip

OR

brew install pre-commit  # Install via homebrew
```
- After you have run either `pip install -r requirements.txt`, `poetry install`, or globally installed
  [Pre-Commit](https://pre-commit.com/) using the above commands you need to run the following command
  in the project directory locally. This allows the pre-commit hooks to run when you are looking to commit
  and push code to this repository.
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
