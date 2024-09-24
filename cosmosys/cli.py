# pylint: disable=redefined-outer-name
"""Command-line interface for Cosmosys."""

from enum import Enum
from typing import List, Optional

import typer
from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.text import Text

from cosmosys.ascii_art import ASCIIArtManager
from cosmosys.config import CosmosysConfig, load_config
from cosmosys.context import CosmosysContext
from cosmosys.console import CosmosysConsole
from cosmosys.plugin_manager import PluginManager
from cosmosys.release import ReleaseManager
from cosmosys.theme import ThemeManager, preview_theme
from cosmosys.version_manager import VersionManager

app = typer.Typer()
console = Console()
plugin_manager: PluginManager = None


@app.callback()
def callback(
    ctx: typer.Context,
    config: str = typer.Option("cosmosys.toml", help="Path to the configuration file"),
    theme: str = typer.Option("default", help="Theme to use"),
) -> None:
    """Cosmosys: A flexible and customizable release management tool."""
    ctx.obj = CosmosysContext(console, config, theme)
    plugin_manager = PluginManager(ctx.obj)
    plugin_manager.load_plugins()


class VersionPart(str, Enum):
    MAJOR = "major"
    MINOR = "minor"
    PATCH = "patch"


DEFAULT_PART = typer.Option(None, "--bump", help="Part of the version to bump")


