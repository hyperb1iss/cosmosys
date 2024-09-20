from dataclasses import dataclass, field
from typing import ClassVar, Dict

from colorama import Fore, Style
from mashumaro import DataClassDictMixin

from cosmosys.config import ColorScheme, CosmosysConfig


@dataclass
class ColorManager(DataClassDictMixin):
    config: CosmosysConfig
    current_scheme: ColorScheme = field(init=False)
    COLOR_SCHEMES: Dict[str, ColorScheme] = field(init=False)

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

    def __post_init__(self):
        self.COLOR_SCHEMES = self.get_default_schemes()
        self.COLOR_SCHEMES.update(self.config.custom_color_schemes)
        self.current_scheme = self.get_scheme(self.config.color_scheme)

    def get_scheme(self, scheme_name: str) -> ColorScheme:
        return self.COLOR_SCHEMES.get(scheme_name, self.DEFAULT_SCHEME)

    def set_scheme(self, scheme_name: str):
        self.current_scheme = self.get_scheme(scheme_name)

    def colorize(self, text: str, color: str) -> str:
        return f"{getattr(self.current_scheme, color)}{text}{Style.RESET_ALL}"

    def primary(self, text: str) -> str:
        return self.colorize(text, "primary")

    def secondary(self, text: str) -> str:
        return self.colorize(text, "secondary")

    def success(self, text: str) -> str:
        return self.colorize(text, "success")

    def error(self, text: str) -> str:
        return self.colorize(text, "error")

    def warning(self, text: str) -> str:
        return self.colorize(text, "warning")

    def info(self, text: str) -> str:
        return self.colorize(text, "info")
