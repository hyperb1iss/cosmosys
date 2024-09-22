# pylint: disable=redefined-outer-name
"""Unit tests for the enhanced Cosmosys configuration module."""

import os
from pathlib import Path

import pytest
from typer.testing import CliRunner

from cosmosys.cli import app as cli_app
from cosmosys.config import CosmosysConfig, ProjectConfig, ReleaseConfig, load_config


@pytest.fixture
def temp_dir(tmp_path):
    """Fixture to create a temporary directory and change to it."""
    original_dir = os.getcwd()
    os.chdir(tmp_path)
    yield tmp_path
    os.chdir(original_dir)


def test_valid_config():
    """Test creating a valid configuration."""
    config_data = {
        "project": {
            "name": "TestProject",
            "repo_name": "test/repo",
            "version": "1.0.0",
            "project_type": "python",
        },
        "theme": "default",
        "release": {"steps": ["version_update", "git_commit"]},
        "features": {"changelog": True},
        "git": {"files_to_commit": ["*"], "commit_message": "Release {version}"},
    }
    config = CosmosysConfig.from_dict(config_data)
    assert config.project.name == "TestProject"
    assert config.get_steps() == ["version_update", "git_commit"]
    assert config.is_feature_enabled("changelog")
    assert config.project.project_type == "python"


def test_auto_detect_config_python(temp_dir):
    """Test auto-detection of Python project."""
    Path("pyproject.toml").write_text('[tool.poetry]\nversion = "0.2.0"')
    config = CosmosysConfig.auto_detect_config(temp_dir)
    assert config.project.project_type == "python"
    assert config.project.version == "0.2.0"


def test_auto_detect_config_rust(temp_dir):
    """Test auto-detection of Rust project."""
    Path("Cargo.toml").write_text('[package]\nversion = "0.3.0"')
    config = CosmosysConfig.auto_detect_config(temp_dir)
    assert config.project.project_type == "rust"
    assert config.project.version == "0.3.0"


def test_auto_detect_config_node(temp_dir):
    """Test auto-detection of Node.js project."""
    Path("package.json").write_text('{"version": "0.4.0"}')
    config = CosmosysConfig.auto_detect_config(temp_dir)
    assert config.project.project_type == "node"
    assert config.project.version == "0.4.0"


def test_auto_detect_config_unknown(temp_dir):
    """Test auto-detection of unknown project type."""
    config = CosmosysConfig.auto_detect_config(temp_dir)
    assert config.project.project_type == "unknown"
    assert config.project.version == "0.1.0"


def test_load_config_file_not_found(temp_dir):
    """Test loading configuration when file is not found."""
    config = load_config("non_existent_config.toml")
    assert isinstance(config, CosmosysConfig)
    assert config.project.project_type == "unknown"


def test_load_config_invalid_toml(temp_dir):
    """Test loading configuration with invalid TOML."""
    Path("invalid_config.toml").write_text("invalid = toml :")
    config = load_config("invalid_config.toml")
    assert isinstance(config, CosmosysConfig)
    assert config.is_auto_detected
    assert config.project.project_type == "unknown"


def test_save_and_load_config(temp_dir):
    """Test saving and then loading a configuration."""
    config = CosmosysConfig(
        project=ProjectConfig(
            name="TestProject", repo_name="test/repo", version="1.0.0", project_type="python"
        ),
        theme="default",
        release=ReleaseConfig(steps=["version_update", "git_commit"]),
        features={"changelog": True},
        git={
            "files_to_commit": ["file1.py", "file2.py"],
            "commit_message": "Release {version}",
        },
    )
    config.save()
    loaded_config = load_config()
    assert loaded_config.to_dict() == config.to_dict()


def test_get_and_set_config_values():
    """Test getting and setting configuration values."""
    config = CosmosysConfig(
        project=ProjectConfig(
            name="TestProject", repo_name="test/repo", version="1.0.0", project_type="python"
        ),
        release=ReleaseConfig(steps=["version_update"]),
        git={
            "files_to_commit": ["file1.py"],
            "commit_message": "Release {version}",
        },
    )
    config.set("features.new_feature", True)
    assert config.get("features.new_feature")
    assert config.get("non_existent_key", "default") == "default"


def test_cli_config_init(temp_dir):
    """Test CLI config initialization."""
    runner = CliRunner()
    result = runner.invoke(cli_app, ["config", "--init"])
    assert result.exit_code == 0
    assert "Initialized new configuration file: cosmosys.toml" in result.output
    assert Path("cosmosys.toml").exists()


def test_cli_config_set_and_get(temp_dir):
    """Test CLI config set and get operations."""
    runner = CliRunner()
    runner.invoke(cli_app, ["config", "--init"])

    set_result = runner.invoke(
        cli_app, ["config", "--set", "project.name", "--value", "NewProject"]
    )
    assert set_result.exit_code == 0
    assert "Set project.name to NewProject" in set_result.output

    get_result = runner.invoke(cli_app, ["config", "--get", "project.name"])
    assert get_result.exit_code == 0
    assert "project.name: NewProject" in get_result.output


def test_cli_config_view(temp_dir):
    """Test CLI config view operation."""
    runner = CliRunner()
    runner.invoke(cli_app, ["config", "--init"])
    result = runner.invoke(cli_app, ["config"])
    assert result.exit_code == 0
    assert "Current Configuration" in result.output
    assert "project" in result.output
