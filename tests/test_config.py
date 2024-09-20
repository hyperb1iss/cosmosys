"""Unit tests for the Cosmosys configuration module."""

from pathlib import Path
import pytest
from mashumaro.exceptions import InvalidFieldValue

from cosmosys.config import CosmosysConfig, ProjectConfig, ReleaseConfig, load_config


def test_valid_config() -> None:
    """Test creating a valid configuration."""
    config_data = {
        "project": {
            "name": "TestProject",
            "repo_name": "test/repo",
            "version": "1.0.0",
        },
        "color_scheme": "default",
        "release": {"steps": ["version_update", "git_commit"]},
        "features": {"changelog": True},
    }
    config = CosmosysConfig.from_dict(config_data)
    assert config.project.name == "TestProject"
    assert config.get_steps() == ["version_update", "git_commit"]
    assert config.is_feature_enabled("changelog")


def test_invalid_config() -> None:
    """Test handling of an invalid configuration."""
    invalid_config = {
        "project": {
            "name": "TestProject",
            "repo_name": "test/repo",
            # Missing required 'version' field
        },
    }
    with pytest.raises(InvalidFieldValue) as excinfo:
        CosmosysConfig.from_dict(invalid_config)
    assert 'Field "project" of type ProjectConfig in CosmosysConfig has invalid value' in str(
        excinfo.value
    )


def test_custom_color_scheme() -> None:
    """Test configuration with a custom color scheme."""
    config_data = {
        "project": {
            "name": "TestProject",
            "repo_name": "test/repo",
            "version": "1.0.0",
        },
        "color_scheme": "custom",
        "custom_color_schemes": {
            "custom": {
                "primary": "blue",
                "secondary": "green",
                "success": "cyan",
                "error": "red",
                "warning": "yellow",
                "info": "magenta",
            }
        },
    }
    config = CosmosysConfig.from_dict(config_data)
    assert config.color_scheme == "custom"
    assert config.custom_color_schemes["custom"].primary == "blue"


def test_load_config(tmp_path: Path) -> None:
    """Test loading configuration from a file."""
    config_file = tmp_path / "test_config.toml"
    config_content = """
    [project]
    name = "TestProject"
    repo_name = "test/repo"
    version = "1.0.0"

    color_scheme = "default"

    [release]
    steps = ["version_update", "git_commit"]

    [features]
    changelog = true
    """
    config_file.write_text(config_content)

    config = load_config(str(config_file))
    assert config.project.name == "TestProject"
    assert config.get_steps() == ["version_update", "git_commit"]
    assert config.is_feature_enabled("changelog")


def test_save_config(tmp_path: Path) -> None:
    """Test saving configuration to a file."""
    config_file = tmp_path / "test_config.toml"
    config = CosmosysConfig(
        project=ProjectConfig(name="TestProject", repo_name="test/repo", version="1.0.0"),
        color_scheme="default",
        release=ReleaseConfig(steps=["version_update", "git_commit"]),
        features={"changelog": True},
    )
    config.save(str(config_file))

    loaded_config = load_config(str(config_file))
    assert loaded_config.to_dict() == config.to_dict()
