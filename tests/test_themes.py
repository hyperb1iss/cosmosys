# pylint: disable=redefined-outer-name
"""Unit tests for the Cosmosys theme module."""

import pytest

from cosmosys.config import CosmosysConfig, ProjectConfig, ReleaseConfig, ThemeConfig
from cosmosys.theme import ThemeManager


@pytest.fixture
def default_config() -> CosmosysConfig:
    """Fixture for creating a default configuration."""
    return CosmosysConfig(
        project=ProjectConfig(
            name="TestProject", repo_name="test/repo", version="1.0.0", project_type="python"
        ),
        theme="default",
        git={
            "files_to_commit": ["file1.py"],
            "commit_message": "Release {version}",
        },
        release=ReleaseConfig(steps=["version_update"]),
    )


@pytest.fixture
def custom_config() -> CosmosysConfig:
    """Fixture for creating a configuration with a custom theme."""
    return CosmosysConfig(
        project=ProjectConfig(
            name="TestProject", repo_name="test/repo", version="1.0.0", project_type="python"
        ),
        theme="custom",
        custom_themes={
            "custom": ThemeConfig(
                name="Custom Theme",
                description="A custom theme for testing",
                primary="#0000FF",  # Blue
                secondary="#008000",  # Green
                success="#00FFFF",  # Cyan
                error="#FF0000",  # Red
                warning="#FFFF00",  # Yellow
                info="#FF00FF",  # Magenta
                emojis={"success": "✅", "error": "❌", "warning": "⚠️", "info": "ℹ️"},
            )
        },
        git={
            "files_to_commit": ["file1.py"],
            "commit_message": "Release {version}",
        },
        release=ReleaseConfig(steps=["version_update"]),
    )


def test_default_color_scheme(default_config: CosmosysConfig) -> None:
    """Test the default color scheme."""
    theme_manager = ThemeManager(default_config)
    assert theme_manager.current_theme == theme_manager.themes["default"]


def test_custom_color_scheme(custom_config: CosmosysConfig) -> None:
    """Test a custom color scheme."""
    theme_manager = ThemeManager(custom_config)
    assert theme_manager.current_theme == custom_config.custom_themes["custom"]


def test_colorize(default_config: CosmosysConfig) -> None:
    """Test the colorize method."""
    theme_manager = ThemeManager(default_config)
    colored_text = theme_manager.primary("Test")
    assert (
        ThemeManager._color_to_hex(colored_text.style.color)
        == theme_manager.get_color("primary").lower()
    )


def test_set_scheme(default_config: CosmosysConfig) -> None:
    """Test setting a different color scheme."""
    theme_manager = ThemeManager(default_config)
    theme_manager.set_theme("monokai")
    assert theme_manager.current_theme == theme_manager.themes["monokai"]


def test_color_methods(default_config: CosmosysConfig) -> None:
    """Test all color methods."""
    theme_manager = ThemeManager(default_config)
    assert (
        ThemeManager._color_to_hex(theme_manager.primary("Test").style.color)
        == theme_manager.get_color("primary").lower()
    )
    assert (
        ThemeManager._color_to_hex(theme_manager.secondary("Test").style.color)
        == theme_manager.get_color("secondary").lower()
    )
    assert (
        ThemeManager._color_to_hex(theme_manager.success("Test").style.color)
        == theme_manager.get_color("success").lower()
    )
    assert (
        ThemeManager._color_to_hex(theme_manager.error("Test").style.color)
        == theme_manager.get_color("error").lower()
    )
    assert (
        ThemeManager._color_to_hex(theme_manager.warning("Test").style.color)
        == theme_manager.get_color("warning").lower()
    )
    assert (
        ThemeManager._color_to_hex(theme_manager.info("Test").style.color)
        == theme_manager.get_color("info").lower()
    )
