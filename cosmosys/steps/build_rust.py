"""Build Rust step for Cosmosys release process."""

import subprocess

from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("build_rust")
class BuildRustStep(Step):
    """Step for building Rust packages during the release process."""

    def execute(self) -> bool:
        """
        Execute the build Rust step.

        Returns:
            bool: True if the build was successful, False otherwise.
        """
        try:
            subprocess.run(["cargo", "build", "--release"], check=True)
            self.console.success("Successfully built Rust package")
            return True
        except subprocess.CalledProcessError as e:
            self.console.error(f"Failed to build Rust package: {e}")
            return False

    def rollback(self) -> None:
        """Rollback the build Rust step."""
        self.console.info(
            "Rollback not supported for build_rust step. "
            "Please clean build artifacts manually if necessary."
        )
