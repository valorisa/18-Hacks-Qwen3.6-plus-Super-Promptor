# src/py_mdlint/__main__.py
"""Support: python -m py_mdlint"""

import sys
from .cli import main

if __name__ == "__main__":
    sys.exit(main())
