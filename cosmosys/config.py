# pylint: disable=too-many-instance-attributes

"""Enhanced configuration management for Cosmosys."""

import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import toml
from mashumaro import DataClassDictMixin

DEFAULT_CONFIG_FILE = "cosmosys.toml"


class ConfigurationError(Exception):
    """Exception raised for configuration errors."""


@dataclass
class ProjectConfig(DataClassDictMixin):
    """Configuration for the project details."""

    name: str
    repo_name: str
    version: str
    project_type: str
    issue_tracker: Optional[str] = None

    def __post_init__(self) -> None:
        """Validate project configuration."""
        if not self.name:
            raise ConfigurationError("Project name is required")
        if not self.repo_name:
            raise ConfigurationError("Repository name is required")
        if not self.version:
            raise ConfigurationError("Project version is required")
        if self.project_type not in ["python", "rust", "node", "unknown"]:
            raise ConfigurationError(f"Invalid project type: {self.project_type}")


@dataclass
class ThemeConfig(DataClassDictMixin):
    """Theme configuration."""

    name: str
    description: str
    primary: str
    secondary: str
    success: str
    error: str
    warning: str
    info: str
    emojis: Dict[str, str] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate theme configuration."""
        for color in [
            self.primary,
            self.secondary,
            self.success,
            self.error,
            self.warning,
            self.info,
        ]:
            if not color.startswith("#") or len(color) != 7:
                raise ConfigurationError(
                    f"Invalid color format: {color}. Use #RRGGBB format."
                )

        required_emojis = ["success", "error", "warning", "info"]
        for emoji in required_emojis:
            if emoji not in self.emojis:
                raise ConfigurationError(f"Missing emoji for {emoji}")


@dataclass
class ReleaseConfig(DataClassDictMixin):
    """Configuration for the release process."""

    steps: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        """Validate release configuration."""
        if not self.steps:
            raise ConfigurationError("At least one release step is required")

@dataclass
class VersionUpdateConfig(DataClassDictMixin):
    files: List[str] = field(default_factory=list)
    update_git_tags: bool = False
    
@dataclass
class CosmosysConfig(DataClassDictMixin):
    """Main configuration class for Cosmosys."""

    project: ProjectConfig
    theme: str = "default"
    custom_themes: Dict[str, ThemeConfig] = field(default_factory=dict)
    release: ReleaseConfig = field(default_factory=ReleaseConfig)
    features: Dict[str, bool] = field(default_factory=dict)
    version_update: VersionUpdateConfig = field(default_factory=VersionUpdateConfig)
    git: Dict[str, Any] = field(default_factory=dict)
    is_auto_detected: bool = False
    new_version: Optional[str] = None
    version_part: Optional[str] = None

    @classmethod
    def from_file(cls, config_file: str) -> "CosmosysConfig":
        """Load configuration from a file."""
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = toml.load(f)
            return cls.from_dict(config_data)
        except FileNotFoundError as exc:
            raise ConfigurationError(
                f"Configuration file not found: {config_file}"
            ) from exc
        except toml.TomlDecodeError as e:
            raise ConfigurationError(
                f"Invalid TOML in configuration file: {str(e)}"
            ) from e

    @classmethod
    def auto_detect_config(
        cls, base_path: Optional[str] = None
    ) -> "CosmosysConfig":
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
            git={
                "files_to_commit": ["*"],
                "commit_message": "Release {version}",
                "push_tags": True,
            },
            is_auto_detected=True,
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
        return "unknown"

    @staticmethod
    def detect_version(
        project_type: str, base_path: Optional[str] = None
    ) -> str:
        """Detect the current version based on the project type."""
        base_path = base_path or os.getcwd()
        version = "0.1.0"  # Default version

        try:
            if project_type == "python":
                with open(
                    os.path.join(base_path, "pyproject.toml"),
                    "r",
                    encoding="utf-8",
                ) as f:
                    pyproject = toml.load(f)
                version = (
                    pyproject.get("tool", {})
                    .get("poetry", {})
                    .get("version")
                    or pyproject.get("project", {})
                    .get("version", version)
                )
            elif project_type == "rust":
                with open(
                    os.path.join(base_path, "Cargo.toml"),
                    "r",
                    encoding="utf-8",
                ) as f:
                    cargo_toml = toml.load(f)
                version = cargo_toml.get("package", {}).get("version", version)
            elif project_type == "node":
                with open(
                    os.path.join(base_path, "package.json"),
                    "r",
                    encoding="utf-8",
                ) as f:
                    package_json = json.load(f)
                version = package_json.get("version", version)
        except (
            FileNotFoundError,
            json.JSONDecodeError,
            toml.TomlDecodeError,
        ) as e:
            print(
                f"Warning: Error detecting version: {str(e)}. Using default version {version}"
            )

        return version

    @staticmethod
    def get_default_steps(project_type: str) -> List[str]:
        """Get default release steps based on the project type."""
        common_steps = [
            "version_update",
            "changelog_update",
            "git_commit",
            "git_tag",
        ]
        if project_type == "python":
            return common_steps + ["build_python", "publish_pypi"]
        if project_type == "rust":
            return common_steps + ["build_rust", "publish_crates_io"]
        if project_type == "node":
            return common_steps + ["build_node", "publish_npm"]
        return common_steps

    def save(self, config_file: str = DEFAULT_CONFIG_FILE) -> None:
        """Save the configuration to a file."""
        try:
            with open(config_file, "w", encoding="utf-8") as f:
                toml.dump(self.to_dict(), f)
        except IOError as e:
            raise ConfigurationError(
                f"Error saving configuration file: {str(e)}"
            ) from e

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key."""
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
        """Set a configuration value by key."""
        keys = key.split(".")
        config_dict = self.to_dict()
        current = config_dict
        for k in keys[:-1]:
            current = current.setdefault(k, {})
        current[keys[-1]] = value
        try:
            self.__dict__.update(self.from_dict(config_dict).__dict__)
        except ValueError as e:
            raise ConfigurationError(
                f"Invalid configuration value: {str(e)}"
            ) from e

    def get_steps(self) -> List[str]:
        """Get the list of release steps."""
        if self.release.steps:
            return self.release.steps
        return self.get_default_steps(self.project.project_type)

    def is_feature_enabled(self, feature: str) -> bool:
        """Check if a feature is enabled."""
        return self.features.get(feature, False)

    def to_flat_dict(self) -> Dict[str, Any]:
        """Convert the configuration to a flat dictionary."""
        flat_dict: Dict[str, Any] = {}

        def recurse(prefix: str, obj: Any) -> None:
            if isinstance(obj, dict):
                for k, v in obj.items():
                    recurse(f"{prefix}.{k}" if prefix else k, v)
            else:
                flat_dict[prefix] = obj

        recurse("", self.to_dict())
        return flat_dict

    def validate(self) -> None:
        """Validate the entire configuration."""
        # Validate project config
        self.project.__post_init__()

        # Validate themes
        for theme_name, theme in self.custom_themes.items():
            try:
                theme.__post_init__()
            except ConfigurationError as e:
                raise ConfigurationError(
                    f"Invalid theme '{theme_name}': {str(e)}"
                ) from e

        # Validate release config
        self.release.__post_init__()

        # Validate features
        for feature, enabled in self.features.items():
            if not isinstance(enabled, bool):
                raise ConfigurationError(
                    f"Invalid feature configuration for '{feature}': must be a boolean"
                )

        # Validate git configuration
        required_git_keys = ["files_to_commit", "commit_message"]
        for key in required_git_keys:
            if key not in self.git:
                raise ConfigurationError(
                    f"Missing required git configuration: '{key}'"
                )

        print("Configuration validation successful.")


def load_config(config_file: str = DEFAULT_CONFIG_FILE) -> CosmosysConfig:
    """Load the configuration from a file."""
    try:
        config = CosmosysConfig.from_file(config_file)
        config.validate()
        return config
    except ConfigurationError as e:
        print(f"Error loading configuration: {str(e)}")
        print("Falling back to auto-detected configuration.")
        return CosmosysConfig.auto_detect_config()
