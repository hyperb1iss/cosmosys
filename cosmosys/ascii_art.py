"""ASCII art generation and management for Cosmosys."""

import random
from typing import List, Optional

from cosmosys.color_schemes import ColorManager


class ASCIIArt:
    """Represents a single piece of ASCII art with color management."""

    def __init__(self, art: str, color_manager: ColorManager):
        """
        Initialize an ASCIIArt object.

        Args:
            art (str): The ASCII art string.
            color_manager (ColorManager): The color manager for rendering.
        """
        self.art = art.strip()
        self.color_manager = color_manager

    def render(self, color: Optional[str] = None) -> str:
        """
        Render the ASCII art with optional coloring.

        Args:
            color (Optional[str]): The color to render the art in.

        Returns:
            str: The rendered ASCII art.
        """
        if color:
            return str(getattr(self.color_manager, color)(self.art))
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
                    stars += random.choice([".", "*", "+", "·"])
                else:
                    stars += " "
            stars += "\n"
        return stars.strip()


DEFAULT_LOGO = [
    "  ▄▄·       .▄▄ · • ▌ ▄ ·.       .▄▄ ·  ▄· ▄▌.▄▄ · ",
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

    def __init__(self, color_manager: ColorManager):
        """
        Initialize an ASCIIArtManager object.

        Args:
            color_manager (ColorManager): The color manager for rendering.
        """
        self.color_manager = color_manager
        self.logo = ASCIIArt("\n".join(DEFAULT_LOGO), self.color_manager)
        self.arts: List[ASCIIArt] = []

    def add_art(self, art: str) -> None:
        """
        Add a new ASCII art piece to the manager.

        Args:
            art (str): The ASCII art string to add.
        """
        self.arts.append(ASCIIArt(art, self.color_manager))

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
        return ASCIIArt(stars, self.color_manager).render(color)
