"""Git tag step for Cosmosys release process."""

import logging

from git import GitCommandError, Repo

from cosmosys.context import CosmosysContext
from cosmosys.steps.base import Step, StepFactory

logger = logging.getLogger(__name__)


@StepFactory.register("git_tag")
class GitTagStep(Step):
    """Step for creating a Git tag during the release process."""

    def __init__(self, context: CosmosysContext):
        super().__init__(context)
        self.repo = Repo(".")
        self.tag_name = f"v{self.config.project.version}"
        self.tag_message = f"Release {self.config.project.version}"

    def execute(self) -> bool:
        """
        Execute the git tag step.

        Returns:
            bool: True if the tag was successfully created, False otherwise.
        """
        try:
            if self.tag_exists():
                self.console.error(f"Tag {self.tag_name} already exists")
                return False

            new_tag = self.repo.create_tag(self.tag_name, message=self.tag_message)
            self.console.success(f"Created new tag: {new_tag.name}")

            if self.config.get("git.push_tags", False):
                self.push_tag()

            return True
        except GitCommandError as e:
            self.console.error(f"Failed to create Git tag: {str(e)}")
            return False

    def rollback(self) -> None:
        """Rollback the git tag creation."""
        try:
            if self.tag_exists():
                self.repo.delete_tag(self.tag_name)
                self.console.info(f"Deleted tag: {self.tag_name}")

                if self.config.get("git.push_tags", False):
                    self.repo.git.push("origin", f":refs/tags/{self.tag_name}")
                    self.console.info(f"Removed tag {self.tag_name} from remote")
            else:
                self.console.info(f"Tag {self.tag_name} does not exist, no rollback needed")
        except GitCommandError as e:
            self.console.error(f"Failed to rollback Git tag: {str(e)}")

    def tag_exists(self) -> bool:
        """
        Check if the tag already exists.

        Returns:
            bool: True if the tag exists, False otherwise.
        """
        return self.tag_name in self.repo.tags

    def push_tag(self) -> None:
        """Push the newly created tag to the remote repository."""
        try:
            self.repo.git.push("origin", self.tag_name)
            self.console.success(f"Pushed tag {self.tag_name} to remote")
        except GitCommandError as e:
            self.console.error(f"Failed to push tag to remote: {str(e)}")
