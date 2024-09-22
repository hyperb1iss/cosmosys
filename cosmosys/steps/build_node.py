"""Build Node.js step for Cosmosys release process."""

import subprocess
from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("build_node")
class BuildNodeStep(Step):
    """Step for building Node.js packages during the release process."""

    def execute(self) -> bool:
        try:
            subprocess.run(["npm", "run", "build"], check=True)
            self.log("Successfully built Node.js package")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to build Node.js package: {e}")
            return False

    def rollback(self) -> None:
        self.log(
            "Rollback not supported for build_node step. "
            "Please clean build artifacts manually if necessary."
        )
