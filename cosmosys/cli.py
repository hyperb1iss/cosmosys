from typing import List, Optional

import typer

from cosmosys.ascii_art import ASCIIArtManager
from cosmosys.color_schemes import ColorManager
from cosmosys.config import CosmosysConfig, load_config
from cosmosys.plugin_manager import PluginManager
from cosmosys.steps.base import StepFactory

app = typer.Typer()

class CosmosysContext:
    def __init__(self, config_file: str, color_scheme: str):
        self.config: CosmosysConfig = load_config(config_file)
        self.color_manager: ColorManager = ColorManager(self.config)
        self.ascii_art_manager: ASCIIArtManager = ASCIIArtManager(self.color_manager)
        self.plugin_manager: PluginManager = PluginManager(self.config)
        self.plugin_manager.load_plugins()

@app.callback()
def callback(
    ctx: typer.Context,
    config: str = typer.Option("cosmosys.toml", help="Path to the configuration file"),
    color_scheme: str = typer.Option("default", help="Color scheme to use"),
):
    """Cosmosys: A flexible and customizable release management tool."""
    if not isinstance(ctx.obj, CosmosysConfig):
        ctx.obj = CosmosysContext(config, color_scheme)

@app.command()
def release(
    ctx: typer.Context,
    dry_run: bool = typer.Option(False, help="Perform a dry run without making any changes"),
):
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

    for step_name in steps:
        try:
            step = StepFactory.create(step_name, config)
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
            typer.echo(color_manager.error(f"Error in step {step_name}: {str(e)}"))
            break

    typer.echo(ascii_art_manager.render_starfield(color="secondary"))
    typer.echo(color_manager.primary("Release process completed"))

@app.command()
def version():
    """Display the current version."""
    typer.echo("Cosmosys v0.1.0")  # TODO: Implement dynamic version retrieval

def main():
    app()

if __name__ == "__main__":
    main()