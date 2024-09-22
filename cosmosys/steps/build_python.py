"""Build Python step for Cosmosys release process."""

import subprocess
from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("build_python")
class BuildPythonStep(Step):
    """Step for building Python packages during the release process."""

    def execute(self) -> bool:
        try:
            subprocess.run(
                ["python", "setup.py", "sdist", "bdist_wheel"],
                check=True
            )
            self.log("Successfully built Python package")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to build Python package: {e}")
            return False

    def rollback(self) -> None:
        self.log(
            "Rollback not supported for build_python step. "
            "Please clean build artifacts manually if necessary."
        )