@app.command()
def release(
    ctx: typer.Context,
    dry_run: bool = typer.Option(False, help="Perform a dry run without making any changes"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Enable interactive mode"),
    new_version: Optional[str] = typer.Option(
        None, "--new-version", help="Set the new version number explicitly"
    ),
    version_part: Optional[VersionPart] = DEFAULT_PART,
) -> None:
    """Run the release process."""
    sf_ctx: CosmosysContext = ctx.obj
    config = sf_ctx.config
    console = sf_ctx.console
    ascii_art_manager = sf_ctx.ascii_art_manager

    display_header(ascii_art_manager, console)
    console.gradient("Starting release process...", "primary", "secondary")

    # Initialize VersionManager
    version_manager = VersionManager(config)

    # Print out the current version
    console.info(f"Current version: {version_manager.current_version}")

    # Set versioning parameters
    if new_version:
        config.new_version = new_version
    if version_part:
        config.version_part = version_part.value

    # Determine and display the new version
    new_version = version_manager.determine_new_version()
    console.info(f"New version will be: {new_version}")

    if config.is_auto_detected:
        console.info("Using auto-detected configuration.")

    if dry_run:
        console.warning("Dry run mode: No changes will be made")

    steps = config.get_steps()
    if verbose:
        console.info(f"Steps to execute: {', '.join(steps)}")

    release_manager = ReleaseManager(sf_ctx, verbose)

    if interactive:
        steps = prompt_for_steps(steps, console)

    # Confirm with the user before proceeding
    if not typer.confirm("Do you want to proceed with the release?"):
        console.info("Release process cancelled.")
        return

    success = release_manager.execute_steps(steps, dry_run)

    display_footer(ascii_art_manager, console, success)


def display_header(ascii_art_manager: ASCIIArtManager, console: CosmosysConsole) -> None:
    """Display the application header with logo."""
    logo = ascii_art_manager.render_logo(color="primary")
    logo_panel = Panel(
        logo,
        expand=False,
        border_style=console.theme_manager.get_color("secondary"),
        title=console.theme_manager.apply_style("Cosmosys", "bold"),
        title_align="center",
    )
    console.console.print(logo_panel)


def display_footer(
    ascii_art_manager: ASCIIArtManager, console: CosmosysConsole, success: bool
) -> None:
    """Display the application footer."""
    console.console.print(ascii_art_manager.render_starfield(color="secondary"))
    message = "Release process completed successfully" if success else "Release process failed"
    if success:
        console.rainbow(message)
    else:
        console.error(message)


def prompt_for_steps(steps: List[str], console: CosmosysConsole) -> List[str]:
    """Prompt the user to confirm or modify the list of steps."""
    console.info("Interactive mode enabled.")
    confirmed_steps: List[str] = []
    for step in steps:
        if typer.confirm(f"Execute step '{step}'?", default=True):
            confirmed_steps.append(step)
    return confirmed_steps


@app.command()
def config(
    ctx: typer.Context,
    set_key: Optional[str] = typer.Option(None, "--set", help="Set a configuration value"),
    set_value: Optional[str] = typer.Option(None, "--value", help="Value to set"),
    get_key: Optional[str] = typer.Option(None, "--get", help="Get a configuration value"),
    init: bool = typer.Option(False, "--init", help="Initialize a new configuration file"),
) -> None:
    """Manage Cosmosys configuration."""
    sf_ctx: CosmosysContext = ctx.obj
    console = sf_ctx.console

    if init:
        config = CosmosysConfig.auto_detect_config()
        config.save()
        console.success("Initialized new configuration file: cosmosys.toml")
    else:
        config = load_config()

    if set_key and set_value:
        config.set(set_key, set_value)
        config.save()
        console.success(f"Set {set_key} to {set_value}")

    if get_key:
        value = config.get(get_key)
        console.info(f"{get_key}: {value}")

    if not any([init, set_key, get_key]):
        display_config(config, console)


def display_config(config: CosmosysConfig, console: CosmosysConsole) -> None:
    """Display the current configuration."""
    table = Table(
        title="Current Configuration",
        border_style=console.theme_manager.get_color("primary"),
    )
    table.add_column("Key", style=console.theme_manager.get_color("secondary"))
    table.add_column("Value", style=console.theme_manager.get_color("info"))

    for key, value in config.to_flat_dict().items():
        table.add_row(key, str(value))

    console.console.print(table)


@app.command()
def version() -> None:
    """Display the current version of Cosmosys."""
    version_str = "Cosmosys v0.1.0"  # TODO: Implement dynamic version retrieval
    console.print(Panel(version_str, expand=False, border_style="cyan"))


@app.command()
def theme(
    ctx: typer.Context,
    list_themes: bool = typer.Option(False, "--list", help="List available themes"),
    set_theme: Optional[str] = typer.Option(None, "--set", help="Set the theme"),
    preview_theme_name: Optional[str] = typer.Option(None, "--preview", help="Preview a theme"),
) -> None:
    """Manage Cosmosys themes."""
    sf_ctx: CosmosysContext = ctx.obj
    theme_manager = sf_ctx.theme_manager
    console = sf_ctx.console

    if list_themes:
        display_themes(theme_manager, console)

    if set_theme:
        if set_theme in theme_manager.themes:
            theme_manager.set_theme(set_theme)
            sf_ctx.config.theme = set_theme
            sf_ctx.config.save()
            console.success(f"Theme set to {set_theme}")
        else:
            console.error(f"Invalid theme name: {set_theme}")

    if preview_theme_name:
        if preview_theme_name in theme_manager.themes:
            theme_manager.set_theme(preview_theme_name)
            console.info(f"Previewing theme: {preview_theme_name}")
            preview_theme(theme_manager, console.console)
        else:
            console.error(f"Invalid theme name: {preview_theme_name}")


def display_themes(theme_manager: ThemeManager, console: CosmosysConsole) -> None:
    """Display the list of available themes with color swatches and emoji samples."""
    table = Table(
        title="✨ Cosmosys Theme Gallery ✨",
        show_header=True,
        header_style=theme_manager.get_color("primary"),
        show_lines=False,
        padding=(0, 1),
        expand=False,
        box=None,
    )
    table.add_column("Theme Name", style=theme_manager.get_color("secondary"), no_wrap=True)
    table.add_column("Description", style=theme_manager.get_color("info"))
    table.add_column("Color Palette", style=theme_manager.get_color("info"))
    table.add_column("Emoji Set", style=theme_manager.get_color("info"))

    sorted_themes = sorted(theme_manager.themes.items(), key=lambda x: x[0].lower())

    for theme_name, scheme in sorted_themes:
        # Create color swatches
        swatches = Text()
        for color_name in ["primary", "secondary", "success", "error", "warning", "info"]:
            color = getattr(scheme, color_name)
            swatches.append("██", style=Style(color=color))
            swatches.append(" ")

        # Create emoji sample
        sample = Text()
        for key in ["success", "error", "warning", "info"]:
            emoji = scheme.emojis[key]
            sample.append(f"{emoji} ", style=theme_manager.get_color(key))

        # Add a row for each theme
        table.add_row(
            theme_name,  # Use the actual theme name (key) instead of the friendly name
            Align(scheme.description, align="left", vertical="middle"),
            Align(swatches, align="center", vertical="middle"),
            Align(sample, align="center", vertical="middle"),
        )

        # Add a subtle separator between rows
        table.add_row("", "", Text("· · · · · · · · · ·", style="dim"), "")

    console.console.print(table)


@app.command()
def plugins(
    ctx: typer.Context,
    list_plugins: bool = typer.Option(False, "--list", help="List available plugins"),
    info_plugin: Optional[str] = typer.Option(None, "--info", help="Get info about a plugin"),
) -> None:
    """Manage Cosmosys plugins."""
    sf_ctx: CosmosysContext = ctx.obj
    console = sf_ctx.console

    if list_plugins:
        display_plugins(plugin_manager, console)

    if info_plugin:
        plugin_info = plugin_manager.get_plugin_info(info_plugin)
        if plugin_info:
            console.console.print(
                Panel(
                    plugin_info,
                    title=console.theme_manager.secondary(f"Plugin: {info_plugin}"),
                    border_style=console.theme_manager.get_color("primary"),
                )
            )
        else:
            console.error(f"Plugin not found: {info_plugin}")


def display_plugins(plugin_manager: PluginManager, console: CosmosysConsole) -> None:
    """Display the list of available plugins."""
    plugins = plugin_manager.get_available_plugins()
    table = Table(
        title="Available Plugins",
        border_style=console.theme_manager.get_color("primary"),
    )
    table.add_column("Plugin Name", style=console.theme_manager.get_color("secondary"))
    table.add_column("Description", style=console.theme_manager.get_color("info"))

    for plugin_name, plugin_desc in plugins.items():
        table.add_row(plugin_name, plugin_desc)

    console.console.print(table)


def main() -> None:
    """Entry point for the Cosmosys CLI."""
    app()


if __name__ == "__main__":
    main()
