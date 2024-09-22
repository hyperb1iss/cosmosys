"""Publish PyPI step for Cosmosys release process."""

import subprocess
from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("publish_pypi")
class PublishPyPIStep(Step):
    """Step for publishing Python packages to PyPI during the release process."""

    def execute(self) -> bool:
        try:
            subprocess.run(["twine", "upload", "dist/*"], check=True)
            self.log("Successfully published package to PyPI")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to publish package to PyPI: {e}")
            return False

    def rollback(self) -> None:
        self.log(
            "Warning: Cannot automatically unpublish from PyPI. Please manually remove the package if necessary."
        )
