"""Unit tests for the VersionUpdateStep in Cosmosys."""

from unittest.mock import patch

import pytest
from cosmosys.config import CosmosysConfig, ProjectConfig
from cosmosys.steps.version_update import VersionUpdateStep


@pytest.fixture
def mock_config():
    """Fixture for creating a mock CosmosysConfig."""
    return CosmosysConfig(
        project=ProjectConfig(
            name="TestProject",
            repo_name="test/repo",
            version="1.2.3",
            project_type="python",
        )
    )


def test_version_update_with_new_version(mock_config):
    """Test VersionUpdateStep with an explicit new version."""
    mock_config.new_version = "2.0.0"
    step = VersionUpdateStep(mock_config)
    assert step.execute()
    assert mock_config.project.version == "2.0.0"


def test_version_update_with_part_major(mock_config):
    """Test VersionUpdateStep bumping the major version."""
    mock_config.version_part = "major"
    step = VersionUpdateStep(mock_config)
    assert step.execute()
    assert mock_config.project.version == "2.0.0"


def test_version_update_with_part_minor(mock_config):
    """Test VersionUpdateStep bumping the minor version."""
    mock_config.version_part = "minor"
    step = VersionUpdateStep(mock_config)
    assert step.execute()
    assert mock_config.project.version == "1.3.0"


def test_version_update_with_part_patch(mock_config):
    """Test VersionUpdateStep bumping the patch version."""
    mock_config.version_part = "patch"
    step = VersionUpdateStep(mock_config)
    assert step.execute()
    assert mock_config.project.version == "1.2.4"


def test_version_update_prompt_user(mock_config):
    """Test VersionUpdateStep prompting the user for version."""
    with patch("typer.prompt") as mock_prompt:
        mock_prompt.return_value = "1.2.5"
        step = VersionUpdateStep(mock_config)
        assert step.execute()
        mock_prompt.assert_called_once_with("Enter the new version", default="1.2.3")
        assert mock_config.project.version == "1.2.5"


def test_version_update_invalid_version_format(mock_config):
    """Test VersionUpdateStep with an invalid version format."""
    mock_config.project.version = "1.2"
    mock_config.version_part = "patch"
    step = VersionUpdateStep(mock_config)
    assert not step.execute()
    assert mock_config.project.version == "1.2"
