"""Changelog update step for Cosmosys release process."""

from datetime import datetime
from cosmosys.config import CosmosysConfig
from cosmosys.steps.base import Step, StepFactory

@StepFactory.register("changelog_update")
class ChangelogUpdateStep(Step):
    """Step for updating the changelog during the release process."""

    def __init__(self, config: CosmosysConfig):
        super().__init__(config)
        self.changelog_file = "CHANGELOG.md"

    def execute(self) -> bool:
        new_version = self.config.project.version
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        try:
            with open(self.changelog_file, "r+") as f:
                content = f.read()
                f.seek(0, 0)
                f.write(f"## [{new_version}] - {current_date}\n\n")
                f.write("### Added\n- \n\n")
                f.write("### Changed\n- \n\n")
                f.write("### Fixed\n- \n\n")
                f.write(content)
            
            self.log(f"Updated changelog for version {new_version}")
            return True
        except IOError:
            self.log(f"Failed to update changelog: {self.changelog_file} not found")
            return False

    def rollback(self) -> None:
        # For simplicity, we're not implementing a rollback for the changelog update
        # In a real-world scenario, you might want to keep a backup of the original file
        self.log("Changelog rollback not implemented")