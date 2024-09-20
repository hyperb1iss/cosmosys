import re
from typing import Optional

from starforge.steps.base import Step, StepFactory


@StepFactory.register("version_update")
class VersionUpdateStep(Step):
    def __init__(self, config):
        super().__init__(config)
        self.old_version: Optional[str] = None
        self.new_version: Optional[str] = None

    def execute(self) -> bool:
        self.old_version = self.config.get("version")
        self.new_version = self._get_new_version()

        if not self.new_version:
            self.log("Failed to determine new version")
            return False

        self._update_version_in_files()
        self.config.set("version", self.new_version)
        self.config.save()

        self.log(f"Updated version from {self.old_version} to {self.new_version}")
        return True

    def rollback(self):
        if self.old_version:
            self.config.set("version", self.old_version)
            self.config.save()
            self._update_version_in_files()
            self.log(f"Rolled back version to {self.old_version}")

    def _get_new_version(self) -> Optional[str]:
        # TODO: Implement proper version bumping logic
        if self.old_version:
            parts = self.old_version.split(".")
            if len(parts) == 3:
                parts[2] = str(int(parts[2]) + 1)
                return ".".join(parts)
        return None

    def _update_version_in_files(self):
        # TODO: Implement updating version in project files (e.g., pyproject.toml, __init__.py)
        pass
