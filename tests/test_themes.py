# pylint: disable=redefined-outer-name
"""Unit tests for the Cosmosys color scheme module."""

import pytest
from colorama import Fore, Style

from cosmosys.theme import ThemeManager
from cosmosys.config import ThemeConfig, CosmosysConfig, ProjectConfig


@pytest.fixture
def default_config() -> CosmosysConfig:
    """Fixture for creating a default configuration."""
    return CosmosysConfig(
        project=ProjectConfig(
            name="TestProject", repo_name="test/repo", version="1.0.0", project_type="python"
        ),
        color_scheme="default",
    )


@pytest.fixture
def custom_config() -> CosmosysConfig:
    """Fixture for creating a configuration with a custom color scheme."""
    return CosmosysConfig(
        project=ProjectConfig(
            name="TestProject", repo_name="test/repo", version="1.0.0", project_type="python"
        ),
        color_scheme="custom",
        custom_color_schemes={
            "custom": ThemeConfig(
                primary="blue",
                secondary="green",
                success="cyan",
                error="red",
                warning="yellow",
                info="magenta",
            )
        },
    )


def test_default_color_scheme(default_config: CosmosysConfig) -> None:
    """Test the default color scheme."""
    theme_manager = ThemeManager(default_config)
    assert theme_manager.current_scheme == ThemeManager.DEFAULT_SCHEME


def test_custom_color_scheme(custom_config: CosmosysConfig) -> None:
    """Test a custom color scheme."""
    theme_manager = ThemeManager(custom_config)
    assert theme_manager.current_scheme == custom_config.custom_color_schemes["custom"]


def test_colorize(default_config: CosmosysConfig) -> None:
    """Test the colorize method."""
    theme_manager = ThemeManager(default_config)
    colored_text = theme_manager.primary("Test")
    assert colored_text == f"{Fore.CYAN}Test{Style.RESET_ALL}"


def test_set_scheme(default_config: CosmosysConfig) -> None:
    """Test setting a different color scheme."""
    theme_manager = ThemeManager(default_config)
    theme_manager.set_scheme("monochrome")
    assert theme_manager.current_scheme == theme_manager.color_schemes["monochrome"]


def test_color_methods(default_config: CosmosysConfig) -> None:
    """Test all color methods."""
    theme_manager = ThemeManager(default_config)
    assert theme_manager.primary("Test") == f"{Fore.CYAN}Test{Style.RESET_ALL}"
    assert theme_manager.secondary("Test") == f"{Fore.MAGENTA}Test{Style.RESET_ALL}"
    assert theme_manager.success("Test") == f"{Fore.GREEN}Test{Style.RESET_ALL}"
    assert theme_manager.error("Test") == f"{Fore.RED}Test{Style.RESET_ALL}"
    assert theme_manager.warning("Test") == f"{Fore.YELLOW}Test{Style.RESET_ALL}"
    assert theme_manager.info("Test") == f"{Fore.BLUE}Test{Style.RESET_ALL}"
