"""Build Python step for Cosmosys release process."""

import subprocess

from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("build_python")
class BuildPythonStep(Step):
    """Step for building Python packages during the release process."""

    def execute(self) -> bool:
        """
        Execute the build Python step.

        Returns:
            bool: True if the build was successful, False otherwise.
        """
        try:
            subprocess.run(["python", "setup.py", "sdist", "bdist_wheel"], check=True)
            self.console.success("Successfully built Python package")
            return True
        except subprocess.CalledProcessError as e:
            self.console.error(f"Failed to build Python package: {e}")
            return False

    def rollback(self) -> None:
        """Rollback the build Python step."""
        self.console.info(
            "Rollback not supported for build_python step. "
            "Please clean build artifacts manually if necessary."
        )
