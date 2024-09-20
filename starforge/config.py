from typing import Any, Dict, List, Optional

import toml
from mashumaro import DataClassDictMixin
from dataclasses import dataclass, field


@dataclass
class ProjectConfig(DataClassDictMixin):
    name: str
    repo_name: str
    version: str
    issue_tracker: Optional[str] = None


@dataclass
class ColorScheme(DataClassDictMixin):
    primary: str
    secondary: str
    success: str
    error: str
    warning: str
    info: str


@dataclass
class ReleaseConfig(DataClassDictMixin):
    steps: List[str] = field(default_factory=list)


@dataclass
class StarForgeConfig(DataClassDictMixin):
    project: ProjectConfig
    color_scheme: str = "default"
    custom_color_schemes: Dict[str, ColorScheme] = field(default_factory=dict)
    release: ReleaseConfig = field(default_factory=ReleaseConfig)
    features: Dict[str, bool] = field(default_factory=dict)

    @classmethod
    def from_file(cls, config_file: str) -> "StarForgeConfig":
        try:
            with open(config_file, "r") as f:
                config_data = toml.load(f)
            return cls.from_dict(config_data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        except toml.TomlDecodeError as e:
            raise ValueError(f"Invalid TOML in configuration file: {e}")

    def save(self, config_file: str):
        with open(config_file, "w") as f:
            toml.dump(self.to_dict(), f)

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self.to_dict()
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any):
        keys = key.split(".")
        config = self.to_dict()
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value
        self.__dict__.update(self.from_dict(config).__dict__)

    def get_steps(self) -> List[str]:
        return self.release.steps

    def is_feature_enabled(self, feature: str) -> bool:
        return self.features.get(feature, False)


def load_config(config_file: str) -> StarForgeConfig:
    return StarForgeConfig.from_file(config_file)