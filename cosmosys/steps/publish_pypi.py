"""Publish PyPI step for Cosmosys release process."""

import subprocess

from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("publish_pypi")
class PublishPyPIStep(Step):
    """Step for publishing Python packages to PyPI during the release process."""

    def execute(self) -> bool:
        """
        Execute the publish to PyPI step.

        Returns:
            bool: True if the publish was successful, False otherwise.
        """
        try:
            subprocess.run(["twine", "upload", "dist/*"], check=True)
            self.console.success("Successfully published package to PyPI")
            return True
        except subprocess.CalledProcessError as e:
            self.console.error(f"Failed to publish package to PyPI: {e}")
            return False

    def rollback(self) -> None:
        """Rollback the publish to PyPI step."""
        self.console.warning(
            "Warning: Cannot automatically unpublish from PyPI. "
            "Please manually remove the package if necessary."
        )
