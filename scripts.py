import subprocess
import sys
from pathlib import Path


def ex_events():
    scriptpath = Path.cwd() / 'examples' / 'events' / '.'
    subprocess.run([sys.executable, str(scriptpath)])
