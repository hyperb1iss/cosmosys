"""Git tag step for Cosmosys release process."""

import logging
from git import Repo, GitCommandError
from cosmosys.config import CosmosysConfig
from cosmosys.steps.base import Step, StepFactory

logger = logging.getLogger(__name__)


@StepFactory.register("git_tag")
class GitTagStep(Step):
    """Step for creating a Git tag during the release process."""

    def __init__(self, config: CosmosysConfig):
        super().__init__(config)
        self.repo = Repo(".")
        self.tag_name = f"v{self.config.project.version}"
        self.tag_message = f"Release {self.config.project.version}"

    def execute(self) -> bool:
        try:
            if self.tag_exists():
                self.log(f"Tag {self.tag_name} already exists")
                return False

            new_tag = self.repo.create_tag(self.tag_name, message=self.tag_message)
            self.log(f"Created new tag: {new_tag.name}")

            if self.config.get("git.push_tags", False):
                self.push_tag()

            return True
        except GitCommandError as e:
            self.log(f"Failed to create Git tag: {str(e)}")
            return False

    def rollback(self) -> None:
        try:
            if self.tag_exists():
                self.repo.delete_tag(self.tag_name)
                self.log(f"Deleted tag: {self.tag_name}")

                if self.config.get("git.push_tags", False):
                    self.repo.git.push("origin", f":refs/tags/{self.tag_name}")
                    self.log(f"Removed tag {self.tag_name} from remote")
            else:
                self.log(f"Tag {self.tag_name} does not exist, no rollback needed")
        except GitCommandError as e:
            self.log(f"Failed to rollback Git tag: {str(e)}")

    def tag_exists(self) -> bool:
        """Check if the tag already exists."""
        return self.tag_name in self.repo.tags

    def push_tag(self) -> None:
        """Push the newly created tag to the remote repository."""
        try:
            self.repo.git.push("origin", self.tag_name)
            self.log(f"Pushed tag {self.tag_name} to remote")
        except GitCommandError as e:
            self.log(f"Failed to push tag to remote: {str(e)}")
