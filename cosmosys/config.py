"""Configuration management for Cosmosys."""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import toml
from mashumaro import DataClassDictMixin


@dataclass
class ProjectConfig(DataClassDictMixin):
    """Configuration for the project details."""

    name: str
    repo_name: str
    version: str
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

    @classmethod
    def from_file(cls, config_file: str) -> "CosmosysConfig":
        """
        Load configuration from a file.

        Args:
            config_file (str): Path to the configuration file.

        Returns:
            CosmosysConfig: Loaded configuration object.

        Raises:
            FileNotFoundError: If the configuration file is not found.
            ValueError: If the TOML in the configuration file is invalid.
        """
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config_data = toml.load(f)
            return cls.from_dict(config_data)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Configuration file not found: {config_file}") from e
        except toml.TomlDecodeError as e:
            raise ValueError(f"Invalid TOML in configuration file: {e}") from e

    def save(self, config_file: str) -> None:
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
        return self.release.steps

    def is_feature_enabled(self, feature: str) -> bool:
        """
        Check if a feature is enabled.

        Args:
            feature (str): The name of the feature to check.

        Returns:
            bool: True if the feature is enabled, False otherwise.
        """
        return self.features.get(feature, False)


def load_config(config_file: str) -> CosmosysConfig:
    """
    Load the configuration from a file.

    Args:
        config_file (str): Path to the configuration file.

    Returns:
        CosmosysConfig: The loaded configuration object.
    """
    return CosmosysConfig.from_file(config_file)
