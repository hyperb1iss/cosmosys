"""Publish Crates.io step for Cosmosys release process."""

import subprocess

from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("publish_crates_io")
class PublishCratesIoStep(Step):
    """Step for publishing Rust packages to Crates.io during the release process."""

    def execute(self) -> bool:
        """
        Execute the publish to Crates.io step.

        Returns:
            bool: True if the publish was successful, False otherwise.
        """
        try:
            subprocess.run(["cargo", "publish"], check=True)
            self.console.success("Successfully published package to Crates.io")
            return True
        except subprocess.CalledProcessError as e:
            self.console.error(f"Failed to publish package to Crates.io: {e}")
            return False

    def rollback(self) -> None:
        """Rollback the publish to Crates.io step."""
        self.console.warning(
            "Warning: Cannot automatically unpublish from Crates.io. "
            "Please manually remove the package if necessary."
        )
