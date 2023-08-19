import subprocess
import sys
from pathlib import Path


def ex_debug():
    scriptpath = Path.cwd() / "examples" / "debug" / "."
    subprocess.run([sys.executable, str(scriptpath)])
