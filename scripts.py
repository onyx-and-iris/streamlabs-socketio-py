import subprocess
import sys
from pathlib import Path


def ex_events():
    scriptpath = Path.cwd() / 'examples' / 'events' / '.'
    subprocess.run([sys.executable, str(scriptpath)])


def ex_block_forever():
    scriptpath = Path.cwd() / 'examples' / 'block_forever' / '.'
    try:
        subprocess.run([sys.executable, str(scriptpath)])
    except KeyboardInterrupt:
        sys.exit(0)
