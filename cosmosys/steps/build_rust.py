"""Build Rust step for Cosmosys release process."""

import subprocess
from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("build_rust")
class BuildRustStep(Step):
    """Step for building Rust packages during the release process."""

    def execute(self) -> bool:
        try:
            subprocess.run(["cargo", "build", "--release"], check=True)
            self.log("Successfully built Rust package")
            return True
        except subprocess.CalledProcessError as e:
            self.log(f"Failed to build Rust package: {e}")
            return False

    def rollback(self) -> None:
        # Remove build artifacts
        subprocess.run(["cargo", "clean"])
        self.log("Removed Rust build artifacts")
