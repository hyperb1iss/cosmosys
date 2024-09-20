from typing import Dict, NamedTuple

from colorama import Back, Fore, Style


class ColorScheme(NamedTuple):
    primary: str
    secondary: str
    success: str
    error: str
    warning: str
    info: str


DEFAULT_SCHEME = ColorScheme(
    primary=Fore.CYAN,
    secondary=Fore.MAGENTA,
    success=Fore.GREEN,
    error=Fore.RED,
    warning=Fore.YELLOW,
    info=Fore.BLUE,
)

COLOR_SCHEMES: Dict[str, ColorScheme] = {
    "default": DEFAULT_SCHEME,
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


class ColorManager:
    def __init__(self, scheme_name: str = "default"):
        self.set_scheme(scheme_name)

    def set_scheme(self, scheme_name: str):
        self.scheme = COLOR_SCHEMES.get(scheme_name, DEFAULT_SCHEME)

    def colorize(self, text: str, color: str) -> str:
        return f"{getattr(self.scheme, color)}{text}{Style.RESET_ALL}"

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
