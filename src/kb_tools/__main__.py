"""
Main entry point for running kb_tools via `python -m kb_tools`.
"""

import sys
from kb_tools.cli import main

if __name__ == "__main__":
    sys.exit(main())
