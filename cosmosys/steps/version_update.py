"""Version update step for Cosmosys release process."""

import re
import os
from typing import Dict, List, Optional

import semver
import toml
import typer
from git import Repo

from cosmosys.context import CosmosysContext
from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("version_update")
class VersionUpdateStep(Step):
    """Step for updating the version number during the release process."""

    def __init__(self, context: CosmosysContext) -> None:
        """
        Initialize the VersionUpdateStep.

        Args:
            context (CosmosysContext): The Cosmosys context object.
        """
        super().__init__(context)
        self.old_version: Optional[semver.VersionInfo] = None
        self.new_version: Optional[semver.VersionInfo] = None
        self.version_files: Dict[str, List[str]] = self._get_version_files()

    def execute(self) -> bool:
        """
        Execute the version update step.

        Returns:
            bool: True if the version was successfully updated, False otherwise.
        """
        self.old_version = semver.VersionInfo.parse(self.config.project.version)
        self.new_version = self._get_new_version()

        if not self.new_version:
            self.console.error("Failed to determine new version")
            return False

        self._update_version_in_files()
        self.config.project.version = str(self.new_version)
        self.console.success(f"Updated version from {self.old_version} to {self.new_version}")
        return True

    def rollback(self) -> None:
        """Rollback the version update."""
        if self.old_version:
            self.config.project.version = str(self.old_version)
            self._update_version_in_files()
            self.console.info(f"Rolled back version to {self.old_version}")

    def _get_new_version(self) -> Optional[semver.VersionInfo]:
        """
        Calculate the new version number.

        Returns:
            Optional[semver.VersionInfo]: The new version number, or None if it couldn't be determined.
        """
        if self.config.new_version:
            return semver.VersionInfo.parse(self.config.new_version)

        if self.config.version_part:
            return self._bump_version_part(self.config.version_part)

        # No version specified; prompt the user
        self.console.info("No version specified; prompting the user.")
        version_options = [
            "major",
            "minor",
            "patch",
            "premajor",
            "preminor",
            "prepatch",
            "prerelease",
            "custom",
        ]
        version_choice = typer.prompt(
            "Choose version update type",
            type=typer.Choice(version_options),
            default="patch"
        )

        if version_choice == "custom":
            new_version_str = typer.prompt("Enter the new version", default=str(self.old_version))
            return semver.VersionInfo.parse(new_version_str)
        else:
            return self._bump_version_part(version_choice)

    def _bump_version_part(self, part: str) -> semver.VersionInfo:
        """
        Bump the specified part of the version.

        Args:
            part (str): The part to bump ('major', 'minor', 'patch', etc.).

        Returns:
            semver.VersionInfo: The new version number.
        """
        if part == "major":
            return self.old_version.bump_major()
        elif part == "minor":
            return self.old_version.bump_minor()
        elif part == "patch":
            return self.old_version.bump_patch()
        elif part == "premajor":
            return self.old_version.bump_premajor()
        elif part == "preminor":
            return self.old_version.bump_preminor()
        elif part == "prepatch":
            return self.old_version.bump_prepatch()
        elif part == "prerelease":
            return self.old_version.bump_prerelease()
        else:
            self.console.error(f"Invalid part specified: {part}")
            return self.old_version

    def _get_version_files(self) -> Dict[str, List[str]]:
        """
        Get the list of files to update based on project type and configuration.

        Returns:
            Dict[str, List[str]]: A dictionary of file types and their corresponding paths.
        """
        project_type = self.config.project.project_type
        custom_files = self.config.get("version_update.files", [])

        default_files = {
            "python": ["pyproject.toml", "setup.py", "__init__.py"],
            "rust": ["Cargo.toml"],
            "node": ["package.json"],
        }

        version_files = default_files.get(project_type, []) + custom_files

        # Group files by type
        grouped_files: Dict[str, List[str]] = {
            "toml": [],
            "json": [],
            "python": [],
            "other": [],
        }

        for file in version_files:
            if file.endswith(".toml"):
                grouped_files["toml"].append(file)
            elif file.endswith(".json"):
                grouped_files["json"].append(file)
            elif file.endswith(".py"):
                grouped_files["python"].append(file)
            else:
                grouped_files["other"].append(file)

        return grouped_files

    def _update_version_in_files(self) -> None:
        """Update the version number in project files."""
        for file_type, files in self.version_files.items():
            for file in files:
                if not os.path.exists(file):
                    self.console.warning(f"File not found: {file}")
                    continue

                if file_type == "toml":
                    self._update_toml_file(file)
                elif file_type == "json":
                    self._update_json_file(file)
                elif file_type == "python":
                    self._update_python_file(file)
                else:
                    self._update_other_file(file)

        self._update_git_tags()

    def _update_toml_file(self, file_path: str) -> None:
        """Update version in TOML files."""
        with open(file_path, "r+") as f:
            data = toml.load(f)
            if "version" in data:
                data["version"] = str(self.new_version)
            elif "package" in data and "version" in data["package"]:
                data["package"]["version"] = str(self.new_version)
            f.seek(0)
            toml.dump(data, f)
            f.truncate()

    def _update_json_file(self, file_path: str) -> None:
        """Update version in JSON files."""
        import json
        with open(file_path, "r+") as f:
            data = json.load(f)
            data["version"] = str(self.new_version)
            f.seek(0)
            json.dump(data, f, indent=2)
            f.truncate()

    def _update_python_file(self, file_path: str) -> None:
        """Update version in Python files."""
        with open(file_path, "r+") as f:
            content = f.read()
            new_content = re.sub(
                r'__version__\s*=\s*["\'].*["\']',
                f'__version__ = "{self.new_version}"',
                content
            )
            f.seek(0)
            f.write(new_content)
            f.truncate()

    def _update_other_file(self, file_path: str) -> None:
        """Update version in other file types."""
        with open(file_path, "r+") as f:
            content = f.read()
            new_content = content.replace(str(self.old_version), str(self.new_version))
            f.seek(0)
            f.write(new_content)
            f.truncate()

    def _update_git_tags(self) -> None:
        """Update Git tags with the new version."""
        if self.config.get("version_update.update_git_tags", False):
            repo = Repo(".")
            new_tag = f"v{self.new_version}"
            repo.create_tag(new_tag, message=f"Release {self.new_version}")
            self.console.success(f"Created new Git tag: {new_tag}")