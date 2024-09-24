"""Publish npm step for Cosmosys release process."""

import subprocess

from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("publish_npm")
class PublishNpmStep(Step):
    """Step for publishing Node.js packages to npm during the release process."""

    def execute(self) -> bool:
        """
        Execute the publish to npm step.

        Returns:
            bool: True if the publish was successful, False otherwise.
        """
        try:
            subprocess.run(["npm", "publish"], check=True)
            self.console.success("Successfully published package to npm")
            return True
        except subprocess.CalledProcessError as e:
            self.console.error(f"Failed to publish package to npm: {e}")
            return False

    def rollback(self) -> None:
        """Rollback the publish to npm step."""
        self.console.warning(
            "Warning: Cannot automatically unpublish from npm. "
            "Please manually remove the package if necessary."
        )
