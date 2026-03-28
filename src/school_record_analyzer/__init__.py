"""School record analyzer package."""

from .parser import parse_record_file
from .rules import RuleEngine
from .renderer import render_report

__all__ = ["parse_record_file", "RuleEngine", "render_report"]
