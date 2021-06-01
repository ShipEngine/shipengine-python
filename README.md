[![ShipEngine](https://shipengine.github.io/img/shipengine-logo-wide.png)](https://shipengine.com)

ShipEngine Python SDK
=====================
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/ShipEngine/shipengine-python/Python%20package?label=shipengine-python&logo=github&logoColor=white)
[![Coverage Status](https://coveralls.io/repos/github/ShipEngine/shipengine-python/badge.svg?branch=main)](https://coveralls.io/github/ShipEngine/shipengine-python?branch=main)
![GitHub](https://img.shields.io/github/license/shipengine/shipengine-python?color=blue)
![OS Compatibility](https://shipengine.github.io/img/badges/os-badges.svg)
> ATTN: This project is under development and not ready for consumer use.

- A Python library for ShipEngine API.

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
    - Next you will have to start the poetry environment:
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
