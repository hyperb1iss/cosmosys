import random
from typing import List, Optional

from cosmosys.color_schemes import ColorManager


class ASCIIArt:
    def __init__(self, art: str, color_manager: ColorManager):
        self.art = art.strip()
        self.color_manager = color_manager

    def render(self, color: Optional[str] = None) -> str:
        if color:
            return getattr(self.color_manager, color)(self.art)
        return self.art

    @staticmethod
    def generate_stars(width: int, height: int, density: float = 0.1) -> str:
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
    " ▄▄·       .▄▄ · • ▌ ▄ ·.       .▄▄ ·  ▄· ▄▌.▄▄ ·  ",
    "▐█ ▌▪▪     ▐█ ▀. ·██ ▐███▪▪     ▐█ ▀. ▐█▪██▌▐█ ▀.  ",
    "█ ▄▄ ▄█▀▄ ▄▀▀▀█▄▐█ ▌▐▌▐█· ▄█▀▄ ▄▀▀▀█▄▐█▌▐█▪▄▀▀▀█▄  ",
    "▐███▌▐█▌.▐▌▐█▄▪▐███ ██▌▐█▌▐█▌.▐▌▐█▄▪▐█ ▐█▀·.▐█▄▪▐█ ",
    "·▀▀▀  ▀█▄▀▪ ▀▀▀▀ ▀▀  █▪▀▀▀ ▀█▄▀▪ ▀▀▀▀   ▀ •  ▀▀▀▀  ",
    "                                                   ",
    "         🌌 Cosmic Release Management 🌠         ",
    "      .:*~*:._.:*~*:._.:*~*:._.:*~*:._.:*~*:.      "
]

class ASCIIArtManager:
    def __init__(self, color_manager: ColorManager):
        self.color_manager = color_manager
        self.logo = ASCIIArt(DEFAULT_LOGO, self.color_manager)
        self.arts: List[ASCIIArt] = []

    def add_art(self, art: str):
        self.arts.append(ASCIIArt(art, self.color_manager))

    def render_logo(self, color: Optional[str] = None) -> str:
        return self.logo.render(color)

    def render_random_art(self, color: Optional[str] = None) -> str:
        if self.arts:
            return random.choice(self.arts).render(color)
        return ""

    def render_starfield(
        self, width: int = 80, height: int = 5, density: float = 0.1, color: Optional[str] = None
    ) -> str:
        stars = ASCIIArt.generate_stars(width, height, density)
        return ASCIIArt(stars, self.color_manager).render(color)
