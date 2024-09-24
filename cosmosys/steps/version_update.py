"""Version update step for Cosmosys release process."""

from cosmosys.context import CosmosysContext
from cosmosys.steps.base import Step, StepFactory
from cosmosys.version_manager import VersionManager


@StepFactory.register("version_update")
class VersionUpdateStep(Step):
    """Step for updating the version number during the release process."""

    def __init__(self, context: CosmosysContext) -> None:
        """
        Initialize the VersionUpdateStep.

        Args:
            context (CosmosysContext): The Cosmosys context object.
        """
        super().__init__(context)
        self.version_manager = VersionManager(self.config)

    def execute(self) -> bool:
        """
        Execute the version update step.

        Returns:
            bool: True if the version was successfully updated, False otherwise.
        """
        try:
            self.version_manager.new_version = self.version_manager.determine_new_version()
            self.console.info(f"Updating version from {self.version_manager.current_version} to {self.version_manager.new_version}")
            self.version_manager.update_version_in_files()
            self.config.project.version = str(self.version_manager.new_version)
            self.console.success(f"Updated version to {self.version_manager.new_version}")
            return True
        except Exception as e:
            self.console.error(f"Failed to update version: {str(e)}")
            return False

    def rollback(self) -> None:
        """Rollback the version update."""
        if self.version_manager.current_version:
            self.config.project.version = str(self.version_manager.current_version)
            self.version_manager.new_version = self.version_manager.current_version
            self.version_manager.update_version_in_files()
            self.console.info(f"Rolled back version to {self.version_manager.current_version}")