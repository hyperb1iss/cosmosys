"""Version update step for Cosmosys release process."""

from typing import Optional

import typer

from cosmosys.config import CosmosysConfig
from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("version_update")
class VersionUpdateStep(Step):
    """Step for updating the version number during the release process."""

    def __init__(self, config: CosmosysConfig):
        """
        Initialize the VersionUpdateStep.

        Args:
            config: The Cosmosys configuration.
        """
        super().__init__(config)
        self.old_version: Optional[str] = None
        self.new_version: Optional[str] = None

    def execute(self) -> bool:
        """
        Execute the version update step.

        Returns:
            bool: True if the version was successfully updated, False otherwise.
        """
        self.old_version = self.config.project.version
        self.new_version = self._get_new_version()

        if not self.new_version:
            self.log("Failed to determine new version")
            return False

        self._update_version_in_files()
        self.config.project.version = self.new_version
        self.log(f"Updated version from {self.old_version} to {self.new_version}")
        return True

    def rollback(self) -> None:
        """Rollback the version update."""
        if self.old_version:
            self.config.project.version = self.old_version
            self._update_version_in_files()
            self.log(f"Rolled back version to {self.old_version}")

    def _get_new_version(self) -> Optional[str]:
        """
        Calculate the new version number.

        Returns:
            Optional[str]: The new version number, or None if it couldn't be determined.
        """
        if self.config.new_version:
            return self.config.new_version

        if self.config.version_part:
            return self._bump_version_part(self.config.version_part)

        # No version specified; prompt the user
        self.log("No version specified; prompting the user.")
        new_version = typer.prompt("Enter the new version", default=self.old_version)
        return new_version

    def _bump_version_part(self, part: str) -> Optional[str]:
        """
        Bump the specified part of the version.

        Args:
            part (str): The part to bump ('major', 'minor', 'patch').

        Returns:
            Optional[str]: The new version number.
        """
        parts = self.old_version.split(".")
        if len(parts) != 3:
            self.log(f"Invalid version format: {self.old_version}")
            return None

        major, minor, patch = map(int, parts)
        if part == "major":
            major += 1
            minor = 0
            patch = 0
        elif part == "minor":
            minor += 1
            patch = 0
        elif part == "patch":
            patch += 1
        else:
            self.log(f"Invalid part specified: {part}")
            return None

        return f"{major}.{minor}.{patch}"

    def _update_version_in_files(self) -> None:
        """Update the version number in project files."""
        # TODO: Implement updating version in project files
        pass
