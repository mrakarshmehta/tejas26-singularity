"""
HiddenYatra — Pure-logic text and string utilities.
Zero external or database dependencies.
"""
import re


def _slugify(text):
    """Convert text to URL-friendly slug."""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text.strip('-')


def slugify(text):
    """Convert text to URL-safe slug."""
    return _slugify(text)


def _escape_like(value):
    """Escape special LIKE wildcards in user input to prevent LIKE injection."""
    return value.replace('\\', '\\\\').replace('%', '\\%').replace('_', '\\_')