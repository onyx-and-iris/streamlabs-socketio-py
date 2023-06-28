# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

-   [x]

## [1.0.0] - 2023-06-28

The only potential breaking change, a new error class raised if the initial connection fails.


### Added

-   tomllib/tomli now lazy loaded in _token_from_toml(). Allows possibility to run package without tomli.
-   module level logger
-   debug example
-   raw kwarg for receiving the raw json data.
-   `Path.home() / ".config" / "streamlabsio" / "config.toml"` added to config.toml filepaths.

### Changed

-   Python minimum required version changed to 3.8
-   new error class
    -   `SteamlabsSIOConnectionError` raised on a connection error
