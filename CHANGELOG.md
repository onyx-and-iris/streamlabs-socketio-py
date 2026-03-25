# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]

The following changes are proposals for v2.

### Added

-   wait() method on the Client class, it's a convenience method that exposes {socketio.Client}.sleep() and {socketio.Client}.wait().

### Fixed

-   The returned dataclasses now work properly with dataclass methods such as `asdict`. See the events example.

### Removed

-   Built-in support for loading the token from a config.toml. This is a job better left to the library consumer.
-   {Client}.raw property, you can still configure the Client to return raw data via the raw kwarg.
-   Support for python versions 3.8 and 3.9.

### Changed

-   loguru is now used for logging. See the examples for a demonstration.


## [1.1.2] - 2024-11-06

### Fixed

-   [PR #8][pr-8] fixes bug receiving `raid` events.

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


[pr-8]: https://github.com/onyx-and-iris/streamlabs-socketio-py/pull/8
