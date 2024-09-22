"""Console helpers for Cosmosys."""

from typing import Optional, List, Any

from rich.console import Console
from rich.table import Table
from wcwidth import wcswidth

from cosmosys.theme import ThemeManager


class CosmosysConsole:
    """Wrapper class for Rich console with theme-aware printing methods."""

    def __init__(self, console: Console, theme_manager: ThemeManager) -> None:
        self.console = console
        self.theme_manager = theme_manager

    def print(self, text: str, style: Optional[str] = None) -> None:
        """Print text with optional style."""
        if style:
            styled_text = getattr(self.theme_manager, style)(text)
            self.console.print(styled_text)
        else:
            self.console.print(text)

    def info(self, text: str) -> None:
        """Print info message."""
        self.print(text, "info")

    def success(self, text: str) -> None:
        """Print success message."""
        self.print(text, "success")

    def warning(self, text: str) -> None:
        """Print warning message."""
        self.print(text, "warning")

    def error(self, text: str) -> None:
        """Print error message."""
        self.print(text, "error")

    def primary(self, text: str) -> None:
        """Print text in primary color."""
        self.print(text, "primary")

    def secondary(self, text: str) -> None:
        """Print text in secondary color."""
        self.print(text, "secondary")

    def rainbow(self, text: str) -> None:
        """Print text with rainbow effect."""
        self.console.print(self.theme_manager.rainbow(text))

    def gradient(self, text: str, start_color: str, end_color: str) -> None:
        """Print text with gradient effect."""
        self.console.print(self.theme_manager.gradient(text, start_color, end_color))

    def print_table(self, headers: List[str], rows: List[List[Any]]) -> None:
        """Print a table with proper alignment for wide characters."""
        table = Table()
        for header in headers:
            table.add_column(header)

        for row in rows:
            formatted_row = [
                self._pad_string(str(cell), max(wcswidth(str(cell)) for cell in row))
                for cell in row
            ]
            table.add_row(*formatted_row)

        self.console.print(table)

    @staticmethod
    def _pad_string(text: str, width: int) -> str:
        """Pad a string to a specific width, accounting for wide characters."""
        current_width = wcswidth(text)
        if current_width < width:
            return text + " " * (width - current_width)
        return text
