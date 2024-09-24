# pylint: disable=broad-exception-caught
"""Release management module for Cosmosys."""

from typing import List

from cosmosys.config import CosmosysConfig
from cosmosys.console import CosmosysConsole
from cosmosys.steps.base import StepFactory


class ReleaseManager:
    """Manages the execution of release steps."""

    def __init__(
        self, config: CosmosysConfig, console: CosmosysConsole, verbose: bool
    ) -> None:
        """
        Initialize the ReleaseManager.

        Args:
            config (CosmosysConfig): The configuration object.
            console (CosmosysConsole): The Cosmosys console for output.
            verbose (bool): Whether to enable verbose output.
        """
        self.config = config
        self.console = console
        self.verbose = verbose

    def execute_steps(self, steps: List[str], dry_run: bool) -> bool:
        """Execute the list of release steps.

        Args:
            steps (List[str]): List of step names to execute.
            dry_run (bool): Whether to perform a dry run.

        Returns:
            bool: True if all steps completed successfully, False otherwise.
        """
        success = True
        for step_name in steps:
            if self.verbose:
                self.console.info(f"Processing step: {step_name}")
            try:
                step = StepFactory.create(step_name, self.config)
                if dry_run:
                    self.console.info(
                        f"Dry run: {step_name} (simulated execution)"
                    )
                elif step.execute():
                    self.console.success(f"Completed: {step_name}")
                else:
                    self.console.error(f"Failed: {step_name}")
                    self.rollback_steps(steps[: steps.index(step_name)])
                    success = False
                    break
            except Exception as e:
                if self.verbose:
                    self.console.error(
                        f"Detailed error: {type(e).__name__}: {str(e)}"
                    )
                self.rollback_steps(steps[: steps.index(step_name)])
                success = False
                break
        return success

    def rollback_steps(self, executed_steps: List[str]) -> None:
        """Rollback the executed steps in reverse order.

        Args:
            executed_steps (List[str]): List of executed step names.
        """
        self.console.warning("Rolling back changes...")
        for step_name in reversed(executed_steps):
            try:
                step = StepFactory.create(step_name, self.config)
                step.rollback()
                if self.verbose:
                    self.console.info(f"Rolled back: {step_name}")
            except Exception as e:
                self.console.error(f"Error rolling back {step_name}: {str(e)}")
        self.console.warning("Rollback completed.")
