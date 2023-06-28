import subprocess
from pathlib import Path


def ex_debug():
    path = Path.cwd() / "examples" / "debug" / "."
    subprocess.run(["py", str(path)])
