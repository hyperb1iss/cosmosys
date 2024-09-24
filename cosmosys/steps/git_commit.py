"""Git commit step for Cosmosys release process"""

import subprocess
from typing import List, Optional

from cosmosys.context import CosmosysContext
from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("git_commit")
class GitCommitStep(Step):
    """Step for committing final updates during the release process."""

    def __init__(self, context: CosmosysContext):
        super().__init__(context)
        self.commit_hash: Optional[str] = None

    def execute(self) -> bool:
        """
        Execute the git commit step.

        Returns:
            bool: True if the commit was successful, False otherwise.
        """
        files_to_commit = self.config.get("git.files_to_commit", [])
        self.console.info(f"Files to commit: {files_to_commit}")
        commit_message = self.config.get("git.commit_message", "Release {version}")

        if not files_to_commit:
            self.console.error("No files specified for git commit")
            return False

        try:
            self._git_add(files_to_commit)
            self.commit_hash = self._git_commit(commit_message)
            self.console.success(f"Created git commit: {self.commit_hash}")
            return True
        except subprocess.CalledProcessError as e:
            self.console.error(f"Git operation failed: {e}")
            return False

    def rollback(self) -> None:
        """Rollback the git commit."""
        if self.commit_hash:
            try:
                self._git_reset(self.commit_hash)
                self.console.success(f"Rolled back git commit: {self.commit_hash}")
            except subprocess.CalledProcessError as e:
                self.console.error(f"Failed to rollback git commit: {e}")

    def _git_add(self, files: List[str]) -> None:
        """
        Add files to git staging area.

        Args:
            files (List[str]): List of files to add.
        """
        subprocess.run(["git", "add"] + files, check=True)

    def _git_commit(self, message: str) -> str:
        """
        Create a git commit with the specified message.

        Args:
            message (str): Commit message.

        Returns:
            str: The commit hash.
        """
        version = self.config.project.version
        formatted_message = message.format(version=version)
        result = subprocess.run(
            ["git", "commit", "-m", formatted_message], capture_output=True, text=True, check=True
        )
        return result.stdout.strip().split()[-1]

    def _git_reset(self, commit_hash: str) -> None:
        """
        Reset git to the specified commit.

        Args:
            commit_hash (str): The commit hash to reset to.
        """
        subprocess.run(["git", "reset", "--hard", f"{commit_hash}^"], check=True)
