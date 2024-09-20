# pylint: disable=redefined-outer-name
"""Color scheme management for Cosmosys."""

from dataclasses import dataclass, field
from typing import ClassVar, Dict

from colorama import Fore, Style
from mashumaro import DataClassDictMixin

from cosmosys.config import ColorScheme, CosmosysConfig


@dataclass
class ColorManager(DataClassDictMixin):
    """Manages color schemes and provides color rendering functionality."""

    config: CosmosysConfig
    current_scheme: ColorScheme = field(init=False)
    color_schemes: Dict[str, ColorScheme] = field(init=False)

    DEFAULT_SCHEME: ClassVar[ColorScheme] = ColorScheme(
        primary=Fore.CYAN,
        secondary=Fore.MAGENTA,
        success=Fore.GREEN,
        error=Fore.RED,
        warning=Fore.YELLOW,
        info=Fore.BLUE,
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
            "monochrome": ColorScheme(
                primary=Fore.WHITE,
                secondary=Fore.LIGHTBLACK_EX,
                success=Fore.WHITE,
                error=Fore.WHITE,
                warning=Fore.WHITE,
                info=Fore.WHITE,
            ),
            "neon": ColorScheme(
                primary=Fore.CYAN,
                secondary=Fore.MAGENTA,
                success=Fore.GREEN,
                error=Fore.RED,
                warning=Fore.YELLOW,
                info=Fore.BLUE,
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

    def colorize(self, text: str, color: str) -> str:
        """
        Colorize text using the current color scheme.

        Args:
            text (str): The text to colorize.
            color (str): The color to apply.

        Returns:
            str: The colorized text.
        """
        return f"{getattr(self.current_scheme, color)}{text}{Style.RESET_ALL}"

    def primary(self, text: str) -> str:
        """Apply primary color to text."""
        return self.colorize(text, "primary")

    def secondary(self, text: str) -> str:
        """Apply secondary color to text."""
        return self.colorize(text, "secondary")

    def success(self, text: str) -> str:
        """Apply success color to text."""
        return self.colorize(text, "success")

    def error(self, text: str) -> str:
        """Apply error color to text."""
        return self.colorize(text, "error")

    def warning(self, text: str) -> str:
        """Apply warning color to text."""
        return self.colorize(text, "warning")

    def info(self, text: str) -> str:
        """Apply info color to text."""
        return self.colorize(text, "info")
