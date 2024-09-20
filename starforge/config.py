from typing import Any, Dict, List

import toml


class StarForgeConfig:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config: Dict[str, Any] = {}
        self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, "r") as f:
                self.config = toml.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        except toml.TomlDecodeError as e:
            raise ValueError(f"Invalid TOML in configuration file: {e}")

    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self.config
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        return value if value is not None else default

    def set(self, key: str, value: Any):
        keys = key.split(".")
        config = self.config
        for k in keys[:-1]:
            config = config.setdefault(k, {})
        config[keys[-1]] = value

    def save(self):
        with open(self.config_file, "w") as f:
            toml.dump(self.config, f)

    def get_steps(self) -> List[str]:
        return self.get("release.steps", [])

    def is_feature_enabled(self, feature: str) -> bool:
        return self.get(f"features.{feature}", False)


def load_config(config_file: str) -> StarForgeConfig:
    return StarForgeConfig(config_file)
