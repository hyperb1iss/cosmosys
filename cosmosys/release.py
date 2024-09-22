import logging
from rich.console import Console
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn, TimeElapsedColumn

from cosmosys.color_schemes import ColorManager
from cosmosys.config import CosmosysConfig
from cosmosys.steps.base import StepFactory

logger = logging.getLogger(__name__)


class ReleaseManager:
    """Manages the execution of release steps."""

    def __init__(
        self, config: CosmosysConfig, console: Console, color_manager: ColorManager, verbose: bool
    ):
        """
        Initialize the ReleaseManager.

        Args:
            config (CosmosysConfig): The configuration object.
            console (Console): The Rich console for output.
            color_manager (ColorManager): The color manager.
            verbose (bool): Whether to enable verbose output.
        """
        self.config = config
        self.console = console
        self.color_manager = color_manager
        self.verbose = verbose

    def execute_steps(self, steps: list, dry_run: bool) -> bool:
        """Execute the list of release steps.

        Args:
            steps (list): List of step names to execute.
            dry_run (bool): Whether to perform a dry run.

        Returns:
            bool: True if all steps completed successfully, False otherwise.
        """
        success = True
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeElapsedColumn(),
            console=self.console,
        ) as progress:
            for step_name in steps:
                task = progress.add_task(f"Executing step: {step_name}", total=None)
                if self.verbose:
                    logger.debug(f"Processing step: {step_name}")
                try:
                    step = StepFactory.create(step_name, self.config)
                    if self.verbose:
                        logger.debug(f"Created step: {step}")
                    if not dry_run:
                        if step.execute():
                            progress.update(
                                task,
                                completed=True,
                                description=self.color_manager.success(
                                    f"✅ Step {step_name} completed successfully"
                                ),
                            )
                        else:
                            progress.update(
                                task,
                                completed=True,
                                description=self.color_manager.error(f"❌ Step {step_name} failed"),
                            )
                            self.rollback_steps(steps[: steps.index(step_name)])
                            success = False
                            break
                    else:
                        progress.update(
                            task,
                            completed=True,
                            description=self.color_manager.info(
                                f"🔍 Dry run: Step {step_name} would be executed"
                            ),
                        )
                except Exception as e:
                    if self.verbose:
                        logger.exception(f"Error in step {step_name}")
                    progress.update(
                        task,
                        completed=True,
                        description=self.color_manager.error(
                            f"❌ Error in step {step_name}: {str(e)}"
                        ),
                    )
                    if self.verbose:
                        self.console.print(
                            self.color_manager.error(
                                f"Detailed error: {type(e).__name__}: {str(e)}"
                            )
                        )
                    self.rollback_steps(steps[: steps.index(step_name)])
                    success = False
                    break
        return success

    def rollback_steps(self, executed_steps: list) -> None:
        """Rollback the executed steps in reverse order.

        Args:
            executed_steps (list): List of executed step names.
        """
        self.console.print(self.color_manager.warning("⚠️ Rolling back changes..."))
        for step_name in reversed(executed_steps):
            try:
                step = StepFactory.create(step_name, self.config)
                step.rollback()
                if self.verbose:
                    logger.debug(f"Rolled back step: {step_name}")
            except Exception as e:
                if self.verbose:
                    logger.exception(f"Error rolling back step {step_name}")
                self.console.print(
                    self.color_manager.error(f"Error rolling back step {step_name}: {str(e)}")
                )
