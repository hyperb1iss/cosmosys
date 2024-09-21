# pylint: disable=redefined-outer-name
"""Command-line interface for Cosmosys."""

import logging
import typer
from typer import Context, Option

from cosmosys.ascii_art import ASCIIArtManager
from cosmosys.color_schemes import ColorManager
from cosmosys.config import CosmosysConfig, load_config
from cosmosys.plugin_manager import PluginManager
from cosmosys.steps.base import StepFactory

app = typer.Typer()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class CosmosysContext:
    """Context object for Cosmosys CLI commands."""

    def __init__(self, config_file: str):
        """
        Initialize the Cosmosys context.

        Args:
            config_file (str): Path to the configuration file.
        """
        self.config: CosmosysConfig = load_config(config_file)
        self.color_manager: ColorManager = ColorManager(self.config)
        self.ascii_art_manager: ASCIIArtManager = ASCIIArtManager(self.color_manager)
        self.plugin_manager: PluginManager = PluginManager(self.config)
        self.plugin_manager.load_plugins()


@app.callback()
def callback(
    ctx: Context,
    config: str = Option("cosmosys.toml", help="Path to the configuration file"),
) -> None:
    """Cosmosys: A flexible and customizable release management tool."""
    if not isinstance(ctx.obj, CosmosysContext):
        ctx.obj = CosmosysContext(config)


@app.command()
def release(
    ctx: Context,
    dry_run: bool = Option(False, help="Perform a dry run without making any changes"),
) -> None:
    """Run the release process."""
    if isinstance(ctx.obj, CosmosysContext):
        sf_ctx = ctx.obj
        config = sf_ctx.config
        color_manager = sf_ctx.color_manager
        ascii_art_manager = sf_ctx.ascii_art_manager
    else:
        config = ctx.obj
        color_manager = ColorManager(config)
        ascii_art_manager = ASCIIArtManager(color_manager)

    typer.echo(ascii_art_manager.render_logo("primary"))
    typer.echo(color_manager.primary("Starting release process..."))

    if dry_run:
        typer.echo(color_manager.warning("Dry run mode: No changes will be made"))

    steps = config.get_steps()
    logger.debug("Steps to execute: %s", steps)

    for step_name in steps:
        logger.debug("Processing step: %s", step_name)
        try:
            step = StepFactory.create(step_name, config)
            logger.debug("Created step: %s", step)
            typer.echo(color_manager.info(f"Executing step: {step_name}"))
            if not dry_run:
                if step.execute():
                    typer.echo(color_manager.success(f"Step {step_name} completed successfully"))
                else:
                    typer.echo(color_manager.error(f"Step {step_name} failed"))
                    break
            else:
                typer.echo(color_manager.info(f"Dry run: Step {step_name} would be executed"))
        except Exception as e:
            logger.exception("Error in step %s", step_name, exc_info=e)
            typer.echo(color_manager.error(f"Error in step {step_name}: {str(e)}"))
            break

    typer.echo(ascii_art_manager.render_starfield(color="secondary"))
    typer.echo(color_manager.primary("Release process completed"))

@app.command()
def config(
    set_key: str = Option(None, "--set", help="Set a configuration value"),
    set_value: str = Option(None, "--value", help="Value to set"),
    get_key: str = Option(None, "--get", help="Get a configuration value"),
    init: bool = Option(False, "--init", help="Initialize a new configuration file"),
) -> None:
    """Manage Cosmosys configuration."""
    if init:
        config = CosmosysConfig.auto_detect_config()
        config.save()
        typer.echo("Initialized new configuration file: cosmosys.toml")
    else:
        config = load_config()

    if set_key and set_value:
        config.set(set_key, set_value)
        config.save()
        typer.echo(f"Set {set_key} to {set_value}")

    if get_key:
        value = config.get(get_key)
        typer.echo(f"{get_key}: {value}")

    if not any([init, set_key, get_key]):
        typer.echo("Current configuration:")
        typer.echo(config.to_dict())


@app.command()
def version() -> None:
    """Display the current version of Cosmosys."""
    # TODO: Implement dynamic version retrieval
    typer.echo("Cosmosys v0.1.0")


def main() -> None:
    """Entry point for the Cosmosys CLI."""
    app()


if __name__ == "__main__":
    main()
