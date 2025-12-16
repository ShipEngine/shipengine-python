# Changelog

## [2.0.1](https://github.com/ShipEngine/shipengine-python/compare/v2.0.0...v2.0.1) (2025-12-16)


### Bug Fixes

* correct typo in CD workflow (dependancies -&gt; dependencies) ([a665002](https://github.com/ShipEngine/shipengine-python/commit/a665002dca3048d012c3974aab7cdc5d4ed57e0c))
* correct typo in CD workflow (dependancies -&gt; dependencies) ([088bee5](https://github.com/ShipEngine/shipengine-python/commit/088bee5bb6cfffa19d301aafd7d5d4aedced8b89))

## [2.0.0](https://github.com/ShipEngine/shipengine-python/compare/v1.0.2...v2.0.0) (2025-12-16)

### ⚠ BREAKING CHANGES

* **Python Support**: Dropped support for Python 3.7, 3.8, and 3.9. Minimum required Python version is now 3.10.

### Features

* Add support for Python 3.10, 3.11, 3.12, and 3.13 ([7559751](https://github.com/ShipEngine/shipengine-python/commit/75597510aa212c086077a03d7513835569be820a))
* Update CI/CD workflows to use current GitHub Actions versions
* Update package dependencies for Python 3.10+ compatibility

### Dependencies

* Update aiohttp from ^3.7.4 to ^3.9.0
* Update pytest from >=5.0 to ^7.0.0
* Update black from ^20.8b1 to ^22.0.0
* Update flake8 from ^3.8.4 to ^6.0.0

## [1.0.0](https://www.github.com/ShipEngine/shipengine-python/compare/v1.0.0...v1.0.0) (2021-08-11)

### Miscellaneous Chores

- release 1.0.0 ([f6f702f](https://www.github.com/ShipEngine/shipengine-python/commit/f6f702fa3427508cd78953b88d62e4bf3a0f3bf1))

## 1.0.0 (2021-08-11)

### Miscellaneous Chores

- release 1.0.0 ([c1407d2](https://www.github.com/ShipEngine/shipengine-python/commit/c1407d2de88182c75ba6dafff1ab30a3ed71efc6))

## 1.0.1

- increase default timeout from 5s to 60s

## 1.0.2

- Added error code FundingSourceMissingConfiguration
- Added error code FundingSourceError
