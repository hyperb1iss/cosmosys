"""Build Node.js step for Cosmosys release process."""

import subprocess

from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("build_node")
class BuildNodeStep(Step):
    """Step for building Node.js packages during the release process."""

    def execute(self) -> bool:
        """
        Execute the build Node.js step.

        Returns:
            bool: True if the build was successful, False otherwise.
        """
        try:
            subprocess.run(["npm", "run", "build"], check=True)
            self.console.success("Successfully built Node.js package")
            return True
        except subprocess.CalledProcessError as e:
            self.console.error(f"Failed to build Node.js package: {e}")
            return False

    def rollback(self) -> None:
        """Rollback the build Node.js step."""
        self.console.info(
            "Rollback not supported for build_node step. "
            "Please clean build artifacts manually if necessary."
        )
