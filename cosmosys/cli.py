# pylint: disable=redefined-outer-name
"""Command-line interface for Cosmosys."""

import logging
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from rich.text import Text
from typer import Context, Option

from cosmosys.ascii_art import ASCIIArtManager
from cosmosys.color_schemes import ColorManager
from cosmosys.config import CosmosysConfig, load_config
from cosmosys.plugin_manager import PluginManager
from cosmosys.steps.base import StepFactory

app = typer.Typer()
console = Console()

logger = logging.getLogger(__name__)


class CosmosysContext:
    """Context object for Cosmosys CLI commands."""

    def __init__(self, config_file: str, color_scheme: str):
        """
        Initialize the Cosmosys context.

        Args:
            config_file (str): Path to the configuration file.
            color_scheme (str): The color scheme to use.
        """
        self.config: CosmosysConfig = load_config(config_file)
        self.color_manager: ColorManager = ColorManager(self.config)
        self.color_manager.set_scheme(color_scheme)
        self.ascii_art_manager: ASCIIArtManager = ASCIIArtManager(self.color_manager)
        self.plugin_manager: PluginManager = PluginManager(self.config)
        self.plugin_manager.load_plugins()


@app.callback()
def callback(
    ctx: Context,
    config: str = Option("cosmosys.toml", help="Path to the configuration file"),
    color_scheme: str = Option("default", help="Color scheme to use"),
) -> None:
    """Cosmosys: A flexible and customizable release management tool."""
    if not isinstance(ctx.obj, CosmosysContext):
        ctx.obj = CosmosysContext(config, color_scheme)


@app.command()
def release(
    ctx: Context,
    dry_run: bool = Option(False, help="Perform a dry run without making any changes"),
    verbose: bool = Option(False, "--verbose", "-v", help="Enable verbose output"),
) -> None:
    """Run the release process."""
    sf_ctx = ctx.obj
    config = sf_ctx.config
    color_manager = sf_ctx.color_manager
    ascii_art_manager = sf_ctx.ascii_art_manager

    # Set up logging
    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level, format="%(message)s")

    # Print logo
    logo = ascii_art_manager.render_logo()
    logo_panel = Panel(
        logo,
        expand=False,
        border_style=color_manager.get_color("primary"),
        title="✨ Cosmosys ✨",
        title_align="center",
    )
    console.print(logo_panel)

    # Print release process start message
    console.print(color_manager.gradient("🌠 Starting release process...", "primary", "secondary"))

    # Print config auto-detection message if necessary
    if config.is_auto_detected:
        console.print(color_manager.info("🔍 Using auto-detected configuration."))

    if dry_run:
        console.print(color_manager.warning("🚧 Dry run mode: No changes will be made"))

    steps = config.get_steps()
    if verbose:
        logger.debug(f"Steps to execute: {steps}")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        for step_name in steps:
            task = progress.add_task(f"Executing step: {step_name}", total=None)
            if verbose:
                logger.debug(f"Processing step: {step_name}")
            try:
                step = StepFactory.create(step_name, config)
                if verbose:
                    logger.debug(f"Created step: {step}")
                if not dry_run:
                    if step.execute():
                        progress.update(
                            task,
                            completed=True,
                            description=color_manager.success(
                                f"✅ Step {step_name} completed successfully"
                            ),
                        )
                    else:
                        progress.update(
                            task,
                            completed=True,
                            description=color_manager.error(f"❌ Step {step_name} failed"),
                        )
                        break
                else:
                    progress.update(
                        task,
                        completed=True,
                        description=color_manager.info(
                            f"🔍 Dry run: Step {step_name} would be executed"
                        ),
                    )
            except Exception as e:
                if verbose:
                    logger.exception(f"Error in step {step_name}")
                progress.update(
                    task,
                    completed=True,
                    description=color_manager.error(f"❌ Error in step {step_name}: {str(e)}"),
                )
                if verbose:
                    console.print(
                        color_manager.error(f"Detailed error: {type(e).__name__}: {str(e)}")
                    )
                break

    console.print(ascii_art_manager.render_starfield())
    completion_message = color_manager.rainbow("🎉 Release process completed 🎉")
    console.print(
        Panel(completion_message, expand=False, border_style=color_manager.get_color("primary"))
    )


@app.command()
def config(
    ctx: Context,
    set_key: str = Option(None, "--set", help="Set a configuration value"),
    set_value: str = Option(None, "--value", help="Value to set"),
    get_key: str = Option(None, "--get", help="Get a configuration value"),
    init: bool = Option(False, "--init", help="Initialize a new configuration file"),
) -> None:
    """Manage Cosmosys configuration."""
    sf_ctx = ctx.obj
    color_manager = sf_ctx.color_manager

    if init:
        config = CosmosysConfig.auto_detect_config()
        config.save()
        console.print(color_manager.success("✨ Initialized new configuration file: cosmosys.toml"))
    else:
        config = load_config()

    if set_key and set_value:
        config.set(set_key, set_value)
        config.save()
        console.print(color_manager.success(f"✅ Set {set_key} to {set_value}"))

    if get_key:
        value = config.get(get_key)
        console.print(color_manager.info(f"{get_key}: {value}"))

    if not any([init, set_key, get_key]):
        table = Table(
            title="Current Configuration", border_style=color_manager.get_color("primary")
        )
        table.add_column("Key", style=color_manager.get_color("secondary"))
        table.add_column("Value", style=color_manager.get_color("info"))

        for key, value in config.to_dict().items():
            if isinstance(value, dict):
                table.add_row(key, str(value))
            else:
                table.add_row(key, str(value))

        console.print(table)


@app.command()
def version() -> None:
    """Display the current version of Cosmosys."""
    # TODO: Implement dynamic version retrieval
    version_text = Text()
    version_text.append("🚀 ", style="bold")
    version_text.append("Cosmosys ", style="bold cyan")
    version_text.append("v0.1.0", style="bold")
    console.print(version_text)


@app.command()
def theme(
    ctx: Context,
    list_themes: bool = Option(False, "--list", help="List available color themes"),
    set_theme: Optional[str] = Option(None, "--set", help="Set the color theme"),
) -> None:
    """Manage Cosmosys color themes."""
    sf_ctx = ctx.obj
    color_manager = sf_ctx.color_manager

    if list_themes:
        table = Table(
            title="Available Color Themes", border_style=color_manager.get_color("primary")
        )
        table.add_column("Theme Name", style=color_manager.get_color("secondary"))
        table.add_column("Sample", style=color_manager.get_color("info"))

        for theme_name in color_manager.color_schemes.keys():
            sample = color_manager.rainbow("■■■■■■")
            table.add_row(theme_name, sample)

        console.print(table)

    if set_theme:
        if set_theme in color_manager.color_schemes:
            color_manager.set_scheme(set_theme)
            sf_ctx.config.color_scheme = set_theme
            sf_ctx.config.save()
            console.print(color_manager.success(f"✅ Color theme set to {set_theme}"))
        else:
            console.print(color_manager.error(f"❌ Invalid theme name: {set_theme}"))


def main() -> None:
    """Entry point for the Cosmosys CLI."""
    app()


if __name__ == "__main__":
    main()
