import sys

print("Trying import base.py settings...", file=sys.stderr)
from .base import *  # noqa: F401, F403

try:
    from .local import *  # noqa: F401, F403

    # if local.py is imported, it will override settings in base.py
    print("Trying import local.py settings...", file=sys.stderr)

except ImportError:
    pass
