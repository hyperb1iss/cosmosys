"""Theme management for Cosmosys."""

import os
from dataclasses import dataclass, field
from typing import Dict, List

import toml
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.text import Text
from mashumaro import DataClassDictMixin

from cosmosys.config import ThemeConfig, CosmosysConfig


@dataclass
class ThemeManager(DataClassDictMixin):
    """Manages themes and provides color rendering functionality."""

    config: CosmosysConfig
    current_theme: ThemeConfig = field(init=False)
    themes: Dict[str, ThemeConfig] = field(init=False)
    emojis: Dict[str, str] = field(init=False)

    def __post_init__(self) -> None:
        """Initialize themes and set the current theme."""
        self.themes = self.load_themes()
        self.current_theme = self.get_theme(self.config.theme)
        self.emojis = self.themes[self.config.theme].emojis

    @staticmethod
    def load_themes() -> Dict[str, ThemeConfig]:
        """Load themes from the themes.toml file."""
        themes_file = os.path.join(os.path.dirname(__file__), "themes.toml")
        with open(themes_file, "r") as f:
            themes_data = toml.load(f)

        return {name: ThemeConfig(**theme) for name, theme in themes_data.items()}

    def get_theme(self, theme_name: str) -> ThemeConfig:
        """Get a theme by name."""
        return self.themes.get(theme_name, self.themes["default"])

    def set_theme(self, theme_name: str) -> None:
        """Set the current theme."""
        self.current_theme = self.get_theme(theme_name)
        self.emojis = self.current_theme.emojis

    def get_color(self, color_name: str) -> str:
        """Get a color value from the current theme."""
        return getattr(self.current_theme, color_name)

    def colorize(self, text: str, color: str) -> Text:
        """Colorize text using the current theme."""
        return Text(text, style=Style(color=self.get_color(color)))

    def primary(self, text: str) -> Text:
        """Apply primary color to text."""
        return self.colorize(text, "primary")

    def secondary(self, text: str) -> Text:
        """Apply secondary color to text."""
        return self.colorize(text, "secondary")

    def success(self, text: str) -> Text:
        """Apply success color to text."""
        return self.colorize(f"{self.emojis['success']} {text}", "success")

    def error(self, text: str) -> Text:
        """Apply error color to text."""
        return self.colorize(f"{self.emojis['error']} {text}", "error")

    def warning(self, text: str) -> Text:
        """Apply warning color to text."""
        return self.colorize(f"{self.emojis['warning']} {text}", "warning")

    def info(self, text: str) -> Text:
        """Apply info color to text."""
        return self.colorize(f"{self.emojis['info']} {text}", "info")

    def rainbow(self, text: str) -> Text:
        """Apply rainbow colors to text."""
        rainbow_colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#8B00FF"]
        rainbow_text = Text()
        for i, char in enumerate(text):
            color = rainbow_colors[i % len(rainbow_colors)]
            rainbow_text.append(char, style=Style(color=color))
        return rainbow_text

    def gradient(self, text: str, start_color_name: str, end_color_name: str) -> Text:
        """Apply a gradient effect to text."""
        start_color_hex = self.get_color(start_color_name)
        end_color_hex = self.get_color(end_color_name)
        start_rgb = self._hex_to_rgb(start_color_hex)
        end_rgb = self._hex_to_rgb(end_color_hex)
        gradient_text = Text()
        length = max(len(text) - 1, 1)
        for i, char in enumerate(text):
            ratio = i / length
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * ratio)
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * ratio)
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * ratio)
            color_code = f"#{r:02X}{g:02X}{b:02X}"
            gradient_text.append(char, style=Style(color=color_code))
        return gradient_text

    @staticmethod
    def _hex_to_rgb(hex_color: str) -> List[int]:
        """Convert hex color code to RGB values."""
        hex_color = hex_color.lstrip("#")
        return [int(hex_color[i : i + 2], 16) for i in (0, 2, 4)]

    def apply_style(self, text: str, style_name: str) -> Text:
        """Apply a predefined style to the text."""
        style_methods = {
            "bold": lambda t: Text(t, style=Style(bold=True)),
            "italic": lambda t: Text(t, style=Style(italic=True)),
            "underline": lambda t: Text(t, style=Style(underline=True)),
        }
        return style_methods.get(style_name, lambda t: Text(t))(text)


def preview_theme(theme_manager: ThemeManager, console: Console) -> None:
    """Preview the essential elements of a theme."""
    # Header
    console.print(Panel(
        Text("Theme Preview", style=f"bold {theme_manager.get_color('primary')}"),
        border_style=theme_manager.get_color("secondary"),
    ))

    # Example text for each level
    console.print(theme_manager.primary("Primary text"))
    console.print(theme_manager.secondary("Secondary text"))
    console.print(theme_manager.success("Success message"))
    console.print(theme_manager.error("Error message"))
    console.print(theme_manager.warning("Warning message"))
    console.print(theme_manager.info("Info message"))

    # Special text effects
    console.print(theme_manager.rainbow("Rainbow text example"))
    console.print(theme_manager.gradient("Gradient text example", "primary", "secondary"))

    # Footer
    console.print(Panel(
        Text("End of Preview", style=f"bold {theme_manager.get_color('secondary')}"),
        border_style=theme_manager.get_color("primary"),
    ))