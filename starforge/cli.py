from typing import List, Optional

import typer

from starforge.ascii_art import ASCIIArtManager
from starforge.color_schemes import ColorManager
from starforge.config import StarForgeConfig, load_config
from starforge.plugin_manager import PluginManager
from starforge.steps.base import StepFactory

app = typer.Typer()


class StarForgeContext:
    def __init__(self, config_file: str, color_scheme: str):
        self.config: StarForgeConfig = load_config(config_file)
        self.color_manager: ColorManager = ColorManager(color_scheme)
        self.ascii_art_manager: ASCIIArtManager = ASCIIArtManager(self.color_manager)
        self.plugin_manager: PluginManager = PluginManager(self.config)
        self.plugin_manager.load_plugins()


@app.callback()
def callback(
    ctx: typer.Context,
    config: str = typer.Option("starforge.toml", help="Path to the configuration file"),
    color_scheme: str = typer.Option("default", help="Color scheme to use"),
):
    """StarForge: A flexible and customizable release management tool."""
    ctx.obj = StarForgeContext(config, color_scheme)


@app.command()
def init(ctx: typer.Context):
    """Initialize a new StarForge configuration."""
    sf_ctx: StarForgeContext = ctx.obj
    typer.echo(sf_ctx.color_manager.primary("Initializing StarForge configuration..."))
    # TODO: Implement configuration initialization


@app.command()
def release(
    ctx: typer.Context,
    steps: Optional[List[str]] = typer.Option(None, help="Specific release steps to run"),
    dry_run: bool = typer.Option(False, help="Perform a dry run without making any changes"),
):
    """Run the release process."""
    sf_ctx: StarForgeContext = ctx.obj

    typer.echo(sf_ctx.ascii_art_manager.render_logo("primary"))
    typer.echo(sf_ctx.color_manager.primary("Starting release process..."))

    if dry_run:
        typer.echo(sf_ctx.color_manager.warning("Dry run mode: No changes will be made"))

    if not steps:
        steps = sf_ctx.config.get_steps()

    for step_name in steps:
        try:
            step = StepFactory.create(step_name, sf_ctx.config)
            typer.echo(sf_ctx.color_manager.info(f"Executing step: {step_name}"))
            if not dry_run:
                if step.execute():
                    typer.echo(
                        sf_ctx.color_manager.success(f"Step {step_name} completed successfully")
                    )
                else:
                    typer.echo(sf_ctx.color_manager.error(f"Step {step_name} failed"))
                    break
            else:
                typer.echo(
                    sf_ctx.color_manager.info(f"Dry run: Step {step_name} would be executed")
                )
        except Exception as e:
            typer.echo(sf_ctx.color_manager.error(f"Error in step {step_name}: {str(e)}"))
            break

    typer.echo(sf_ctx.ascii_art_manager.render_starfield(color="secondary"))
    typer.echo(sf_ctx.color_manager.primary("Release process completed"))


@app.command()
def version():
    """Display the current version."""
    typer.echo("StarForge v0.1.0")  # TODO: Implement dynamic version retrieval


def main():
    app()


if __name__ == "__main__":
    main()
