"""Version management module for Cosmosys."""

import os
import re
from typing import Optional

import semver
import toml
import typer

from cosmosys.config import CosmosysConfig


class VersionManager:
    """Manages version-related operations for Cosmosys."""

    def __init__(self, config: CosmosysConfig):
        """
        Initialize the VersionManager.

        Args:
            config (CosmosysConfig): The Cosmosys configuration object.
        """
        self.config = config
        self.current_version = semver.VersionInfo.parse(config.project.version)
        self.new_version: Optional[semver.VersionInfo] = None

    def determine_new_version(self) -> semver.VersionInfo:
        """
        Determine the new version based on configuration or user input.

        Returns:
            semver.VersionInfo: The new version.
        """
        if self.config.new_version:
            return semver.VersionInfo.parse(self.config.new_version)

        if self.config.version_part:
            return self._bump_version_part(self.config.version_part)

        # No version specified; prompt the user
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
            "Choose version update type", type=typer.Choice(version_options), default="patch"
        )

        if version_choice == "custom":
            new_version_str = typer.prompt(
                "Enter the new version", default=str(self.current_version)
            )
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
            return self.current_version.bump_major()
        elif part == "minor":
            return self.current_version.bump_minor()
        elif part == "patch":
            return self.current_version.bump_patch()
        elif part == "premajor":
            return self.current_version.bump_premajor()
        elif part == "preminor":
            return self.current_version.bump_preminor()
        elif part == "prepatch":
            return self.current_version.bump_prepatch()
        elif part == "prerelease":
            return self.current_version.bump_prerelease()
        else:
            raise ValueError(f"Invalid version part: {part}")

    def update_version_in_files(self) -> None:
        """Update the version number in project files."""
        version_files = self._get_version_files()
        for file_type, files in version_files.items():
            for file in files:
                if not os.path.exists(file):
                    print(f"Warning: File not found: {file}")
                    continue

                if file_type == "toml":
                    self._update_toml_file(file)
                elif file_type == "json":
                    self._update_json_file(file)
                elif file_type == "python":
                    self._update_python_file(file)
                else:
                    self._update_other_file(file)

    def _get_version_files(self):
        """
        Get the list of files to update based on project type and configuration.

        Returns:
            dict: A dictionary of file types and their corresponding paths.
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
        grouped_files = {
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
                r'__version__\s*=\s*["\'].*["\']', f'__version__ = "{self.new_version}"', content
            )
            f.seek(0)
            f.write(new_content)
            f.truncate()

    def _update_other_file(self, file_path: str) -> None:
        """Update version in other file types."""
        with open(file_path, "r+") as f:
            content = f.read()
            new_content = content.replace(str(self.current_version), str(self.new_version))
            f.seek(0)
            f.write(new_content)
            f.truncate()
