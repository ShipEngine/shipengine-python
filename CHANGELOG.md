# Changelog

## [2.0.5](https://github.com/ShipEngine/shipengine-python/compare/v2.0.4...v2.0.5) (2025-12-16)


### Bug Fixes

* correct typo in linting section of README ([222b293](https://github.com/ShipEngine/shipengine-python/commit/222b2930706476254b2229b72db63f9ec3cffb0a))

## [2.0.4](https://github.com/ShipEngine/shipengine-python/compare/v2.0.3...v2.0.4) (2025-12-16)


### Bug Fixes

* correct typos in README documentation ([8b1951f](https://github.com/ShipEngine/shipengine-python/commit/8b1951f60b2b30640f83eaa938fd9e835d05e7d9))

## [2.0.3](https://github.com/ShipEngine/shipengine-python/compare/v2.0.2...v2.0.3) (2025-12-16)


### Bug Fixes

* update GitHub workflow badge and resolve CD PyYAML compatibility issue ([5b634ca](https://github.com/ShipEngine/shipengine-python/commit/5b634ca5862ddaadd3e527d91b2b55314a158e98))
* update GitHub workflow badge URL and fix PyYAML compatibility ([65cc2a3](https://github.com/ShipEngine/shipengine-python/commit/65cc2a3a3e0e3ee6d298c417bed2aba01c3b9d5e))

## [2.0.2](https://github.com/ShipEngine/shipengine-python/compare/v2.0.1...v2.0.2) (2025-12-16)


### Bug Fixes

* regenerate poetry.lock and update to modern Poetry config ([6ee6fbe](https://github.com/ShipEngine/shipengine-python/commit/6ee6fbef131b49db9fe998939547b5a01a6281aa))
* regenerate poetry.lock and update to modern Poetry config ([80b2531](https://github.com/ShipEngine/shipengine-python/commit/80b2531ced22aea74334caa2050fb572b8d43e9e))

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
