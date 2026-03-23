## About

To view the logs emitted by the streamlabsio library simply add the following to your code:

```python
from loguru import logger

logger.enable('streamlabsio')
```

## Configure

The script expects the Streamlabs token to be loaded into the environment with key `STREAMLABS_TOKEN`.

If you're running the script with `poetry poe` then poe is configured to load a `.env` file in the root of the repository.

## Use

Run the script and trigger any of the events with `Test Widgets` in the Streamlabs GUI.
