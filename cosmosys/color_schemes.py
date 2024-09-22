"""Color scheme management for Cosmosys."""

import os
from dataclasses import dataclass, field
from typing import Dict, List

import toml
from rich.style import Style
from rich.text import Text
from mashumaro import DataClassDictMixin

from cosmosys.config import ColorScheme, CosmosysConfig


@dataclass
class ColorManager(DataClassDictMixin):
    """Manages color schemes and provides color rendering functionality."""

    config: CosmosysConfig
    current_scheme: ColorScheme = field(init=False)
    color_schemes: Dict[str, ColorScheme] = field(init=False)
    emojis: Dict[str, str] = field(init=False)

    def __post_init__(self) -> None:
        """Initialize color schemes and set the current scheme."""
        self.color_schemes = self.load_themes()
        self.current_scheme = self.get_scheme(self.config.color_scheme)
        self.emojis = self.color_schemes[self.config.color_scheme].emojis

    @staticmethod
    def load_themes() -> Dict[str, ColorScheme]:
        """Load themes from the themes.toml file."""
        themes_file = os.path.join(os.path.dirname(__file__), "themes.toml")
        with open(themes_file, "r") as f:
            themes_data = toml.load(f)

        return {name: ColorScheme(**theme) for name, theme in themes_data.items()}

    def get_scheme(self, scheme_name: str) -> ColorScheme:
        """Get a color scheme by name."""
        return self.color_schemes.get(scheme_name, self.color_schemes["default"])

    def set_scheme(self, scheme_name: str) -> None:
        """Set the current color scheme."""
        self.current_scheme = self.get_scheme(scheme_name)
        self.emojis = self.current_scheme.emojis

    def get_color(self, color_name: str) -> str:
        """Get a color value from the current scheme."""
        return getattr(self.current_scheme, color_name)

    def colorize(self, text: str, color: str) -> Text:
        """Colorize text using the current color scheme."""
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
