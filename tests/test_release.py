# pylint: disable=redefined-outer-name
"""Unit tests for the Cosmosys release process."""

from unittest.mock import MagicMock, patch

import pytest
from typer.testing import CliRunner

from cosmosys.config import ColorScheme, CosmosysConfig, ProjectConfig, ReleaseConfig
from cosmosys.steps.base import StepFactory
from cosmosys.steps.git_commit import GitCommitStep
from cosmosys.steps.version_update import VersionUpdateStep


@pytest.fixture
def mock_config() -> CosmosysConfig:
    """Fixture for creating a mock configuration."""
    return CosmosysConfig(
        project=ProjectConfig(name="TestProject", repo_name="test/repo", version="1.0.0"),
        color_scheme="default",
        custom_color_schemes={
            "custom": ColorScheme(
                primary="blue",
                secondary="green",
                success="cyan",
                error="red",
                warning="yellow",
                info="magenta",
            )
        },
        release=ReleaseConfig(steps=["version_update", "git_commit"]),
        features={"changelog": True},
    )


def test_version_update_step(mock_config: CosmosysConfig) -> None:
    """Test the version update step."""
    step = VersionUpdateStep(mock_config)

    with patch.object(step, "_update_version_in_files"):
        assert step.execute()
        assert mock_config.project.version == "1.0.1"

    step.rollback()
    assert mock_config.project.version == "1.0.0"


@patch("subprocess.run")
def test_git_commit_step(mock_run: MagicMock, mock_config: CosmosysConfig) -> None:
    """Test the git commit step."""
    # Ensure we're setting the git configuration correctly
    mock_config.set("git.files_to_commit", ["file1.py", "file2.py"])
    mock_config.set("git.commit_message", "Release {version}")

    # Print the configuration for debugging
    print(f"Mock config: {mock_config.to_dict()}")

    step = GitCommitStep(mock_config)
    mock_run.return_value.stdout = "abcdef123456"

    assert step.execute()
    assert step.commit_hash == "abcdef123456"

    mock_run.assert_any_call(["git", "add", "file1.py", "file2.py"], check=True)
    mock_run.assert_any_call(
        ["git", "commit", "-m", f"Release {mock_config.project.version}"],
        capture_output=True,
        text=True,
        check=True,
    )


def test_step_factory(mock_config: CosmosysConfig) -> None:
    """Test the step factory."""
    version_update_step = StepFactory.create("version_update", mock_config)
    assert isinstance(version_update_step, VersionUpdateStep)

    git_commit_step = StepFactory.create("git_commit", mock_config)
    assert isinstance(git_commit_step, GitCommitStep)

    with pytest.raises(ValueError):
        StepFactory.create("unknown_step", mock_config)


@patch("typer.echo")
@patch("cosmosys.steps.base.StepFactory.create")
def test_release_process(
    mock_create_step: MagicMock, mock_echo: MagicMock, mock_config: CosmosysConfig
) -> None:
    """Test the release process."""
    mock_steps = [MagicMock(), MagicMock()]
    mock_create_step.side_effect = mock_steps

    from cosmosys.cli import app

    runner = CliRunner()
    result = runner.invoke(app, ["release"], obj=mock_config)

    print(f"Exit code: {result.exit_code}")
    print(f"Output: {result.output}")
    print(f"Exception: {result.exception}")

    assert result.exit_code == 0
    assert mock_create_step.call_count == 2
    assert all(step.execute.called for step in mock_steps)
    assert "Release process completed" in result.output
