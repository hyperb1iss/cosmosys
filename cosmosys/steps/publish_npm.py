"""Publish npm step for Cosmosys release process."""

import subprocess
from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("publish_npm")
class PublishNpmStep(Step):
    """Step for publishing Node.js packages to npm during the release process."""

    def execute(self) -> bool:
        try:
            subprocess.run(["npm", "publish"], check=True)
            self.log("Successfully published package to npm")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to publish package to npm: {e}")
            return False

    def rollback(self) -> None:
        self.log(
            "Warning: Cannot automatically unpublish from npm. Please manually remove the package if necessary."
        )
