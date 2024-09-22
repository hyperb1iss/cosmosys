"""ASCII art generation and management for Cosmosys."""

import random
from typing import List, Optional

from cosmosys.theme import ThemeManager


class ASCIIArt:
    """Represents a single piece of ASCII art with theme management."""

    def __init__(self, art: str, theme_manager: ThemeManager):
        """
        Initialize an ASCIIArt object.

        Args:
            art (str): The ASCII art string.
            theme_manager (ThemeManager): The theme manager for rendering.
        """
        self.art = art.strip()
        self.theme_manager = theme_manager

    def render(self, color: Optional[str] = None) -> str:
        """
        Render the ASCII art with optional coloring.

        Args:
            color (Optional[str]): The color to render the art in.

        Returns:
            str: The rendered ASCII art.
        """
        if color:
            return str(self.theme_manager.colorize(self.art, color))
        return self.art

    @staticmethod
    def generate_stars(width: int, height: int, density: float = 0.1) -> str:
        """
        Generate a starfield ASCII art.

        Args:
            width (int): The width of the starfield.
            height (int): The height of the starfield.
            density (float): The density of stars (0.0 to 1.0).

        Returns:
            str: The generated starfield ASCII art.
        """
        stars = ""
        for _ in range(height):
            for _ in range(width):
                if random.random() < density:
                    stars += random.choice([".", "*", "+", "·", "✦", "✧", "☆", "★"])
                else:
                    stars += " "
            stars += "\n"
        return stars.strip()


DEFAULT_LOGO = [
    " ▄▄·       .▄▄ · • ▌ ▄ ·.       .▄▄ ·  ▄· ▄▌.▄▄ ·  ",
    "▐█ ▌▪▪     ▐█ ▀. ·██ ▐███▪▪     ▐█ ▀. ▐█▪██▌▐█ ▀.  ",
    "█ ▄▄ ▄█▀▄ ▄▀▀▀█▄▐█ ▌▐▌▐█· ▄█▀▄ ▄▀▀▀█▄▐█▌▐█▪▄▀▀▀█▄  ",
    "▐███▌▐█▌.▐▌▐█▄▪▐███ ██▌▐█▌▐█▌.▐▌▐█▄▪▐█ ▐█▀·.▐█▄▪▐█ ",
    "·▀▀▀  ▀█▄▀▪ ▀▀▀▀ ▀▀  █▪▀▀▀ ▀█▄▀▪ ▀▀▀▀   ▀ •  ▀▀▀▀  ",
    "                                                   ",
    "         🌌 Cosmic Release Management 🌠         ",
    "     .:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.      ",
]


class ASCIIArtManager:
    """Manages multiple ASCII art pieces and provides rendering options."""

    def __init__(self, theme_manager: ThemeManager):
        """
        Initialize an ASCIIArtManager object.

        Args:
            theme_manager (ThemeManager): The theme manager for rendering.
        """
        self.theme_manager = theme_manager
        self.logo = ASCIIArt("\n".join(DEFAULT_LOGO), self.theme_manager)
        self.arts: List[ASCIIArt] = []

    def add_art(self, art: str) -> None:
        """
        Add a new ASCII art piece to the manager.

        Args:
            art (str): The ASCII art string to add.
        """
        self.arts.append(ASCIIArt(art, self.theme_manager))

    def render_logo(self, color: Optional[str] = None) -> str:
        """
        Render the default logo.

        Args:
            color (Optional[str]): The color to render the logo in.

        Returns:
            str: The rendered logo.
        """
        return self.logo.render(color)

    def render_random_art(self, color: Optional[str] = None) -> str:
        """
        Render a random ASCII art piece from the collection.

        Args:
            color (Optional[str]): The color to render the art in.

        Returns:
            str: The rendered ASCII art, or an empty string if no art is available.
        """
        if self.arts:
            return random.choice(self.arts).render(color)
        return ""

    def render_starfield(
        self, width: int = 80, height: int = 5, density: float = 0.1, color: Optional[str] = None
    ) -> str:
        """
        Render a starfield ASCII art.

        Args:
            width (int): The width of the starfield.
            height (int): The height of the starfield.
            density (float): The density of stars (0.0 to 1.0).
            color (Optional[str]): The color to render the starfield in.

        Returns:
            str: The rendered starfield ASCII art.
        """
        stars = ASCIIArt.generate_stars(width, height, density)
        return ASCIIArt(stars, self.theme_manager).render(color)
