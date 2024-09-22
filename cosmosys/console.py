"""Console helpers for Cosmosys."""

from rich.console import Console
from cosmosys.theme import ThemeManager

class CosmosysConsole:
    """Wrapper class for Rich console with theme-aware printing methods."""

    def __init__(self, console: Console, theme_manager: ThemeManager):
        self.console = console
        self.theme_manager = theme_manager

    def print(self, text: str, style: str = None):
        """Print text with optional style."""
        if style:
            self.console.print(getattr(self.theme_manager, style)(text))
        else:
            self.console.print(text)

    def info(self, text: str):
        """Print info message."""
        self.print(text, "info")

    def success(self, text: str):
        """Print success message."""
        self.print(text, "success")

    def warning(self, text: str):
        """Print warning message."""
        self.print(text, "warning")

    def error(self, text: str):
        """Print error message."""
        self.print(text, "error")

    def primary(self, text: str):
        """Print text in primary color."""
        self.print(text, "primary")

    def secondary(self, text: str):
        """Print text in secondary color."""
        self.print(text, "secondary")

    def rainbow(self, text: str):
        """Print text with rainbow effect."""
        self.console.print(self.theme_manager.rainbow(text))

    def gradient(self, text: str, start_color: str, end_color: str):
        """Print text with gradient effect."""
        self.console.print(self.theme_manager.gradient(text, start_color, end_color))