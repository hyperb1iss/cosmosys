from rich.console import Console

from cosmosys.ascii_art import ASCIIArtManager
from cosmosys.config import CosmosysConfig, load_config
from cosmosys.console import CosmosysConsole
from cosmosys.theme import ThemeManager


class CosmosysContext:
    """Context object for Cosmosys"""

    def __init__(self, console: Console, config_file: str, theme: str) -> None:
        self.config: CosmosysConfig = load_config(config_file)
        self.theme_manager: ThemeManager = ThemeManager(self.config)
        self.theme_manager.set_theme(theme)
        self.console: CosmosysConsole = CosmosysConsole(console, self.theme_manager)
        self.ascii_art_manager: ASCIIArtManager = ASCIIArtManager(self.theme_manager)
