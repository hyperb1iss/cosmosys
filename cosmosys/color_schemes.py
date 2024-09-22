"""Color scheme management for Cosmosys."""

from dataclasses import dataclass, field
from typing import ClassVar, Dict, List

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
                primary="#39FF14",  # Neon Green
                secondary="#FF6EC7",  # Neon Pink
                success="#0FFF50",  # Spring Green
                error="#FF073A",  # Neon Red
                warning="#FFD300",  # Neon Yellow
                info="#00FFFF",  # Neon Cyan
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
            "forest": ColorScheme(
                primary="#228B22",  # Forest Green
                secondary="#8B4513",  # Saddle Brown
                success="#6B8E23",  # Olive Drab
                error="#A52A2A",  # Brown
                warning="#DAA520",  # Goldenrod
                info="#2E8B57",  # Sea Green
            ),
            "midnight": ColorScheme(
                primary="#191970",  # Midnight Blue
                secondary="#000000",  # Black
                success="#2F4F4F",  # Dark Slate Gray
                error="#8B0000",  # Dark Red
                warning="#808000",  # Olive
                info="#00008B",  # Dark Blue
            ),
            "rose": ColorScheme(
                primary="#FF007F",  # Rose
                secondary="#C71585",  # Medium Violet Red
                success="#FF69B4",  # Hot Pink
                error="#DB7093",  # Pale Violet Red
                warning="#FFC0CB",  # Pink
                info="#FF1493",  # Deep Pink
            ),
            "sunrise": ColorScheme(
                primary="#FF4500",  # Orange Red
                secondary="#FFA500",  # Orange
                success="#FFD700",  # Gold
                error="#FF69B4",  # Hot Pink
                warning="#FFFF00",  # Yellow
                info="#FFE4B5",  # Moccasin
            ),
            "grayscale": ColorScheme(
                primary="#333333",  # Dark Gray
                secondary="#666666",  # Gray
                success="#999999",  # Light Gray
                error="#CCCCCC",  # Very Light Gray
                warning="#777777",  # Medium Gray
                info="#BBBBBB",  # Silver
            ),
            # Added a new "galaxy" theme
            "galaxy": ColorScheme(
                primary="#8A2BE2",  # Blue Violet
                secondary="#4B0082",  # Indigo
                success="#7FFF00",  # Chartreuse
                error="#FF4500",  # Orange Red
                warning="#FFD700",  # Gold
                info="#00CED1",  # Dark Turquoise
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
        hex_color = hex_color.lstrip('#')
        return [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]

    def apply_style(self, text: str, style_name: str) -> Text:
        """
        Apply a predefined style to the text.

        Args:
            text (str): The text to style.
            style_name (str): The style to apply.

        Returns:
            Text: The styled text.
        """
        style_methods = {
            "bold": lambda t: Text(t, style=Style(bold=True)),
            "italic": lambda t: Text(t, style=Style(italic=True)),
            "underline": lambda t: Text(t, style=Style(underline=True)),
        }
        return style_methods.get(style_name, lambda t: Text(t))(text)
