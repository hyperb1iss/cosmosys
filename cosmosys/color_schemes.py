"""Color scheme management for Cosmosys."""

from dataclasses import dataclass, field
from typing import ClassVar, Dict, List

from colorama import Fore

from rich.text import Style, Text
from mashumaro import DataClassDictMixin

from cosmosys.config import ColorScheme, CosmosysConfig


@dataclass
class ColorManager(DataClassDictMixin):
    """Manages color schemes and provides color rendering functionality."""

    config: CosmosysConfig
    current_scheme: ColorScheme = field(init=False)
    color_schemes: Dict[str, ColorScheme] = field(init=False)

    DEFAULT_SCHEME: ClassVar[ColorScheme] = ColorScheme(
        primary="#00FFFF",  # Cyan
        secondary="#FF00FF",  # Magenta
        success="#00FF00",  # Green
        error="#FF0000",  # Red
        warning="#FFFF00",  # Yellow
        info="#0000FF",  # Blue
    )

    @classmethod
    def get_default_schemes(cls) -> Dict[str, ColorScheme]:
        """
        Get the default color schemes.

        Returns:
            Dict[str, ColorScheme]: A dictionary of default color schemes.
        """
        return {
            "default": cls.DEFAULT_SCHEME,
            "neon": ColorScheme(
                primary="#00FFFF",  # Cyan
                secondary="#FF00FF",  # Magenta
                success="#00FF00",  # Green
                error="#FF0000",  # Red
                warning="#FFFF00",  # Yellow
                info="#0000FF",  # Blue
            ),
            "pastel": ColorScheme(
                primary="#AFE1FF",  # Light Blue
                secondary="#FFD1DC",  # Light Pink
                success="#98FB98",  # Pale Green
                error="#FFA07A",  # Light Salmon
                warning="#FFFACD",  # Lemon Chiffon
                info="#E6E6FA",  # Lavender
            ),
            "ocean": ColorScheme(
                primary="#1E90FF",  # Dodger Blue
                secondary="#20B2AA",  # Light Sea Green
                success="#32CD32",  # Lime Green
                error="#FF4500",  # Orange Red
                warning="#FFD700",  # Gold
                info="#87CEEB",  # Sky Blue
            ),
            "sunset": ColorScheme(
                primary="#FF6347",  # Tomato
                secondary="#FF8C00",  # Dark Orange
                success="#32CD32",  # Lime Green
                error="#DC143C",  # Crimson
                warning="#FFD700",  # Gold
                info="#1E90FF",  # Dodger Blue
            ),
        }

    def __post_init__(self) -> None:
        """Initialize color schemes and set the current scheme."""
        self.color_schemes = self.get_default_schemes()
        self.color_schemes.update(self.config.custom_color_schemes)
        self.current_scheme = self.get_scheme(self.config.color_scheme)

    def get_scheme(self, scheme_name: str) -> ColorScheme:
        """
        Get a color scheme by name.

        Args:
            scheme_name (str): The name of the color scheme.

        Returns:
            ColorScheme: The requested color scheme or the default scheme if not found.
        """
        return self.color_schemes.get(scheme_name, self.DEFAULT_SCHEME)

    def set_scheme(self, scheme_name: str) -> None:
        """
        Set the current color scheme.

        Args:
            scheme_name (str): The name of the color scheme to set.
        """
        self.current_scheme = self.get_scheme(scheme_name)

    def get_color(self, color_name: str) -> str:
        """
        Get a color value from the current scheme.

        Args:
            color_name (str): The name of the color.

        Returns:
            str: The color value.
        """
        return getattr(self.current_scheme, color_name)

    def colorize(self, text: str, color: str) -> Text:
        """
        Colorize text using the current color scheme.

        Args:
            text (str): The text to colorize.
            color (str): The color to apply.

        Returns:
            Text: The colorized text.
        """
        return Text(text, style=Style(color=self.get_color(color)))

    def primary(self, text: str) -> Text:
        """Apply primary color to text."""
        return self.colorize(text, "primary")

    def secondary(self, text: str) -> Text:
        """Apply secondary color to text."""
        return self.colorize(text, "secondary")

    def success(self, text: str) -> Text:
        """Apply success color to text."""
        return self.colorize(text, "success")

    def error(self, text: str) -> Text:
        """Apply error color to text."""
        return self.colorize(text, "error")

    def warning(self, text: str) -> Text:
        """Apply warning color to text."""
        return self.colorize(text, "warning")

    def info(self, text: str) -> Text:
        """Apply info color to text."""
        return self.colorize(text, "info")

    def rainbow(self, text: str) -> Text:
        """Apply rainbow colors to text."""
        rainbow_colors = ["#FF0000", "#FF7F00", "#FFFF00", "#00FF00", "#0000FF", "#8B00FF"]
        rainbow_text = Text()
        for i, char in enumerate(text):
            color = rainbow_colors[i % len(rainbow_colors)]
            rainbow_text.append(char, style=Style(color=color))
        return rainbow_text

    def gradient(self, text: str, start_color: str, end_color: str) -> str:
        """Apply a gradient effect to text."""
        start_rgb = self._fore_to_rgb(start_color)
        end_rgb = self._fore_to_rgb(end_color)
        gradient_text = ""
        for i, char in enumerate(text):
            r = int(start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i / len(text))
            g = int(start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i / len(text))
            b = int(start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i / len(text))
            gradient_text += f"\033[38;2;{r};{g};{b}m{char}"
        return gradient_text

    @staticmethod
    def _fore_to_rgb(fore_color: str) -> List[int]:
        """Convert Fore color to RGB values."""
        color_map = {
            Fore.BLACK: [0, 0, 0],
            Fore.RED: [255, 0, 0],
            Fore.GREEN: [0, 255, 0],
            Fore.YELLOW: [255, 255, 0],
            Fore.BLUE: [0, 0, 255],
            Fore.MAGENTA: [255, 0, 255],
            Fore.CYAN: [0, 255, 255],
            Fore.WHITE: [255, 255, 255],
        }
        return color_map.get(fore_color, [255, 255, 255])
