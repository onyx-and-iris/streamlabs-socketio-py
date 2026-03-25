## About

This example demonstrates the following:

-   How to register callback functions for different kinds of events.
-   How to view the logs emitted by the streamlabsio library.
-   How to use the raw data returned by the callback functions.
-   How to use {Client}.wait() to block the main thread indefinitely.

## Configure

The script expects the Streamlabs token to be loaded into the environment with key `STREAMLABS_TOKEN`.

If you're running the script with `poetry poe block-forever` then poe is configured to load a `.env` file in the root of the repository.

## Use

Run the script and trigger any of the events with `Test Widgets` in the Streamlabs GUI.
