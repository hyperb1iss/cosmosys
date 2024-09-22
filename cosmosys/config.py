"""Enhanced configuration management for Cosmosys."""

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import toml
from mashumaro import DataClassDictMixin

DEFAULT_CONFIG_FILE = "cosmosys.toml"


@dataclass
class ProjectConfig(DataClassDictMixin):
    """Configuration for the project details."""

    name: str
    repo_name: str
    version: str
    project_type: str
    issue_tracker: Optional[str] = None


@dataclass
class ColorScheme(DataClassDictMixin):
    """Color scheme configuration."""

    primary: str
    secondary: str
    success: str
    error: str
    warning: str
    info: str


@dataclass
class ReleaseConfig(DataClassDictMixin):
    """Configuration for the release process."""

    steps: List[str] = field(default_factory=list)


@dataclass
class CosmosysConfig(DataClassDictMixin):
    """Main configuration class for Cosmosys."""

    project: ProjectConfig
    color_scheme: str = "default"
    custom_color_schemes: Dict[str, ColorScheme] = field(default_factory=dict)
    release: ReleaseConfig = field(default_factory=ReleaseConfig)
    features: Dict[str, bool] = field(default_factory=dict)
    git: Dict[str, Any] = field(default_factory=dict)
    is_auto_detected: bool = False

    @classmethod
    def from_file(cls, config_file: str) -> "CosmosysConfig":
        """
        Load configuration from a file.

        Args:
            config_file (str): Path to the configuration file.

        Returns:
            CosmosysConfig: Loaded configuration object.
        """
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = toml.load(f)
            return cls.from_dict(config_data)
        except FileNotFoundError:
            return cls.auto_detect_config()
        except toml.TomlDecodeError:
            return cls.auto_detect_config()

    @classmethod
    def auto_detect_config(cls, base_path: Optional[str] = None) -> "CosmosysConfig":
        """Auto-detect project type and create a default configuration."""
        project_type = cls.detect_project_type(base_path)
        project_name = os.path.basename(base_path or os.getcwd())
        version = cls.detect_version(project_type, base_path)

        return cls(
            project=ProjectConfig(
                name=project_name,
                repo_name=f"{project_name}/{project_name}",
                version=version,
                project_type=project_type,
            ),
            release=ReleaseConfig(steps=cls.get_default_steps(project_type)),
            is_auto_detected=True
        )

    @staticmethod
    def detect_project_type(base_path: Optional[str] = None) -> str:
        """Detect the type of project based on files present in the given directory."""
        base_path = base_path or os.getcwd()
        if os.path.exists(os.path.join(base_path, "pyproject.toml")):
            return "python"
        if os.path.exists(os.path.join(base_path, "Cargo.toml")):
            return "rust"
        if os.path.exists(os.path.join(base_path, "package.json")):
            return "node"
        if os.path.exists(os.path.join(base_path, "setup.py")):
            return "python-setuptools"
        return "unknown"

    @staticmethod
    def detect_version(project_type: str, base_path: Optional[str] = None) -> str:
        """Detect the current version based on the project type."""
        base_path = base_path or os.getcwd()
        if project_type == "python":
            try:
                with open(os.path.join(base_path, "pyproject.toml"), "r", encoding="utf-8") as f:
                    pyproject = toml.load(f)
                return pyproject.get("tool", {}).get("poetry", {}).get("version") or pyproject.get(
                    "project", {}
                ).get("version", "0.1.0")
            except FileNotFoundError:
                print("Warning: pyproject.toml not found. Defaulting to version 0.1.0")
                return "0.1.0"
            except toml.TomlDecodeError:
                print("Warning: Invalid TOML in pyproject.toml. Defaulting to version 0.1.0")
                return "0.1.0"
        elif project_type == "rust":
            try:
                with open(os.path.join(base_path, "Cargo.toml"), "r", encoding="utf-8") as f:
                    cargo_toml = toml.load(f)
                return cargo_toml.get("package", {}).get("version", "0.1.0")
            except FileNotFoundError:
                print("Warning: Cargo.toml not found. Defaulting to version 0.1.0")
                return "0.1.0"
            except toml.TomlDecodeError:
                print("Warning: Invalid TOML in Cargo.toml. Defaulting to version 0.1.0")
                return "0.1.0"
        elif project_type == "node":
            try:
                with open(os.path.join(base_path, "package.json"), "r", encoding="utf-8") as f:
                    package_json = json.load(f)
                return package_json.get("version", "0.1.0")
            except FileNotFoundError:
                print("Warning: package.json not found. Defaulting to version 0.1.0")
                return "0.1.0"
            except json.JSONDecodeError:
                print("Warning: Invalid JSON in package.json. Defaulting to version 0.1.0")
                return "0.1.0"
        return "0.1.0"

    @staticmethod
    def get_default_steps(project_type: str) -> List[str]:
        """Get default release steps based on the project type."""
        common_steps = ["version_update", "changelog_update", "git_commit", "git_tag"]
        if project_type == "python":
            return common_steps + ["build_python", "publish_pypi"]
        if project_type == "rust":
            return common_steps + ["build_rust", "publish_crates_io"]
        if project_type == "node":
            return common_steps + ["build_node", "publish_npm"]
        return common_steps

    def save(self, config_file: str = DEFAULT_CONFIG_FILE) -> None:
        """
        Save the configuration to a file.

        Args:
            config_file (str): Path to save the configuration file.
        """
        with open(config_file, "w", encoding="utf-8") as f:
            toml.dump(self.to_dict(), f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.

        Args:
            key (str): The configuration key, using dot notation for nested keys.
            default (Any, optional): The default value to return if the key is not found.

        Returns:
            Any: The configuration value if found, otherwise the default value.
        """
        keys = key.split(".")
        value: Any = self.to_dict()
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        return value

    def set(self, key: str, value: Any) -> None:
        """
        Set a configuration value by key.

        Args:
            key (str): The configuration key, using dot notation for nested keys.
            value (Any): The value to set.
        """
        keys = key.split(".")
        config_dict = self.to_dict()
        current = config_dict
        for k in keys[:-1]:
            current = current.setdefault(k, {})
        current[keys[-1]] = value
        self.__dict__.update(self.from_dict(config_dict).__dict__)

    def get_steps(self) -> List[str]:
        """
        Get the list of release steps.

        Returns:
            List[str]: The list of release steps.
        """
        if self.release.steps:
            return self.release.steps
        return self.get_default_steps(self.project.project_type)

    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled."""
        return self.features.get(feature, False)

    def to_flat_dict(self) -> Dict[str, Any]:
        """
        Convert the configuration to a flat dictionary.

        Returns:
            Dict[str, Any]: A flat dictionary representation of the configuration.
        """
        flat_dict = {}

        def recurse(prefix: str, obj: Any):
            if isinstance(obj, dict):
                for k, v in obj.items():
                    recurse(f"{prefix}.{k}" if prefix else k, v)
            else:
                flat_dict[prefix] = obj

        recurse("", self.to_dict())
        return flat_dict


def load_config(config_file: str = DEFAULT_CONFIG_FILE) -> CosmosysConfig:
    """
    Load the configuration from a file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        CosmosysConfig: The loaded or auto-detected configuration object.
    """
    return CosmosysConfig.from_file(config_file)
