"""Changelog update step for Cosmosys release process."""

from datetime import datetime
from typing import Optional

from cosmosys.config import CosmosysConfig
from cosmosys.steps.base import Step, StepFactory


@StepFactory.register("changelog_update")
class ChangelogUpdateStep(Step):
    """Step for updating the changelog during the release process."""

    def __init__(self, config: CosmosysConfig) -> None:
        super().__init__(config)
        self.changelog_file = "CHANGELOG.md"
        self.original_content: Optional[str] = None

    def execute(self) -> bool:
        new_version = self.config.project.version
        current_date = datetime.now().strftime("%Y-%m-%d")

        try:
            with open(self.changelog_file, "r+", encoding="utf-8") as f:
                self.original_content = f.read()
                f.seek(0, 0)
                f.write(f"## [{new_version}] - {current_date}\n\n")
                f.write("### Added\n- \n\n")
                f.write("### Changed\n- \n\n")
                f.write("### Fixed\n- \n\n")
                f.write(self.original_content)

            self.log(f"Updated changelog for version {new_version}")
            return True
        except IOError:
            self.log(f"Failed to update changelog: {self.changelog_file} not found")
            return False

    def rollback(self) -> None:
        if self.original_content:
            try:
                with open(self.changelog_file, "w", encoding="utf-8") as f:
                    f.write(self.original_content)
                self.log("Rolled back changelog changes")
            except IOError as e:
                self.log(f"Failed to rollback changelog changes: {str(e)}")
        else:
            self.log("No changes to roll back in changelog")
