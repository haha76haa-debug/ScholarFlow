"""
kb_tools: Python Automation Maintenance Tools for Academic Knowledge Base.
"""

__version__ = "0.1.0"

from kb_tools import canvas_gen, cli, ingest, link_checker, linter, registry, synthesizer

__all__ = [
    "__version__",
    "canvas_gen",
    "cli",
    "ingest",
    "link_checker",
    "linter",
    "registry",
    "synthesizer",
]
