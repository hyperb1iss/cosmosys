"""Command-line interface for Cosmosys."""

from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from cosmosys.ascii_art import ASCIIArtManager
from cosmosys.theme import ThemeManager, preview_theme
from cosmosys.config import CosmosysConfig, load_config
from cosmosys.plugin_manager import PluginManager
from cosmosys.release import ReleaseManager
from cosmosys.console import CosmosysConsole

app = typer.Typer()
console = Console()


class CosmosysContext:
    """Context object for Cosmosys CLI commands."""

    def __init__(self, config_file: str, theme: str):
        self.config: CosmosysConfig = load_config(config_file)
        self.theme_manager: ThemeManager = ThemeManager(self.config)
        self.theme_manager.set_theme(theme)
        self.console: CosmosysConsole = CosmosysConsole(console, self.theme_manager)
        self.ascii_art_manager: ASCIIArtManager = ASCIIArtManager(self.theme_manager)
        self.plugin_manager: PluginManager = PluginManager(self.config)
        self.plugin_manager.load_plugins()


@app.callback()
def callback(
    ctx: typer.Context,
    config: str = typer.Option("cosmosys.toml", help="Path to the configuration file"),
    theme: str = typer.Option("default", help="Theme to use"),
) -> None:
    """Cosmosys: A flexible and customizable release management tool."""
    ctx.obj = CosmosysContext(config, theme)


@app.command()
def release(
    ctx: typer.Context,
    dry_run: bool = typer.Option(False, help="Perform a dry run without making any changes"),
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output"),
    interactive: bool = typer.Option(False, "--interactive", "-i", help="Enable interactive mode"),
) -> None:
    """Run the release process."""
    sf_ctx = ctx.obj
    config = sf_ctx.config
    console = sf_ctx.console
    ascii_art_manager = sf_ctx.ascii_art_manager

    display_header(ascii_art_manager, console)
    console.gradient("Starting release process...", "primary", "secondary")

    if config.is_auto_detected:
        console.info("Using auto-detected configuration.")

    if dry_run:
        console.warning("Dry run mode: No changes will be made")

    steps = config.get_steps()
    if verbose:
        console.info(f"Steps to execute: {', '.join(steps)}")

    release_manager = ReleaseManager(config, console, verbose)

    if interactive:
        steps = prompt_for_steps(steps, console)

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
    console.rainbow(message) if success else console.error(message)


def prompt_for_steps(steps: list, console: CosmosysConsole) -> list:
    """Prompt the user to confirm or modify the list of steps."""
    console.info("Interactive mode enabled.")
    confirmed_steps = []
    for step in steps:
        if typer.confirm(f"Execute step '{step}'?", default=True):
            confirmed_steps.append(step)
    return confirmed_steps


@app.command()
def config(
    ctx: typer.Context,
    set_key: str = typer.Option(None, "--set", help="Set a configuration value"),
    set_value: str = typer.Option(None, "--value", help="Value to set"),
    get_key: str = typer.Option(None, "--get", help="Get a configuration value"),
    init: bool = typer.Option(False, "--init", help="Initialize a new configuration file"),
) -> None:
    """Manage Cosmosys configuration."""
    sf_ctx = ctx.obj
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
    sf_ctx = ctx.obj
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
    """Display the list of available themes."""
    table = Table(title="Available Themes", border_style=theme_manager.get_color("primary"))
    table.add_column("Theme Name", style=theme_manager.get_color("secondary"))
    table.add_column("Sample", style=theme_manager.get_color("info"))

    for theme_name, scheme in theme_manager.themes.items():
        sample = " ".join([scheme.emojis[key] for key in ["success", "error", "warning", "info"]])
        table.add_row(theme_name, sample)

    console.console.print(table)


@app.command()
def plugins(
    ctx: typer.Context,
    list_plugins: bool = typer.Option(False, "--list", help="List available plugins"),
    info_plugin: Optional[str] = typer.Option(None, "--info", help="Get info about a plugin"),
) -> None:
    """Manage Cosmosys plugins."""
    sf_ctx = ctx.obj
    plugin_manager = sf_ctx.plugin_manager
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
        title="Available Plugins", border_style=console.theme_manager.get_color("primary")
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
